"""Behavioral security and RAM-lifecycle tests; no external services required."""

from collections import OrderedDict
from dataclasses import dataclass
import subprocess
import sys
import uuid

import pytest
from fastapi.testclient import TestClient

from live_questions.app import (
    API, MAX_BODY, MAX_CHARS, MAX_MESSAGES, MAX_STUDENTS, MESSAGE_TTL,
    ROOM_TTL, TEACHER_TTL, Limits, Settings, State, create_app,
)
from live_questions.password import hash_password, validate_hash, verify_password

ORIGIN = "https://testserver"
PASSWORD = "a classroom password 2026"


class Clock:
    def __init__(self):
        self.now = 2_000_000_000.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


@pytest.fixture(scope="session")
def password_hash():
    return hash_password(PASSWORD)


@dataclass
class Env:
    client: TestClient
    student: TestClient
    state: State
    clock: Clock


@pytest.fixture
def env(password_hash):
    clock = Clock()
    state = State(clock)
    app = create_app(Settings(ORIGIN, password_hash), state)
    with TestClient(app, base_url=ORIGIN) as teacher:
        # Only the outer client owns the shared application's lifespan.
        student = TestClient(app, base_url=ORIGIN)
        yield Env(teacher, student, state, clock)
        student.close()


def post(client, path, data, csrf=None, **kwargs):
    headers = {"Origin": ORIGIN, "X-Live-Request": "1"}
    if csrf is not None:
        headers["X-CSRF-Token"] = csrf
    headers.update(kwargs.pop("headers", {}))
    return client.post(API + path, json=data, headers=headers, **kwargs)


def classroom(env):
    login = post(env.client, "/login", {"password": PASSWORD})
    assert login.status_code == 200
    csrf = login.json()["csrf"]
    response = post(env.client, "/room/start", {}, csrf)
    assert response.status_code == 200
    return csrf, response.json()["room"]["code"]


def joined(env, code):
    result = post(env.student, "/join", {"code": code})
    assert result.status_code == 200
    return result.json()["csrf"]


def submit(env, csrf, text="Why does range stop here?", request_id=None):
    return post(env.student, "/questions", {
        "text": text, "request_id": request_id or str(uuid.uuid4()),
    }, csrf)


def test_teacher_student_roles_and_no_question_leak(env):
    assert env.student.get(API + "/teacher").status_code == 401
    assert env.student.get(API + "/events").status_code == 401
    teacher_csrf, code = classroom(env)
    student_csrf = joined(env, code)
    result = submit(env, student_csrf)
    assert result.status_code == 200
    assert set(result.json()) == {"accepted", "id", "duplicate"}
    status = env.student.get(API + "/student")
    assert set(status.json()) == {"csrf", "room"}
    assert set(status.json()["room"]) == {"expires_at", "paused"}
    assert "messages" not in status.text and code not in status.text
    assert env.student.get(API + "/teacher").status_code == 401
    assert post(env.student, "/room/close", {}, student_csrf).status_code == 401
    assert len(env.client.get(API + "/teacher").json()["messages"]) == 1
    assert post(env.client, "/questions", {"text": "x", "request_id": str(uuid.uuid4())}, teacher_csrf).status_code == 401


@pytest.mark.parametrize("headers", [
    {}, {"Origin": ORIGIN}, {"X-Live-Request": "1"},
    {"Origin": "https://evil.example", "X-Live-Request": "1"},
    {"Origin": ORIGIN, "X-Live-Request": "1", "Sec-Fetch-Site": "cross-site"},
])
def test_posts_require_same_origin_and_custom_header(env, headers):
    result = env.client.post(API + "/login", json={"password": PASSWORD}, headers=headers)
    assert result.status_code == 403
    assert not env.state.teachers


def test_mutations_require_correct_role_csrf(env):
    teacher_csrf, code = classroom(env)
    student_csrf = joined(env, code)
    assert post(env.client, "/room/pause", {"paused": True}).status_code == 403
    assert post(env.client, "/room/close", {}, "incorrect").status_code == 403
    assert submit(env, teacher_csrf).status_code == 403
    assert post(env.client, "/room/pause", {"paused": True}, teacher_csrf).status_code == 200
    assert submit(env, student_csrf).status_code == 409


def test_non_ascii_csrf_is_rejected_not_server_error(env):
    _, code = classroom(env)
    joined(env, code)
    result = post(env.student, "/questions", {"text": "hello", "request_id": str(uuid.uuid4())},
                  headers={"X-CSRF-Token": b"\xff"})
    assert result.status_code == 403


def test_bad_password_login_rate_limit_and_recovery(env):
    for _ in range(10):
        assert post(env.client, "/login", {"password": "wrong"}).status_code == 401
    limited = post(env.client, "/login", {"password": PASSWORD})
    assert limited.status_code == 429
    assert int(limited.headers["Retry-After"]) > 0
    env.clock.advance(601)
    login = post(env.client, "/login", {"password": PASSWORD})
    assert login.status_code == 200
    cookie = login.headers["set-cookie"]
    for marker in ("__Host-py101_teacher=", "HttpOnly", "Secure", "SameSite=strict", "Path=/"):
        assert marker in cookie
    assert "Domain=" not in cookie


def test_login_rotates_old_cookie_and_limits_teacher_sessions(env):
    first = post(env.client, "/login", {"password": PASSWORD})
    assert first.status_code == 200
    old_token = env.client.cookies.get("__Host-py101_teacher")
    assert post(env.client, "/login", {"password": PASSWORD}).status_code == 200
    assert old_token not in env.state.teachers
    for i in range(7):
        env.state.teachers[f"other-{i}"] = {"csrf": "x", "expires_at": env.clock() + 100}
    assert post(env.student, "/login", {"password": PASSWORD}).status_code == 429


def test_python_and_html_questions_remain_literal_plain_text(env):
    _, code = classroom(env)
    csrf = joined(env, code)
    text = '<img src=x onerror="alert(1)">\nif x < 3: print("你好")\n[link](javascript:alert(1))'
    assert submit(env, csrf, text).status_code == 200
    snapshot = env.client.get(API + "/teacher").json()
    assert snapshot["messages"][0]["text"] == text


@pytest.mark.parametrize("payload", [
    {"password": PASSWORD, "role": "admin"}, {"password": None},
    {"password": 1}, [], {}, "password", {"password": True},
])
def test_json_schema_rejects_unknown_missing_and_wrong_types(env, payload):
    assert post(env.client, "/login", payload).status_code == 400


def test_json_media_type_syntax_and_size(env):
    headers = {"Origin": ORIGIN, "X-Live-Request": "1"}
    assert env.client.post(API + "/login", content="{}", headers=headers).status_code == 415
    headers["Content-Type"] = "application/json"
    assert env.client.post(API + "/login", content="{", headers=headers).status_code == 400
    assert env.client.post(API + "/login", content=b"\xff", headers=headers).status_code == 400
    huge = '{"password":"' + "x" * MAX_BODY + '"}'
    assert env.client.post(API + "/login", content=huge, headers=headers).status_code == 413
    # Even a misleading declared length cannot bypass the streamed body limit.
    headers["Content-Length"] = "0"
    assert env.client.post(API + "/login", content=huge, headers=headers).status_code == 413


def test_deep_json_and_surrogate_password_are_rejected(env):
    headers = {"Origin": ORIGIN, "X-Live-Request": "1", "Content-Type": "application/json"}
    nested = "[" * 1500 + "0" + "]" * 1500
    assert len(nested) < MAX_BODY
    assert env.client.post(API + "/login", content=nested, headers=headers).status_code == 400
    result = env.client.post(API + "/login", content='{"password":"\\ud800"}', headers=headers)
    assert result.status_code == 401


@pytest.mark.parametrize("text", ["", "  ", "x" * (MAX_CHARS + 1), "x\x00y", "x\u202ey", "x\ud800y"])
def test_invalid_question_text_is_rejected(env, text):
    _, code = classroom(env)
    csrf = joined(env, code)
    # ASCII JSON encoding permits testing an escaped lone surrogate.
    import json
    result = env.student.post(API + "/questions", content=json.dumps({"text": text, "request_id": str(uuid.uuid4())}),
        headers={"Origin": ORIGIN, "X-Live-Request": "1", "X-CSRF-Token": csrf, "Content-Type": "application/json"})
    assert result.status_code == 400
    assert not env.state.messages


@pytest.mark.parametrize("code", ["bad", "00000000", "é" * 8, "中" * 8])
def test_bad_room_code_is_rejected_not_server_error(env, code):
    classroom(env)
    assert post(env.student, "/join", {"code": code}).status_code == 400


def test_pause_close_and_new_room_invalidate_old_students(env):
    teacher_csrf, code = classroom(env)
    student_csrf = joined(env, code)
    assert post(env.client, "/room/start", {}, teacher_csrf).status_code == 409
    assert post(env.client, "/room/pause", {"paused": True}, teacher_csrf).status_code == 200
    assert submit(env, student_csrf).status_code == 409
    assert post(env.client, "/room/pause", {"paused": 1}, teacher_csrf).status_code == 400
    assert post(env.client, "/room/pause", {"paused": False}, teacher_csrf).status_code == 200
    assert submit(env, student_csrf).status_code == 200
    assert post(env.client, "/room/close", {}, teacher_csrf).status_code == 200
    assert not env.state.students and not env.state.messages and not env.state.muted
    assert env.student.get(API + "/student").status_code == 401
    assert post(env.student, "/join", {"code": code}).status_code == 400
    new = post(env.client, "/room/start", {}, teacher_csrf).json()["room"]["code"]
    assert submit(env, student_csrf).status_code == 401
    assert joined(env, new) != student_csrf


def test_mute_survives_rejoining_with_existing_cookie(env):
    teacher_csrf, code = classroom(env)
    student_csrf = joined(env, code)
    assert submit(env, student_csrf).status_code == 200
    sender_id = env.state.messages[0]["sender_id"]
    assert post(env.client, "/room/mute", {"sender_id": sender_id}, teacher_csrf).status_code == 200
    assert not env.state.messages
    assert joined(env, code) == student_csrf
    env.clock.advance(6)
    assert submit(env, student_csrf).status_code == 403
    assert len(env.state.students) == 1
    assert post(env.client, "/room/mute", {"sender_id": "nonexistent"}, teacher_csrf).status_code == 404


def test_idempotency_cooldown_and_bounded_retry_metadata(env):
    _, code = classroom(env)
    csrf = joined(env, code)
    request_id = str(uuid.uuid4())
    first = submit(env, csrf, request_id=request_id)
    assert first.status_code == 200
    retry = submit(env, csrf, request_id=request_id)
    assert retry.json() == {"accepted": True, "id": first.json()["id"], "duplicate": True}
    assert submit(env, csrf, "A different question", request_id=request_id).status_code == 409
    assert len(env.state.messages) == 1
    assert submit(env, csrf).status_code == 429
    env.clock.advance(5)
    assert submit(env, csrf).status_code == 200
    for _ in range(25):
        env.clock.advance(5)
        assert submit(env, csrf).status_code == 200
    assert len(next(iter(env.state.students.values()))["recent"]) == 20


def test_bounded_message_retention_and_expiry(env):
    _, code = classroom(env)
    csrf = joined(env, code)
    for i in range(MAX_MESSAGES + 5):
        assert submit(env, csrf, str(i)).status_code == 200
        env.clock.advance(5)
    assert len(env.state.messages) == MAX_MESSAGES
    assert env.state.messages[0]["text"] == "5"
    old_revision = env.state.revision
    env.clock.advance(MESSAGE_TTL)
    snapshot = env.client.get(API + "/teacher").json()
    assert snapshot["messages"] == []
    assert snapshot["revision"] > old_revision


def test_room_and_teacher_expiry(env):
    _, code = classroom(env)
    csrf = joined(env, code)
    assert submit(env, csrf).status_code == 200
    env.clock.advance(ROOM_TTL)
    assert env.student.get(API + "/student").status_code == 401
    assert env.state.room is None and not env.state.messages
    assert env.client.get(API + "/teacher").status_code == 200
    env.clock.advance(TEACHER_TTL)
    assert env.client.get(API + "/teacher").status_code == 401


def test_max_students_and_room_question_rate_limit(env):
    _, code = classroom(env)
    csrf = joined(env, code)
    for i in range(MAX_STUDENTS - 1):
        env.state.students[f"test-{i}"] = {"csrf": "x", "sender_id": f"S-{i}", "last_sent": 0, "recent": OrderedDict()}
    assert joined(env, code) == csrf  # Existing student can reconnect at capacity.
    env.student.cookies.clear()
    assert post(env.student, "/join", {"code": code}).status_code == 429
    assert len(env.state.students) == MAX_STUDENTS
    for _ in range(300):
        env.state.limits.check(("questions", "room"), 300, 60, env.clock())
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as error:
        env.state.limits.check(("questions", "room"), 300, 60, env.clock())
    assert error.value.status_code == 429
    env.clock.advance(60)
    env.state.limits.check(("questions", "room"), 300, 60, env.clock())


def test_rate_metadata_is_bounded_and_expires():
    from fastapi import HTTPException
    limits = Limits()
    for i in range(2048):
        limits.check(("join", str(i)), 600, 60, 100)
    with pytest.raises(HTTPException) as error:
        limits.check(("join", "overflow"), 600, 60, 100)
    assert error.value.status_code == 429
    limits.cleanup(160)
    assert not limits.entries


def test_dismiss_clear_logout_and_stream_cap(env):
    teacher_csrf, code = classroom(env)
    csrf = joined(env, code)
    first = submit(env, csrf).json()["id"]
    env.clock.advance(5)
    assert submit(env, csrf).status_code == 200
    assert post(env.client, "/room/dismiss", {"id": first}, teacher_csrf).status_code == 200
    assert len(env.state.messages) == 1
    assert post(env.client, "/room/clear", {}, teacher_csrf).status_code == 200
    assert not env.state.messages
    env.state.streams = 8
    assert env.client.get(API + "/events").status_code == 429
    env.state.streams = 0
    assert post(env.client, "/logout", {}, teacher_csrf).status_code == 200
    assert not env.state.teachers and not env.state.students and env.state.room is None
    assert env.client.get(API + "/teacher").status_code == 401


@pytest.mark.parametrize("path,status", [("/health", 200), ("/teacher", 401), ("/not-found", 404)])
def test_api_cache_and_security_headers(env, path, status):
    result = env.student.get(API + path)
    assert result.status_code == status
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["x-content-type-options"] == "nosniff"
    assert result.headers["x-frame-options"] == "DENY"
    assert result.headers["referrer-policy"] == "no-referrer"
    csp = result.headers["content-security-policy"]
    assert "default-src 'none'" in csp and "frame-ancestors 'none'" in csp
    assert "unsafe-inline" not in csp


@pytest.mark.parametrize("path", ["/live/", "/teacher/", "/live/assets/student.js"])
def test_retired_question_form_is_not_linked(env, path):
    response = env.client.get(path)
    assert response.status_code == 200
    assert "wjx.cn" not in response.text
    assert "Wenjuanxing" not in response.text
    assert "问卷星" not in response.text


def test_hash_and_development_settings(password_hash):
    validate_hash(password_hash)
    assert verify_password(PASSWORD, password_hash)
    assert not verify_password(PASSWORD + "!", password_hash)
    for value in ("", "wrong$600000$" + "a" * 32 + "$" + "b" * 64,
                  "pbkdf2_sha256$1$" + "a" * 32 + "$" + "b" * 64):
        with pytest.raises(ValueError):
            validate_hash(value)
    for origin, dev in (("http://testserver", False), ("https://testserver/", False),
                        ("https://user:pass@testserver", False), ("https://testserver", True),
                        ("ftp://localhost", True)):
        with pytest.raises(ValueError):
            Settings(origin, password_hash, dev)
    assert Settings("http://127.0.0.1:8000", password_hash, True).cookie("teacher") == "py101_teacher"
    assert Settings(ORIGIN, password_hash).cookie("teacher") == "__Host-py101_teacher"


def test_hash_validation_is_not_disabled_by_python_optimization():
    script = "from live_questions.password import validate_hash; validate_hash('wrong$1$' + 'a'*32 + '$' + 'b'*64)"
    result = subprocess.run([sys.executable, "-O", "-c", script], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Invalid LIVE_PASSWORD_HASH" in result.stderr
