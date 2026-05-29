from kitconcept.core.testing.layers import kitconceptDistributionFixture
from plone.app.robotframework.autologin import AutoLogin
from plone.app.robotframework.content import Content
from plone.app.robotframework.genericsetup import GenericSetup
from plone.app.robotframework.i18n import I18N
from plone.app.robotframework.mailhost import MockMailHost
from plone.app.robotframework.quickinstaller import QuickInstaller
from plone.app.robotframework.remote import RemoteLibraryLayer
from plone.app.robotframework.server import Zope2ServerRemote
from plone.app.robotframework.testing import MockMailHostLayer as BaseMailLayer
from plone.app.robotframework.testing import PloneRobotFixture
from plone.app.robotframework.testing import WSGI_SERVER_SINGLE_THREADED_FIXTURE
from plone.app.robotframework.users import Users
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.app.testing.interfaces import TEST_USER_PASSWORD
from plone.app.testing.interfaces import TEST_USER_ROLES
from plone.testing import zope
from plone.testing.zope import WSGI_SERVER_FIXTURE
from zope.globalrequest import setRequest


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
    internal_packages: tuple[str, ...] = (
        "plone.restapi",
        "plone.volto",
        "kitconcept.core",
        "kitconcept.website",
    )

    def setUpDefaultContent(self, app):
        """Create a Plone site using plone.distribution."""
        from kitconcept.core.factory import add_site

        # Create the owner user and "log in" so that the site object gets
        # the right ownership information
        app["acl_users"].userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], []
        )

        setRequest(app.REQUEST)
        zope.login(app["acl_users"], SITE_OWNER_NAME)
        sites = self.sites
        for distribution_name, answers in sites:
            site_id = answers["site_id"]
            # Create Plone site
            add_site(
                app,
                extension_ids=self.extensionProfiles,
                distribution=distribution_name,
                **answers,
            )

            # Create the test user. (Plone)PAS does not have an API to create a
            # user with different userid and login name, so we call the plugin
            # directly.
            pas = app[site_id]["acl_users"]
            pas.source_users.addUser(TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD)
            for role in TEST_USER_ROLES:
                pas.portal_role_manager.doAssignRoleToPrincipal(TEST_USER_ID, role)

        # Log out again
        zope.logout()
        setRequest(None)


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


ANSWERS_CONTENT = {
    **DEFAULT_ANSWERS,
    "setup_content": False,
}


class ContentFixture(BaseFixture):
    sites = (("kitconcept-website", ANSWERS_CONTENT),)


CONTENT_FIXTURE = ContentFixture()


class MockMailHostLayer(BaseMailLayer):
    defaultBases = (CONTENT_FIXTURE,)


MOCK_MAILHOST_FIXTURE = MockMailHostLayer()


class RobotFixture(PloneRobotFixture):
    """Acceptance testing fixture, using robot framework, for kitconcept.website."""

    defaultBases = (MOCK_MAILHOST_FIXTURE,)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)


ROBOT_FIXTURE = RobotFixture()

REMOTE_LIBRARY_BUNDLE_FIXTURE = RemoteLibraryLayer(
    bases=(CONTENT_FIXTURE,),
    libraries=(
        AutoLogin,
        QuickInstaller,
        GenericSetup,
        Content,
        Users,
        I18N,
        MockMailHost,
        Zope2ServerRemote,
    ),
    name="RemoteLibraryBundle:RobotRemote",
)

ROBOT_TESTING = FunctionalTesting(
    bases=(
        ROBOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_SINGLE_THREADED_FIXTURE,
    ),
    name="Website:Robot",
)


ANSWERS_EXAMPLE_CONTENT = {
    **DEFAULT_ANSWERS,
    "setup_content": True,
}


class ExampleContentFixture(BaseFixture):
    sites = (("kitconcept-website", ANSWERS_EXAMPLE_CONTENT),)


EXAMPLE_CONTENT_FIXTURE = ExampleContentFixture()


class A11YMockMailHostLayer(BaseMailLayer):
    defaultBases = (EXAMPLE_CONTENT_FIXTURE,)


A11Y_MOCK_MAILHOST_FIXTURE = A11YMockMailHostLayer()


class A11YFixture(PloneRobotFixture):
    """Accessibility testing fixture, using robot framework, for kitconcept.website."""

    defaultBases = (A11Y_MOCK_MAILHOST_FIXTURE,)

    def setUpPloneSite(self, portal):
        super().setUpPloneSite(portal)


A11Y_FIXTURE = A11YFixture()

A11Y_REMOTE_LIBRARY_BUNDLE_FIXTURE = RemoteLibraryLayer(
    bases=(EXAMPLE_CONTENT_FIXTURE,),
    libraries=(
        AutoLogin,
        QuickInstaller,
        GenericSetup,
        Content,
        Users,
        I18N,
        MockMailHost,
        Zope2ServerRemote,
    ),
    name="RemoteLibraryBundle:A11YRemote",
)

A11Y_TESTING = FunctionalTesting(
    bases=(
        A11Y_FIXTURE,
        A11Y_REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_SINGLE_THREADED_FIXTURE,
    ),
    name="Website:A11Y",
)
