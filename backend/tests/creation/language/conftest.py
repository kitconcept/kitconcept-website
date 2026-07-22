import pytest


@pytest.fixture(scope="class")
def available_languages() -> list[str]:
    return ["en"]


@pytest.fixture(scope="class")
def language() -> str:
    return "en"


@pytest.fixture(scope="class")
def answers(prepare_answers, available_languages, language) -> dict:
    answers = dict(prepare_answers().items())
    answers["setup_content"] = False
    answers["available_languages"] = available_languages
    answers["default_language"] = language
    return answers
