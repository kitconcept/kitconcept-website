from plone import api
from Products.GenericSetup.tool import SetupTool

import pytest


class TestSiteCreation:
    @pytest.fixture(autouse=True)
    def _setup(self, portal):
        self.site = portal

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.available_languages", ["de", "en"]],
            ["plone.default_language", "de"],
        ],
    )
    def test_registry_entries(self, key, expected):
        assert api.portal.get_registry_record(key) == expected

    def test_plone_app_multilingual_installed(self):
        st: SetupTool = api.portal.get_tool("portal_setup")
        installed_version = st.getLastVersionForProfile(
            "profile-plone.app.multilingual:default"
        )
        assert installed_version != "unknown"
