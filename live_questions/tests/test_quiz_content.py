"""Validate whichever class quizzes are present, without requiring example dates."""

import pytest

from live_questions.app import API, QUIZZES
from .test_app import env, password_hash, post, PASSWORD


@pytest.mark.parametrize("quiz_path", sorted(QUIZZES.glob("*.json")), ids=lambda path: path.name)
def test_class_quiz_content_is_valid(env, quiz_path):
    assert post(env.client, "/login", {"password": PASSWORD}).status_code == 200
    response = env.client.get(API + "/quizzes/" + quiz_path.stem)
    assert response.status_code == 200, f"{quiz_path.name}: {response.text}"


def test_class_library_matches_current_files(env):
    assert post(env.client, "/login", {"password": PASSWORD}).status_code == 200
    response = env.client.get(API + "/quizzes")
    assert response.status_code == 200, response.text
    assert [quiz["id"] for quiz in response.json()["quizzes"]] == [
        path.stem for path in sorted(QUIZZES.glob("*.json"))
    ]
