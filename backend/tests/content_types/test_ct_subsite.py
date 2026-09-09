from kitconcept.website.content.subsite import ISubsite
from plone import api
from plone.dexterity.fti import DexterityFTI

import pytest


class TestContentTypeFTI:
    portal_type: str = "Subsite"

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_fti):
        self.portal = portal
        self.fti: DexterityFTI = get_fti(self.portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Subsite"),
            ("global_allow", True),
            ("filter_content_types", True),
            ("add_permission", "kitconcept.website.siteadminsonly"),
            ("klass", "kitconcept.website.content.subsite.Subsite"),
            ("schema", "kitconcept.website.content.subsite.ISubsite"),
            (
                "allowed_content_types",
                (
                    "Document",
                    "File",
                    "Image",
                    "Link",
                ),
            ),
        ],
    )
    def test_fti(self, attr: str, expected):
        """Test FTI values."""
        fti = self.fti

        assert isinstance(fti, DexterityFTI)
        assert getattr(fti, attr) == expected

    @pytest.mark.parametrize(
        "idx,behavior",
        enumerate((
            "plone.basic",
            "volto.preview_image_link",
            "volto.kicker",
            "plone.categorization",
            "plone.publication",
            "plone.ownership",
            "plone.shortname",
            "volto.navtitle",
            "plone.excludefromnavigation",
            "volto.blocks",
            "voltolighttheme.header",
            "voltolighttheme.theme",
            "voltolighttheme.footer",
            "kitconcept.footer",
            "plone.constraintypes",
            "plone.namefromtitle",
            "plone.versioning",
            "plone.locking",
            "plone.translatable",
            "plone.navigationroot",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior


class TestContentTypeSubsite:
    portal_type: str = "Subsite"

    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.portal = portal

    def test_create(self):
        """A Subsite can be created and is a navigation root."""
        from plone.base.interfaces import INavigationRoot

        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(
                container=self.portal,
                type=self.portal_type,
                title="My Subsite",
                id="my-subsite",
            )

        assert content.portal_type == self.portal_type
        assert ISubsite.providedBy(content)
        # Own navigation and breadcrumbs starting on the subsite are driven
        # by the plone.navigationroot behavior.
        assert INavigationRoot.providedBy(content)
