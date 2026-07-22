from kitconcept.website.upgrades import remove_preview_image_behavior
from plone.base.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return []


def post_install(setup_tool):
    remove_preview_image_behavior(setup_tool)
