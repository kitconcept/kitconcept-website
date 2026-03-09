from kitconcept.website import PACKAGE_NAME


class TestSetupInstall:
    profile_id: str = f"{PACKAGE_NAME}:default"

    def test_addon_installed(self, installer):
        """Test if kitconcept.website is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from kitconcept.website.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers
