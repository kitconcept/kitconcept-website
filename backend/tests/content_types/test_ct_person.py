from plone.dexterity.fti import DexterityFTI

import pytest


class TestContentTypeFTI:
    portal_type: str = "Person"

    @pytest.fixture(autouse=True)
    def _setup(self, portal, get_fti):
        self.portal = portal
        self.fti: DexterityFTI = get_fti(self.portal_type)

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ("title", "Person"),
            ("klass", "collective.person.content.person.Person"),
            ("global_allow", True),
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
            "kitconcept.core.person_image",
            "volto.kicker",
            "collective.person.person",
            "kitconcept.core.biography",
            "collective.contact_behaviors.contact_info",
            "kitconcept.core.additional_contact_info",
            "plone.namefromtitle",
            "plone.shortname",
            "volto.navtitle",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
            "plone.locking",
            "plone.translatable",
        )),
    )
    def test_behaviors(self, idx: int, behavior: str):
        """Test behaviors are present and in correct order."""
        assert self.fti.behaviors[idx] == behavior
