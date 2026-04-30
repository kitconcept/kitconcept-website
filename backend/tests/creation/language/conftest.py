from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.distribution.api import site as site_api
from Products.CMFPlone.Portal import PloneSite
from zope.component.hooks import setSite

import pytest


@pytest.fixture
def create_site(app, distribution_name):
    def func(answers: dict) -> PloneSite:
        with api.env.adopt_user(SITE_OWNER_NAME):
            site = site_api.create(app, distribution_name, answers)
            setSite(site)
        return site

    return func


@pytest.fixture()
def language() -> str:
    return "en"


@pytest.fixture()
def answers(prepare_answers, language) -> dict:
    answers = dict(prepare_answers().items())
    answers["default_language"] = language
    return answers
