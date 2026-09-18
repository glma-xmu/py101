"""Validate whichever class quizzes are present, without requiring example dates."""

import re

import pytest

from live_questions.app import API, QUIZZES
from .test_app import env, password_hash, post, PASSWORD


def test_quiz_files_are_safe_to_deploy():
    assert not QUIZZES.is_symlink(), "The quiz directory must not be a symlink"
    paths = sorted(QUIZZES.glob("*.json"))
    assert paths, "Keep at least one quiz; deployment does not delete server files"
    assert set(QUIZZES.rglob("*.json")) == set(paths), "Keep quiz JSON at the top level"
    for path in paths:
        assert path.is_file() and not path.is_symlink(), f"Not a regular file: {path.name}"
        assert re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}\.json", path.name), path.name


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
