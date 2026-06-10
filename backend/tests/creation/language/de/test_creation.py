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
            ["plone.available_languages", ["de"]],
            ["plone.default_language", "de"],
        ],
    )
    def test_registry_entries(self, key, expected):
        assert api.portal.get_registry_record(key) == expected

    def test_plone_app_multilingual_not_installed(self):
        st: SetupTool = api.portal.get_tool("portal_setup")
        installation_date = st.getProfileImportDate(
            "profile-plone.app.multilingual:default"
        )
        assert installation_date is None
