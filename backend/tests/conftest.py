from kitconcept.core.factory import add_site
from kitconcept.website.testing import FUNCTIONAL_TESTING
from kitconcept.website.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME
from Products.CMFPlone.Portal import PloneSite
from pytest_plone import fixtures_factory
from typing import Any
from zope.component.hooks import site

import pytest


pytest_plugins = ["pytest_plone"]
globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture(scope="session")
def distribution_name() -> str:
    """Distribution name."""
    return "kitconcept-website"


@pytest.fixture(scope="class")
def portal_class(integration_class):
    if hasattr(integration_class, "testSetUp"):
        integration_class.testSetUp()
    portal = integration_class["portal"]
    with site(portal):
        yield portal
    if hasattr(integration_class, "testTearDown"):
        integration_class.testTearDown()


@pytest.fixture
def traverse():
    def func(data: dict | list, path: str) -> Any:
        func = None
        path = path.split(":")
        if len(path) == 2:
            func, path = path
        else:
            path = path[0]
        parts = [part for part in path.split("/") if part.strip()]
        value = data
        for part in parts:
            if isinstance(value, list):
                part = int(part)
            value = value[part]
        match func:
            # Add other functions here
            case "len":
                value = len(value)
            case "type":
                # This makes it easier to compare
                value = type(value).__name__
            case "is_uuid4":
                value = len(value) == 32 and value[15] == "4"
            case "keys":
                value = list(value.keys())
        return value

    return func


@pytest.fixture(scope="session")
def prepare_answers():
    def func() -> dict:
        return {
            "site_id": "site",
            "title": "Site",
            "description": "Site created with A CMS solution for public websites. Created by kitconcept.",  # noQA: E501
            "available_languages": ["en"],
            "default_language": "en",
            "portal_timezone": "Europe/Berlin",
            "setup_content": True,
            "authentication": {"provider": "internal"},
        }

    return func


@pytest.fixture(scope="session")
def answers(prepare_answers) -> dict:
    return prepare_answers()


@pytest.fixture(scope="session")
def create_site(distribution_name):
    def func(app, answers: dict) -> PloneSite:
        with api.env.adopt_user(SITE_OWNER_NAME):
            site = add_site(app, distribution=distribution_name, **answers)
        return site

    return func
