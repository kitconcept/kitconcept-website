import pytest


@pytest.fixture(scope="class")
def available_languages() -> list[str]:
    return ["de", "en"]


@pytest.fixture(scope="class")
def language() -> str:
    return "de"
