from Acquisition import aq_parent
from collections.abc import Generator
from Products.CMFPlone.Portal import PloneSite

import pytest


@pytest.fixture(scope="class")
def portal(portal_class, create_site, answers) -> Generator[PloneSite, None, None]:
    app = aq_parent(portal_class)
    site = create_site(app=app, answers=answers)
    yield site
