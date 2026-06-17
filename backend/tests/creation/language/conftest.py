from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.distribution.api import site as site_api
from Products.CMFPlone.Portal import PloneSite
from zope.component.hooks import setSite

import pytest


@pytest.fixture(scope="class")
def app(integration_class):
    if hasattr(integration_class, "testSetUp"):
        integration_class.testSetUp()
    app = integration_class["app"]
    yield app
    if hasattr(integration_class, "testTearDown"):
        integration_class.testTearDown()


@pytest.fixture(scope="class")
def create_site(app, distribution_name):
    def func(answers: dict) -> PloneSite:
        with api.env.adopt_user(SITE_OWNER_NAME):
            site = site_api.create(app, distribution_name, answers)
            setSite(site)
        return site

    return func


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


@pytest.fixture(scope="class")
def portal(app, create_site, answers):
    portal = create_site(answers)
    yield portal
