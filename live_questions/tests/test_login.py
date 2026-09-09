"""Password-policy and actionable local-login diagnostics."""

import pytest
from fastapi.testclient import TestClient

from live_questions import password as password_tools
from live_questions.app import API, Settings, create_app

ORIGIN = "http://127.0.0.1:8765"


@pytest.mark.parametrize("password", ["x", "1234", "课堂密码", "x" * 300])
def test_generated_password_logs_in_without_length_policy(monkeypatch, capsys, password):
    answers = iter([password, password])
    monkeypatch.setattr(password_tools.getpass, "getpass", lambda prompt: next(answers))
    password_tools.main()
    line = capsys.readouterr().out.strip()
    assert line.startswith("LIVE_PASSWORD_HASH=")
    encoded = line.removeprefix("LIVE_PASSWORD_HASH=")
    password_tools.validate_hash(encoded)
    app = create_app(Settings(ORIGIN, encoded, dev=True))
    with TestClient(app, base_url=ORIGIN) as client:
        response = client.post(API + "/login", json={"password": password},
                               headers={"Origin": ORIGIN, "X-Live-Request": "1"})
        assert response.status_code == 200
        assert client.get(API + "/teacher").status_code == 200
        assert "HttpOnly" in response.headers["set-cookie"]
        assert "Secure" not in response.headers["set-cookie"]
        assert client.post(API + "/login", json={"password": password + "wrong"},
                           headers={"Origin": ORIGIN, "X-Live-Request": "1"}).status_code == 401


def test_generator_rejects_empty_password(monkeypatch):
    monkeypatch.setattr(password_tools.getpass, "getpass", lambda prompt: "")
    with pytest.raises(SystemExit, match="cannot be empty"):
        password_tools.main()


def test_generator_requires_confirmation(monkeypatch):
    answers = iter(["a", "b"])
    monkeypatch.setattr(password_tools.getpass, "getpass", lambda prompt: next(answers))
    with pytest.raises(SystemExit, match="do not match"):
        password_tools.main()


def test_origin_mismatch_explains_configuration_not_password():
    encoded = password_tools.hash_password("x")
    configured_origin = "https://maguoliang.cn"
    app = create_app(Settings(configured_origin, encoded))
    with TestClient(app, base_url=ORIGIN) as client:
        response = client.post(API + "/login", json={"password": "x"},
                               headers={"Origin": ORIGIN, "X-Live-Request": "1"})
        assert response.status_code == 403
        assert response.json() == {
            "detail": "The page address does not match LIVE_ORIGIN.",
            "code": "origin_mismatch",
            "expected_origin": configured_origin,
        }
        assert not app.state.live.teachers
        assert not app.state.live.limits.entries
        assert encoded not in response.text
        assert "set-cookie" not in response.headers


def test_password_still_requires_nonempty_and_bounded_request():
    app = create_app(Settings(ORIGIN, password_tools.hash_password("x"), dev=True))
    with TestClient(app, base_url=ORIGIN) as client:
        headers = {"Origin": ORIGIN, "X-Live-Request": "1"}
        assert client.post(API + "/login", json={"password": ""}, headers=headers).status_code == 401
        assert client.post(API + "/login", json={"password": "x" * 4096}, headers=headers).status_code == 413
