"""Real HTTP streaming tests; avoids TestClient's buffering of endless SSE."""

import json
import socket
import threading
import time
import uuid

import httpx
import uvicorn

from live_questions.app import API, MESSAGE_TTL, Settings, State, create_app
from .test_app import Clock, PASSWORD, password_hash


def read_event(lines, name):
    event_name = None
    data = []
    for line in lines:
        if not line:
            if event_name == name:
                return json.loads("\n".join(data))
            event_name, data = None, []
        elif line.startswith("event: "):
            event_name = line[7:]
        elif line.startswith("data: "):
            data.append(line[6:])
    raise AssertionError(f"Stream closed before {name!r} arrived")


def test_real_sse_snapshot_reconnect_expiry_and_logout(password_hash):
    clock = Clock()
    state = State(clock)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    origin = f"http://127.0.0.1:{port}"
    app = create_app(Settings(origin, password_hash, dev=True), state)
    server = uvicorn.Server(uvicorn.Config(app, log_level="critical", access_log=False))
    worker = threading.Thread(target=server.run, kwargs={"sockets": [listener]}, daemon=True)
    worker.start()

    def send(client, path, data, csrf=None):
        headers = {"Origin": origin, "X-Live-Request": "1"}
        if csrf:
            headers["X-CSRF-Token"] = csrf
        return client.post(API + path, json=data, headers=headers)

    try:
        deadline = time.monotonic() + 10
        while not server.started and worker.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started
        with httpx.Client(base_url=origin, timeout=5, trust_env=False) as teacher, httpx.Client(base_url=origin, timeout=5, trust_env=False) as student:
            login = send(teacher, "/login", {"password": PASSWORD})
            assert login.status_code == 200
            csrf = login.json()["csrf"]
            room = send(teacher, "/room/start", {}, csrf).json()["room"]
            student_csrf = send(student, "/join", {"code": room["code"]}).json()["csrf"]
            with teacher.stream("GET", API + "/events") as stream:
                assert stream.status_code == 200
                assert stream.headers["content-type"].startswith("text/event-stream")
                assert stream.headers["cache-control"] == "no-store"
                assert stream.headers["x-accel-buffering"] == "no"
                lines = stream.iter_lines()
                assert read_event(lines, "snapshot")["messages"] == []
                text = "How does async work?\n<script>alert('literal')</script>"
                result = send(student, "/questions", {"text": text, "request_id": str(uuid.uuid4())}, student_csrf)
                assert result.status_code == 200
                snapshot = read_event(lines, "snapshot")
                assert snapshot["messages"][0]["text"] == text

            # A reconnect receives a current bounded snapshot without relying on
            # event history or a browser-supplied Last-Event-ID.
            with teacher.stream("GET", API + "/events", headers={"Last-Event-ID": "untrusted"}) as stream:
                lines = stream.iter_lines()
                assert read_event(lines, "snapshot")["messages"][0]["text"] == text
                clock.advance(MESSAGE_TTL)
                assert read_event(lines, "snapshot")["messages"] == []
                assert send(teacher, "/logout", {}, csrf).status_code == 200
                assert read_event(lines, "session_expired") == {}
                assert list(lines) == []
            assert teacher.get(API + "/events").status_code == 401
            assert student.get(API + "/student").status_code == 401
        deadline = time.monotonic() + 3
        while state.streams and time.monotonic() < deadline:
            time.sleep(0.01)
        assert state.streams == 0
    finally:
        server.should_exit = True
        worker.join(timeout=5)
        listener.close()
    assert not worker.is_alive()
