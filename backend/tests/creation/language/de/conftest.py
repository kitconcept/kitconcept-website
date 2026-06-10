import pytest


@pytest.fixture(scope="class")
def available_languages() -> list[str]:
    return ["de"]


@pytest.fixture(scope="class")
def language() -> str:
    return "de"
