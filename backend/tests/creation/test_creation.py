from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME

import pytest


@pytest.fixture()
def roles_permission():
    def func(context, permission: str) -> list[str]:
        report = context.rolesOfPermission(permission)
        return [role["name"] for role in report if role["selected"]]

    return func


class TestSiteCreation:
    @pytest.fixture(autouse=True)
    def _create_site(self, create_site, answers):
        self.site = create_site(answers)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["id", "site"],
        ],
    )
    def test_properties(self, attr, expected):
        site = self.site
        assert getattr(site, attr) == expected

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.site_title", "Site"],
        ],
    )
    def test_registry_entries(self, key, expected):
        assert api.portal.get_registry_record(key) == expected

    @pytest.mark.parametrize(
        "path,title,portal_type,review_state",
        [
            ("/about", "About", "Document", "published"),
        ],
    )
    def test_content_created(self, path, title, portal_type, review_state):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.get(path=path)
        assert content.title == title
        assert content.portal_type == portal_type
        assert api.content.get_state(content) == review_state

    @pytest.mark.parametrize(
        "path,permission,role,expected",
        [
            ("/about", "View", "Anonymous", True),
        ],
    )
    def test_content_permission_role(
        self, roles_permission, path, permission, role, expected
    ):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.get(path=path)
        roles = roles_permission(content, permission)
        assert (role in roles) is expected
