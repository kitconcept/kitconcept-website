from kitconcept.website import logger
from kitconcept.website.utils import creation as utils
from kitconcept.website.utils.authentication import setup_authentication
from plone import api
from plone.distribution.core import Distribution
from plone.distribution.handler import default_handler
from plone.distribution.utils.data import convert_data_uri_to_b64
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.WorkflowTool import WorkflowTool


def pre_handler(answers: dict) -> dict:
    """Process answers."""
    # Goal here is to also handle cases where the answers
    # only contain default_language but not available_languages
    available_languages = answers.get("available_languages")
    default_language = answers.get("default_language")
    if available_languages is None and default_language:
        answers["available_languages"] = [default_language]
    elif available_languages and default_language not in available_languages:
        answers["default_language"] = available_languages[0]
    return answers


def handler(distribution: Distribution, site: PloneSite, answers: dict) -> PloneSite:
    """Handler to create a new site."""
    return default_handler(distribution, site, answers)


def post_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """Run after site creation."""
    name = distribution.name
    logger.info(f"{site.id}: Running {name} post_handler")
    # Update security
    wf_tool: WorkflowTool = api.portal.get_tool("portal_workflow")
    wf_tool.updateRoleMappings()

    # This should be fixed on plone.distribution
    title = answers.get("title", site.title)
    description = answers.get("description", site.description)
    available_languages = answers.get("available_languages")
    default_language = answers.get("default_language")
    registry_data = {
        "plone.available_languages": available_languages,
        "plone.default_language": default_language,
        "plone.email_from_name": title,
        "plone.site_title": title,
    }
    site.title = title
    site.description = description
    if raw_logo := answers.get("site_logo"):
        logo = convert_data_uri_to_b64(raw_logo)
        logger.info(f"{site.id}: Set logo")
        registry_data["plone.site_logo"] = logo
        utils.set_site_logo(raw_logo, site)

    # Update registry
    utils.update_registry(registry_data)
    # Install multilingual support if more than one language is available
    utils.multilingual_support(site, available_languages)
    # Configure authentication
    if auth_answers := answers.get("authentication"):
        logger.info(f"{site.id}: Processing authentication options")
        setup_authentication(auth_answers)
    return site
