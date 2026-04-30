from plone import api

import pytest


class TestSiteCreation:
    @pytest.fixture(autouse=True)
    def _create_site(self, create_site, answers):
        self.site = create_site(answers)

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.default_language", "de"],
        ],
    )
    def test_registry_entries(self, key, expected):
        assert api.portal.get_registry_record(key) == expected
