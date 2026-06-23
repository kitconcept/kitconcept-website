from kitconcept.core.testing.layers import kitconceptDistributionFixture
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE


DEFAULT_ANSWERS = {
    "site_id": "plone",
    "title": "Site",
    "description": "Site created with A CMS solution for public websites. Created by kitconcept.",  # noQA: E501
    "available_languages": ["en"],
    "default_language": "en",
    "portal_timezone": "Europe/Berlin",
    "setup_content": True,
    "authentication": {"provider": "internal"},
}


class BaseFixture(kitconceptDistributionFixture):
    PACKAGE_NAME = "kitconcept.website"
    sites = (("kitconcept-website", DEFAULT_ANSWERS),)
    internal_packages: tuple[str, ...] = ("kitconcept.website",)


BASE_FIXTURE = BaseFixture()


class Layer(PloneSandboxLayer):
    defaultBases = (BASE_FIXTURE,)


FIXTURE = Layer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="kitconcept.websiteLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="kitconcept.websiteLayer:FunctionalTesting",
)
