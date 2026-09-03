from plone import api
from plone.app.testing.interfaces import SITE_OWNER_NAME

import pytest


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture()
def roles_permission():
    def func(context, permission: str) -> list[str]:
        report = context.rolesOfPermission(permission)
        return [role["name"] for role in report if role["selected"]]

    return func


class TestSiteCreation:
    @pytest.fixture(autouse=True)
    def _setup(self, app, create_site, answers):
        self.site = create_site(app, answers)

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
            ("/qa", "QA", "Document", "published"),
        ],
    )
    def test_content_created(self, path, title, portal_type, review_state):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.get(path=path)
        assert content.title == title
        assert content.portal_type == portal_type
        assert api.content.get_state(content) == review_state

    def test_feature_block_examples_not_created(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.get(path="/features/block")
        assert content is None

    def test_qa_image_fixture_created(self):
        with api.env.adopt_user(SITE_OWNER_NAME):
            content = api.content.get(path="/images/image-light")
        assert content.title == "Image - Light"
        assert content.portal_type == "Image"
        assert content.image.filename == "image-light.jpg"
        assert content.image.getSize() == 475285
        assert content.UID() == "eec82559bf3242a6be4d43bc2096f399"
        resolved = api.content.get(UID=content.UID())
        assert resolved.getPhysicalPath() == content.getPhysicalPath()

    def test_teaser_person_fixtures_resolve(self):
        person_uids = (
            "c71a61066533455db656f0ac93044401",
            "29619a2394d7421980fabaa99b742eda",
            "37d87d573b4448369afb431a0eb1f728",
            "4de23606a34b4db284c6125a94ca1c41",
            "34d45ae4d36c4fa1a678358dd5320609",
            "059feee144a44bf88a3b38fbe9deca65",
            "1cdfd0c5a337469f8c41ade1fba5274d",
            "27ae32819bc64e4fa280efc1a1d5514d",
            "2e17746a030b479a918afefc50d5ff4c",
            "95a19878c3b34b0584db198524b0b58b",
        )

        with api.env.adopt_user(SITE_OWNER_NAME):
            people = [api.content.get(UID=uid) for uid in person_uids]

        assert all(person is not None for person in people)
        assert all(person.portal_type == "Person" for person in people)

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
