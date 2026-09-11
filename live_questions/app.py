"""Single-process, RAM-only classroom relay. No payload logs or database."""

from __future__ import annotations

import asyncio
from collections import OrderedDict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass
import json
import hashlib
import os
import re
from pathlib import Path
import secrets
import time
import unicodedata
from urllib.parse import urlsplit
import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from .password import validate_hash, verify_password

API = "/live/api"
STATIC = Path(__file__).parent / "static"
QUIZZES = Path(__file__).parent / "quizzes"
MAX_BODY = 4096
MAX_CHARS = 500
MESSAGE_TTL = 600
ROOM_TTL = 7200
TEACHER_TTL = 28800
MAX_MESSAGES = 100
MAX_STUDENTS = 500


@dataclass(frozen=True)
class Settings:
    origin: str
    password_hash: str
    dev: bool = False

    def __post_init__(self):
        parsed = urlsplit(self.origin)
        if parsed.path or parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValueError("LIVE_ORIGIN must have no path or trailing slash")
        if not parsed.hostname or parsed.scheme not in ("http", "https"):
            raise ValueError("LIVE_ORIGIN must be an HTTP(S) origin")
        if self.dev:
            if parsed.hostname not in ("localhost", "127.0.0.1", "::1"):
                raise ValueError("LIVE_DEV is allowed only for a loopback origin")
        elif parsed.scheme != "https":
            raise ValueError("Production requires HTTPS")
        validate_hash(self.password_hash)

    @classmethod
    def from_env(cls):
        return cls(os.environ.get("LIVE_ORIGIN", "https://maguoliang.cn"),
                   os.environ.get("LIVE_PASSWORD_HASH", ""), os.environ.get("LIVE_DEV") == "1")

    def cookie(self, role):
        return ("" if self.dev else "__Host-") + "py101_" + role


class Limits:
    """Bounded, expiring rate metadata; never stores question text."""

    def __init__(self):
        self.entries = OrderedDict()

    def check(self, key, limit, period, now):
        entry = self.entries.get(key)
        if entry is None:
            if len(self.entries) >= 2048:
                raise HTTPException(429, "Too many requests. Try later.", headers={"Retry-After": "60"})
            queue = deque()
            self.entries[key] = (queue, period)
        else:
            queue, _ = entry
        while queue and queue[0] <= now - period:
            queue.popleft()
        if len(queue) >= limit:
            wait = max(1, int(period - (now - queue[0])) + 1)
            raise HTTPException(429, "Please wait before trying again.", headers={"Retry-After": str(wait)})
        queue.append(now)

    def cleanup(self, now):
        for key, (queue, period) in list(self.entries.items()):
            if not queue or queue[-1] <= now - period:
                del self.entries[key]


class State:
    def __init__(self, clock=time.time):
        self.clock = clock
        self.teachers = {}
        self.students = {}
        self.quiz_students = {}
        self.quiz_room = None
        self.room = None
        self.messages = deque(maxlen=MAX_MESSAGES)
        self.muted = set()
        self.limits = Limits()
        self.revision = 0
        self.streams = 0
        self.password_checks = asyncio.Semaphore(2)

    def close_room(self):
        self.room = None
        self.students.clear()
        self.messages.clear()
        self.muted.clear()
        self.limits.entries.pop(("questions", "room"), None)
        self.revision += 1

    def close_quiz(self):
        self.quiz_room = None
        self.quiz_students.clear()
        self.revision += 1

    def cleanup(self):
        now = self.clock()
        self.limits.cleanup(now)
        for token, item in list(self.teachers.items()):
            if item["expires_at"] <= now:
                del self.teachers[token]
        if self.room and self.room["expires_at"] <= now:
            self.close_room()
        if self.quiz_room and self.quiz_room["expires_at"] <= now:
            self.close_quiz()
        old_length = len(self.messages)
        while self.messages and self.messages[0]["created_at"] <= now - MESSAGE_TTL:
            self.messages.popleft()
        if old_length != len(self.messages):
            self.revision += 1

    def snapshot(self, item):
        self.cleanup()
        return {"csrf": item["csrf"], "room": self.room, "quiz_room": self.quiz_room, "messages": list(self.messages),
                "revision": self.revision}


class SecurityHeaders:
    """ASGI middleware preserves streaming rather than buffering response bodies."""

    def __init__(self, app, settings):
        self.app, self.settings = app, settings

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])

        async def secure_send(message):
            if message["type"] == "http.response.start":
                extra = [
                    (b"cache-control", b"no-store"),
                    (b"x-content-type-options", b"nosniff"),
                    (b"referrer-policy", b"no-referrer"),
                    (b"x-frame-options", b"DENY"),
                    (b"content-security-policy", b"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"),
                ]
                message["headers"] = [h for h in message["headers"] if h[0].lower() != b"cache-control"] + extra
            await send(message)

        if scope["method"] == "POST":
            if headers.get(b"origin", b"").decode("latin1") != self.settings.origin:
                return await JSONResponse({
                    "detail": "The page address does not match LIVE_ORIGIN.",
                    "code": "origin_mismatch",
                    "expected_origin": self.settings.origin,
                }, 403)(scope, receive, secure_send)
            if (headers.get(b"x-live-request") != b"1"
                    or headers.get(b"sec-fetch-site") == b"cross-site"):
                return await JSONResponse({"detail": "Open the classroom page to submit this request."}, 403)(scope, receive, secure_send)
            try:
                length = int(headers.get(b"content-length", b"0"))
                if length < 0 or length > MAX_BODY:
                    raise ValueError
            except ValueError:
                return await JSONResponse({"detail": "Request is too large."}, 413)(scope, receive, secure_send)
        await self.app(scope, receive, secure_send)


async def body(request, fields):
    if request.headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
        raise HTTPException(415, "Send JSON only.")
    raw = bytearray()
    async for chunk in request.stream():
        if len(raw) + len(chunk) > MAX_BODY:
            raise HTTPException(413, "Request is too large.")
        raw.extend(chunk)
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError, RecursionError):
        raise HTTPException(400, "Invalid request.") from None
    if not isinstance(value, dict) or set(value) != set(fields):
        raise HTTPException(400, "Unexpected or missing fields.")
    for name, expected_type in fields.items():
        if type(value[name]) is not expected_type:
            raise HTTPException(400, "Invalid field type.")
    return value


def create_app(settings=None, state=None):
    settings = settings or Settings.from_env()
    state = state or State()

    @asynccontextmanager
    async def lifespan(app):
        async def expire():
            while True:
                await asyncio.sleep(5)
                state.cleanup()
        task = asyncio.create_task(expire())
        try:
            yield
        finally:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            state.close_room()
            state.close_quiz()
            state.teachers.clear()

    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    app.add_middleware(SecurityHeaders, settings=settings)
    app.state.live = state
    app.state.settings = settings

    def session(request, role, change=False):
        state.cleanup()
        token = request.cookies.get(settings.cookie(role), "")
        sessions = state.teachers if role == "teacher" else state.students
        item = sessions.get(token)
        if not item:
            raise HTTPException(401, "Please log in." if role == "teacher" else "Please join the classroom again.")
        if change:
            csrf = request.headers.get("x-csrf-token", "")
            if not csrf.isascii() or not secrets.compare_digest(csrf, item["csrf"]):
                raise HTTPException(403, "Session check failed. Reload the page.")
        return item

    def room_required():
        if not state.room:
            raise HTTPException(410, "This classroom has ended.")

    def set_cookie(response, role, token):
        response.set_cookie(settings.cookie(role), token, httponly=True, secure=not settings.dev,
                            samesite="strict", path="/")

    def limit(request, action, per_ip, total, period=60):
        state.cleanup()
        now = state.clock()
        ip = request.client.host if request.client else "unknown"
        state.limits.check((action, "global"), total, period, now)
        state.limits.check((action, ip), per_ip, period, now)

    def student_view(item):
        room_required()
        return {"csrf": item["csrf"], "room": {"expires_at": state.room["expires_at"], "paused": state.room["paused"]}}

    @app.get("/live/")
    async def student_page():
        return FileResponse(STATIC / "student.html")

    @app.get("/teacher/")
    async def teacher_page():
        return FileResponse(STATIC / "teacher.html")

    def read_quiz(quiz_id):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", quiz_id):
            raise HTTPException(404, "Quiz not found.")
        path = QUIZZES / (quiz_id + ".json")
        if not path.is_file():
            raise HTTPException(404, "Quiz not found.")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            assert isinstance(data, dict) and isinstance(data["title"], str)
            assert isinstance(data["questions"], list) and data["questions"]
            assert isinstance(data.get("description", ""), str)
            for question in data["questions"]:
                assert isinstance(question, dict)
                assert isinstance(question["prompt"], str) and question["prompt"]
                assert isinstance(question.get("code", ""), str)
                assert isinstance(question.get("after", ""), str)
                assert isinstance(question.get("options", []), list)
                assert all(isinstance(option, str) for option in question.get("options", []))
        except (ValueError, KeyError, AssertionError, TypeError):
            raise HTTPException(503, "Quiz content needs correction.") from None
        questions = [{key: question[key] for key in ("prompt", "code", "after", "options") if key in question}
                     for question in data["questions"]]
        return {"id": quiz_id, "title": data["title"],
                "description": data.get("description", ""), "questions": questions}

    @app.get("/quiz/")
    async def quiz_page():
        return FileResponse(STATIC / "quiz.html", headers={"X-Robots-Tag": "noindex, nofollow"})

    @app.get("/quiz/{quiz_id}/")
    async def quiz_detail_page(quiz_id: str):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", quiz_id) or not (QUIZZES / (quiz_id + ".json")).is_file():
            raise HTTPException(404, "Quiz not found.")
        return FileResponse(STATIC / "quiz.html", headers={"X-Robots-Tag": "noindex, nofollow"})

    @app.get(API + "/quizzes")
    async def quiz_index(request: Request):
        item = session(request, "teacher")
        quizzes = [read_quiz(path.stem) for path in sorted(QUIZZES.glob("*.json"))]
        return {"csrf": item["csrf"], "quizzes": [
            {"id": quiz["id"], "title": quiz["title"], "description": quiz["description"],
             "count": len(quiz["questions"])} for quiz in quizzes]}

    @app.get(API + "/quizzes/{quiz_id}")
    async def quiz_content(quiz_id: str, request: Request):
        session(request, "teacher")
        return read_quiz(quiz_id)

    def quiz_publication():
        if not state.quiz_room:
            return None
        return dict(state.quiz_room)

    def student_quiz(request):
        state.cleanup()
        if not state.quiz_room:
            raise HTTPException(410, "This quiz has closed or expired.")
        token = request.cookies.get(settings.cookie("quiz_student"), "")
        if token not in state.quiz_students:
            raise HTTPException(401, "Enter the quiz passcode.")
        return {"expires_at": state.quiz_room["expires_at"]}

    @app.get(API + "/quiz-session")
    async def quiz_session(request: Request):
        item = session(request, "teacher")
        return {"csrf": item["csrf"], "publication": quiz_publication()}

    @app.post(API + "/quiz-start")
    async def start_quiz(request: Request):
        item = session(request, "teacher", True)
        await body(request, {})
        if state.quiz_room:
            raise HTTPException(409, "Quiz access is already open.")
        state.quiz_room = {"code": "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8)),
                           "expires_at": state.clock() + ROOM_TTL}
        state.quiz_students.clear()
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/quiz-close")
    async def close_quiz(request: Request):
        item = session(request, "teacher", True)
        await body(request, {})
        state.close_quiz()
        return state.snapshot(item)

    @app.post(API + "/quiz-join")
    async def join_quiz(request: Request):
        limit(request, "quiz-join", 600, 1200)
        data = await body(request, {"code": str})
        code = data["code"].strip().upper()
        if (len(code) != 8 or not code.isascii() or not state.quiz_room
                or not secrets.compare_digest(code, state.quiz_room["code"])):
            raise HTTPException(400, "Quiz passcode is incorrect or has expired.")
        token = request.cookies.get(settings.cookie("quiz_student"), "")
        if token not in state.quiz_students:
            if len(state.quiz_students) >= MAX_STUDENTS:
                raise HTTPException(429, "This quiz is full.")
            token = secrets.token_urlsafe(32)
            state.quiz_students[token] = True
        response = JSONResponse({"expires_at": state.quiz_room["expires_at"]})
        set_cookie(response, "quiz_student", token)
        return response

    @app.get(API + "/quiz-student")
    async def get_student_quiz(request: Request):
        return student_quiz(request)

    @app.get(API + "/quiz-library")
    async def student_quiz_library(request: Request):
        access = student_quiz(request)
        quizzes = [read_quiz(path.stem) for path in sorted(QUIZZES.glob("*.json"))]
        return {**access, "quizzes": [
            {"id": quiz["id"], "title": quiz["title"], "description": quiz["description"],
             "count": len(quiz["questions"])} for quiz in quizzes]}

    @app.get(API + "/quiz-library/{quiz_id}")
    async def student_quiz_detail(quiz_id: str, request: Request):
        access = student_quiz(request)
        return {**access, "quiz": read_quiz(quiz_id)}

    @app.get("/live/assets/{name}")
    async def assets(name: str):
        if name not in {"live.css", "student.js", "teacher.js", "shared.js", "quiz.js", "quiz.css"}:
            raise HTTPException(404)
        return FileResponse(STATIC / name)

    @app.get(API + "/health")
    async def health():
        return {"status": "ok"}

    @app.get(API + "/config")
    async def config():
        return {"max_message_chars": MAX_CHARS, "message_ttl_minutes": MESSAGE_TTL // 60,
                "room_ttl_minutes": ROOM_TTL // 60, "buffer_size": MAX_MESSAGES}

    @app.post(API + "/login")
    async def login(request: Request):
        limit(request, "login", 10, 50, 600)
        data = await body(request, {"password": str})
        if not data["password"] or any(unicodedata.category(c) == "Cs" for c in data["password"]):
            raise HTTPException(401, "Incorrect password.")
        # Hash outside the event loop so streams remain responsive during login.
        async with state.password_checks:
            valid = await asyncio.to_thread(verify_password, data["password"], settings.password_hash)
        if not valid:
            raise HTTPException(401, "Incorrect password.")
        state.cleanup()
        state.teachers.pop(request.cookies.get(settings.cookie("teacher"), ""), None)
        if len(state.teachers) >= 8:
            raise HTTPException(429, "Too many teacher sessions. Close existing sessions or try later.")
        token = secrets.token_urlsafe(32)
        item = {"csrf": secrets.token_urlsafe(32), "expires_at": state.clock() + TEACHER_TTL}
        state.teachers[token] = item
        response = JSONResponse(state.snapshot(item))
        set_cookie(response, "teacher", token)
        return response

    @app.get(API + "/teacher")
    async def teacher_state(request: Request):
        return state.snapshot(session(request, "teacher"))

    @app.post(API + "/logout")
    async def logout(request: Request):
        session(request, "teacher", True)
        await body(request, {})
        # One-teacher pilot: logout ends class and revokes every teacher tab.
        state.close_room()
        state.close_quiz()
        state.teachers.clear()
        response = JSONResponse({"ok": True})
        response.delete_cookie(settings.cookie("teacher"), path="/", secure=not settings.dev, httponly=True, samesite="strict")
        return response

    @app.post(API + "/room/start")
    async def start(request: Request):
        item = session(request, "teacher", True)
        await body(request, {})
        if state.room:
            raise HTTPException(409, "End the current classroom before starting another.")
        code = "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(8))
        state.room = {"code": code, "expires_at": state.clock() + ROOM_TTL, "paused": False}
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/room/close")
    async def close(request: Request):
        item = session(request, "teacher", True)
        await body(request, {})
        state.close_room()
        return state.snapshot(item)

    @app.post(API + "/room/pause")
    async def pause(request: Request):
        item = session(request, "teacher", True)
        data = await body(request, {"paused": bool})
        room_required()
        state.room["paused"] = data["paused"]
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/room/clear")
    async def clear(request: Request):
        item = session(request, "teacher", True)
        await body(request, {})
        state.messages.clear()
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/room/dismiss")
    async def dismiss(request: Request):
        item = session(request, "teacher", True)
        data = await body(request, {"id": str})
        state.messages = deque((m for m in state.messages if m["id"] != data["id"]), maxlen=MAX_MESSAGES)
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/room/mute")
    async def mute(request: Request):
        item = session(request, "teacher", True)
        data = await body(request, {"sender_id": str})
        if not any(s["sender_id"] == data["sender_id"] for s in state.students.values()):
            raise HTTPException(404, "Sender is no longer in this classroom.")
        state.muted.add(data["sender_id"])
        state.messages = deque((m for m in state.messages if m["sender_id"] != data["sender_id"]), maxlen=MAX_MESSAGES)
        state.revision += 1
        return state.snapshot(item)

    @app.post(API + "/join")
    async def join(request: Request):
        # A whole classroom may share one IP; use a generous IP allowance.
        limit(request, "join", 600, 1200)
        data = await body(request, {"code": str})
        code = data["code"].strip().upper()
        if len(code) != 8 or not code.isascii() or not state.room or not secrets.compare_digest(code, state.room["code"]):
            raise HTTPException(400, "Classroom code is incorrect or has expired.")
        token = request.cookies.get(settings.cookie("student"), "")
        item = state.students.get(token)
        if not item:
            if len(state.students) >= MAX_STUDENTS:
                raise HTTPException(429, "This classroom is full. Use the alternative question form.")
            token = secrets.token_urlsafe(32)
            item = {"csrf": secrets.token_urlsafe(32), "sender_id": "S-" + secrets.token_hex(4),
                    "last_sent": 0, "recent": OrderedDict()}
            state.students[token] = item
        response = JSONResponse(student_view(item))
        set_cookie(response, "student", token)
        return response

    @app.get(API + "/student")
    async def student_status(request: Request):
        return student_view(session(request, "student"))

    @app.post(API + "/questions")
    async def question(request: Request):
        item = session(request, "student", True)
        state.limits.check(("requests", item["sender_id"]), 120, 60, state.clock())
        data = await body(request, {"text": str, "request_id": str})
        room_required()
        if item["sender_id"] in state.muted:
            raise HTTPException(403, "Submissions from this session have been paused by the teacher.")
        text = data["text"].strip()
        # Keep programming punctuation; do not interpret HTML, Markdown or Python.
        if not 1 <= len(text) <= MAX_CHARS or any(unicodedata.category(c) in {"Cc", "Cs"} and c not in "\n\t" for c in text):
            raise HTTPException(400, "Use 1 to 500 characters of plain text.")
        if any(c in "\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069" for c in text):
            raise HTTPException(400, "Unsupported invisible formatting characters.")
        try:
            request_id = str(uuid.UUID(data["request_id"]))
        except ValueError:
            raise HTTPException(400, "Invalid submission identifier.") from None
        if request_id in item["recent"]:
            previous_id, digest = item["recent"][request_id]
            if hashlib.sha256(text.encode()).hexdigest() != digest:
                raise HTTPException(409, "This submission identifier was already used for another question.")
            return {"accepted": True, "id": previous_id, "duplicate": True}
        if state.room["paused"]:
            raise HTTPException(409, "The teacher has paused questions.")
        now = state.clock()
        if now - item["last_sent"] < 5:
            raise HTTPException(429, "Please wait five seconds between questions.", headers={"Retry-After": "5"})
        state.limits.check(("questions", "room"), 300, 60, now)
        message = {"id": secrets.token_urlsafe(12), "sender_id": item["sender_id"], "text": text, "created_at": now}
        state.messages.append(message)
        item["last_sent"] = now
        item["recent"][request_id] = (message["id"], hashlib.sha256(text.encode()).hexdigest())
        while len(item["recent"]) > 20:
            item["recent"].popitem(last=False)
        state.revision += 1
        return {"accepted": True, "id": message["id"], "duplicate": False}

    @app.get(API + "/events")
    async def events(request: Request):
        item = session(request, "teacher")
        if state.streams >= 8:
            raise HTTPException(429, "Too many live teacher windows.")
        state.streams += 1
        token = request.cookies.get(settings.cookie("teacher"), "")

        async def stream():
            last_revision = -1
            last_ping = 0
            try:
                while not await request.is_disconnected():
                    state.cleanup()
                    if token not in state.teachers:
                        yield 'event: session_expired\ndata: {}\n\n'
                        return
                    if state.revision != last_revision:
                        payload = json.dumps(state.snapshot(item), ensure_ascii=True, separators=(",", ":"))
                        yield f"event: snapshot\ndata: {payload}\n\n"
                        last_revision = state.revision
                    if state.clock() - last_ping >= 15:
                        yield 'event: ping\ndata: {}\n\n'
                        last_ping = state.clock()
                    await asyncio.sleep(0.5)
            finally:
                state.streams -= 1
        return StreamingResponse(stream(), media_type="text/event-stream", headers={"X-Accel-Buffering": "no"})

    return app
