"""Quiz access and lifecycle tests use a temporary library, never class content."""
import json

import pytest

from live_questions.app import API, TEACHER_TTL, ROOM_TTL, State
from .test_app import env, password_hash, post, PASSWORD, classroom, joined


@pytest.fixture(autouse=True)
def quiz_files(tmp_path, monkeypatch):
    library = tmp_path / "quizzes"
    library.mkdir()
    for quiz_id in ("0912", "0919"):
        quiz = {"title": "Quiz " + quiz_id, "questions": [{
            "prompt": "Consider the following list:",
            "code": "values = [1, 2, 3]",
            "after": "Extract the third element.",
            "answer": "PRIVATE",
        }]}
        (library / (quiz_id + ".json")).write_text(json.dumps(quiz), encoding="utf-8")
    monkeypatch.setattr("live_questions.app.QUIZZES", library)
    return library


def test_quiz_login_and_private_content(env):
    for route in ["/quiz", "/quiz/", "/quiz/0912/"]:
        response = env.client.get(route)
        assert response.status_code == 200
        assert "noindex" in response.headers["x-robots-tag"]
        assert "[1, 2, 3]" not in response.text
    assert env.client.get(API + "/quizzes").status_code == 401
    assert env.client.get(API + "/quizzes/0912").status_code == 401
    assert env.client.get("/live/assets/0912.json").status_code == 404
    assert env.client.get("/quiz/0912.json").status_code == 404
    assert post(env.client, "/login", {"password": "incorrect"}).status_code == 401
    assert post(env.client, "/login", {"password": PASSWORD}).status_code == 200
    assert env.state.room is None
    response = env.client.get(API + "/quizzes")
    assert {q["id"] for q in response.json()["quizzes"]} == {"0912", "0919"}
    assert all("questions" not in quiz for quiz in response.json()["quizzes"])
    detail = env.client.get(API + "/quizzes/0912")
    assert detail.status_code == 200
    assert all("answer" not in q for q in detail.json()["questions"])
    assert detail.json()["questions"][0]["after"] == "Extract the third element."
    assert detail.headers["cache-control"] == "no-store"
    assert env.client.get(API + "/quizzes/missing").status_code == 404
    env.clock.advance(TEACHER_TTL + 1)
    assert env.client.get(API + "/quizzes/0912").status_code == 401


def test_student_cannot_read_quizzes_and_logout_revokes(env):
    csrf, code = classroom(env)
    joined(env, code)
    assert env.student.get(API + "/quizzes").status_code == 401
    assert env.student.get(API + "/quizzes/0919").status_code == 401
    assert env.client.get(API + "/quizzes/0919").status_code == 200
    assert post(env.client, "/logout", {}, csrf).status_code == 200
    assert env.client.get(API + "/quizzes/0919").status_code == 401


def test_content_edits_are_loaded_without_restart(env, tmp_path, monkeypatch):
    monkeypatch.setattr("live_questions.app.QUIZZES", tmp_path)
    post(env.client, "/login", {"password": PASSWORD})
    quiz = {"title": "Quiz 0926", "questions": [{"prompt": "First version", "answer": "A"}]}
    path = tmp_path / "0926.json"
    path.write_text(json.dumps(quiz))
    assert env.client.get(API + "/quizzes").json()["quizzes"][0]["id"] == "0926"
    quiz["questions"][0]["prompt"] = "Edited version"
    path.write_text(json.dumps(quiz))
    assert env.client.get(API + "/quizzes/0926").json()["questions"][0]["prompt"] == "Edited version"
    path.write_text("broken JSON")
    assert env.client.get(API + "/quizzes/0926").status_code == 503


def test_publish_join_close_and_republish(env):
    csrf = post(env.client, "/login", {"password": PASSWORD}).json()["csrf"]
    assert post(env.student, "/quiz-start", {}).status_code == 401
    assert post(env.client, "/quiz-start", {}).status_code == 403
    pub = post(env.client, "/quiz-start", {}, csrf).json()["quiz_room"]
    assert len(pub["code"]) == 8
    assert post(env.client, "/quiz-start", {}, csrf).status_code == 409
    assert env.student.get(API + "/quiz-student").status_code == 401
    assert post(env.student, "/quiz-join", {"code": "WRONG"}).status_code == 400
    joined_quiz = post(env.student, "/quiz-join", {"code": pub["code"].lower()})
    assert joined_quiz.status_code == 200
    library = env.student.get(API + "/quiz-library").json()
    assert {q["id"] for q in library["quizzes"]} == {"0912", "0919"}
    for quiz_id in ["0912", "0919"]:
        quiz = env.student.get(API + "/quiz-library/" + quiz_id).json()["quiz"]
        assert quiz["id"] == quiz_id
        assert all("answer" not in q for q in quiz["questions"])
        assert quiz["questions"][0]["after"] == "Extract the third element."
    assert env.student.get(API + "/quizzes/0919").status_code == 401
    assert env.student.get(API + "/quiz-session").status_code == 401
    assert env.student.get(API + "/quiz-student").status_code == 200
    assert post(env.student, "/quiz-close", {}).status_code == 401
    assert post(env.client, "/quiz-close", {}, csrf).status_code == 200
    assert env.student.get(API + "/quiz-student").status_code == 410
    assert post(env.student, "/quiz-join", {"code": pub["code"]}).status_code == 400
    newer = post(env.client, "/quiz-start", {}, csrf).json()["quiz_room"]
    assert env.student.get(API + "/quiz-student").status_code == 401
    assert post(env.student, "/quiz-join", {"code": newer["code"]}).status_code == 200
    env.clock.advance(ROOM_TTL + 1)
    assert env.student.get(API + "/quiz-student").status_code == 410
    assert env.client.get(API + "/teacher").json()["quiz_room"] is None
    assert not env.state.quiz_students
    assert State().quiz_room is None


def test_quiz_is_independent_and_logout_revokes(env):
    csrf, live_code = classroom(env)
    pub = post(env.client, "/quiz-start", {}, csrf).json()["quiz_room"]
    joined(env, live_code)
    assert env.student.get(API + "/quiz-student").status_code == 401
    post(env.student, "/quiz-join", {"code": pub["code"]})
    assert post(env.client, "/room/close", {}, csrf).status_code == 200
    assert env.student.get(API + "/quiz-student").status_code == 200
    assert post(env.client, "/logout", {}, csrf).status_code == 200
    assert env.student.get(API + "/quiz-student").status_code == 410


def test_library_updates_and_no_answer_fields(env, tmp_path, monkeypatch):
    monkeypatch.setattr("live_questions.app.QUIZZES", tmp_path)
    path = tmp_path / "0912.json"
    path.write_text(json.dumps({"title": "Quiz", "questions": [
        {"prompt": "Original", "answer": "PRIVATE", "explanation": "PRIVATE"}]}))
    csrf = post(env.client, "/login", {"password": PASSWORD}).json()["csrf"]
    pub = post(env.client, "/quiz-start", {}, csrf).json()["quiz_room"]
    path.write_text(json.dumps({"title": "Edited", "questions": [{"prompt": "New"}]}))
    post(env.student, "/quiz-join", {"code": pub["code"]})
    data = env.student.get(API + "/quiz-library/0912").json()["quiz"]
    assert data["questions"] == [{"prompt": "New"}]
    (tmp_path / "0919.json").write_text(json.dumps({"title": "New quiz", "questions": [{"prompt": "Another question", "answer": "PRIVATE"}]}))
    assert len(env.student.get(API + "/quiz-library").json()["quizzes"]) == 2
    assert env.student.get(API + "/quiz-library/0919").json()["quiz"]["questions"] == [{"prompt": "Another question"}]
    assert env.client.get(API + "/quizzes/0912").json()["title"] == "Edited"


def test_removed_quizzes_leave_the_library_without_restart(env, quiz_files):
    csrf = post(env.client, "/login", {"password": PASSWORD}).json()["csrf"]
    code = post(env.client, "/quiz-start", {}, csrf).json()["quiz_room"]["code"]
    assert post(env.student, "/quiz-join", {"code": code}).status_code == 200
    for quiz_id, remaining in [("0919", ["0912"]), ("0912", [])]:
        (quiz_files / (quiz_id + ".json")).unlink()
        for client, route in [(env.client, "/quizzes"), (env.student, "/quiz-library")]:
            response = client.get(API + route)
            assert response.status_code == 200
            assert [q["id"] for q in response.json()["quizzes"]] == remaining
            assert client.get(API + route + "/" + quiz_id).status_code == 404


def test_student_entrance_is_separate_from_teacher(env):
    html = env.client.get("/quiz/").text
    assert 'id="login-form"' not in html and 'publish-button' not in html
    assert 'id="join-form"' in html
    teacher = env.client.get("/teacher/").text
    assert 'id="start-quiz-button"' in teacher
    assert teacher.index('id="start-button"') < teacher.index('id="start-quiz-button"')
    post(env.client, "/login", {"password": PASSWORD})
    assert env.client.get(API + "/quiz-library").status_code == 410
    assert env.client.get(API + "/quiz-library/0912").status_code == 410
    assert env.client.get(API + "/teacher").json()["quiz_room"] is None
