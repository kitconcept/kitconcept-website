from kitconcept.website import _
from kitconcept.website.interfaces import IBrowserLayer
from plone.registry.interfaces import IRegistry
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.restapi.interfaces import ISiteEndpointExpander
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary


# These are the modules supported in 
# https://github.com/kitconcept/volto-dsgvo-banner/blob/main/packages/volto-dsgvo-banner/src/components/Block/View.jsx
DSGVO_MODULES = SimpleVocabulary.fromValues([
    'tracking',
    'youtube',
    'facebook',
    'google',
    'vimeo',
    'twitter',
])


class IDSGVOSettings(Interface):
    """Settings for @kitconcept/volto-dsgvo-banner"""

    show_banner = schema.Bool(
        title=_("label_dsgvo_show_banner", default="Show GDPR banner on first visit"),
        description=_("help_dsgvo_show_banner",
            default="If true, the cookie consent banner will be shown immediately. "
            "If false, users will be prompted to accept cookies only in the context "
            "of blocks where they are needed.",
        ),
        default=True,
    )

    modules = schema.List(
        title=_("label_dsgvo_modules", default="Show privacy settings for"),
        description=_("help_dsgvo_modules",
            default="List of 3rd-party sites to be shown in privacy preferences.",
        ),
        value_type=schema.Choice(
            vocabulary=DSGVO_MODULES,
        ),
        default=['tracking', 'youtube', 'facebook', 'google'],
        required=True,
    )


@adapter(Interface, Interface)
class DSGVOControlpanel(RegistryConfigletPanel):
    """REST API control panel for DSGVO settings."""
    schema = IDSGVOSettings
    configlet_id = "dsgvo-settings"
    configlet_category_id = "plone-general"
    schema_prefix = "kitconcept.website.dsgvo"


@adapter(Interface, IBrowserLayer)
@implementer(ISiteEndpointExpander)
class DSGVOSiteEndpointExpander:
    """Add DSGVO settings to the @site endpoint."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, data):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IDSGVOSettings, prefix="kitconcept.website.dsgvo", check=False)
        try:
            data["kitconcept.website.dsgvo"] = {
                "show_banner": settings.show_banner,
                "modules": settings.modules,
            }
        except AttributeError:
            # Probably the upgrade step wasn't run yet, so the records don't exist.
            pass
