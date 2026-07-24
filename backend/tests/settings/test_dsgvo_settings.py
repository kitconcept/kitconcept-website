class TestDSGVOSettings:
    def test_dsgvo_controlpanel(self, manager_request):
        resp = manager_request.get("/@controlpanels/dsgvo-settings")
        assert resp.status_code == 200
        properties = resp.json()["schema"]["properties"]
        assert "show_banner" in properties
        assert "modules" in properties
        assert "tracker" in properties
        assert "tracker_options" in properties
        assert "privacy_url" in properties

    def test_dsgvo_settings_in_site_endpoint(self, anon_request):
        resp = anon_request.get("/@site")
        assert resp.status_code == 200
        data = resp.json()
        assert "kitconcept.website.dsgvo" in data
        assert data["kitconcept.website.dsgvo"]["show_banner"] is True
        assert data["kitconcept.website.dsgvo"]["modules"] == [
            "tracking",
            "youtube",
            "facebook",
            "google",
        ]
        assert data["kitconcept.website.dsgvo"]["tracker"] is None
        assert data["kitconcept.website.dsgvo"]["tracker_options"] is None
        assert data["kitconcept.website.dsgvo"]["privacy_url"] is None
