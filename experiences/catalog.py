"""Authoritative catalogue for public Experiences and Explore resources.

Change a destination's ``enabled`` value here to show or hide it throughout
the app. The landing page, sidebar and router all use these catalogues.
"""

EXPERIENCES = (
    {
        "name": "Is Our Solar System Normal?",
        "nav_label": "Is Our Solar System Normal?",
        "summary": "A fast-paced, facilitator-led CURIOUS experience. Compare planets, change graph scales and discuss why the planets we detect may not tell the whole story.",
        "enabled": False,
        "icon": "🪐",
        "app_experience": "Exoplanet Demographics",
        "pathway": "Is Our Solar System Normal?",
    },
    {
        "name": "Strange New Worlds",
        "nav_label": "Strange New Worlds",
        "summary": "A two-lesson classroom experience for exploring individual discoveries, growing datasets and the wonderfully varied planetary systems beyond our own.",
        "enabled": False,
        "icon": "✨",
        "app_experience": "Exoplanet Demographics",
        "pathway": "Strange New Worlds",
    },
    {
        "name": "The Planets We Haven't Found",
        "nav_label": "Planets We Haven't Found",
        "summary": "A two-lesson classroom experience that investigates how different ways of finding planets shape the evidence we have—and the planets we have not yet found.",
        "enabled": False,
        "icon": "🔭",
        "app_experience": "Exoplanet Demographics",
        "pathway": "The Planets We Haven't Found",
    },
    {
        "name": "Find Your Perfect Planet",
        "nav_label": "Find Your Perfect Planet",
        "summary": "A guided data-science mission: turn a planet idea into testable criteria, inspect candidate worlds and communicate uncertainty in your conclusion.",
        "enabled": False,
        "icon": "🌅",
        "app_experience": "Guided Tatooine Mission",
        "pathway": None,
    },
    {
        "name": "Planet Shopping Outside Our Solar System",
        "nav_label": "Planet Shopping",
        "summary": "Use real exoplanet data to find your perfect planet.",
        "card_title": "Planet Shopping",
        "card_summary": None,
        "card_button_label": "Start →",
        "enabled": True,
        "icon": "🛒",
        "thumbnail": "assets/planet-shopping-thumbnail.png",
        "app_experience": "Planet Shopping Outside Our Solar System",
        "pathway": None,
    },
)


EXPLORE_RESOURCES = (
    {
        "name": "How We Found Other Worlds",
        "nav_label": "Finding Other Worlds",
        "summary": "Explore how we went from knowing one planetary system to discovering thousands of worlds.",
        "enabled": False,
        "icon": "🛰️",
        "app_experience": "Explore: How We Found Other Worlds",
    },
    {
        "name": "How Do We Find a Planet We Can't See?",
        "nav_label": "Finding Planets We Can't See",
        "summary": "Explore the techniques astronomers use to detect planets around other stars.",
        "enabled": False,
        "icon": "🔭",
        "app_experience": "Explore: How Do We Find a Planet We Can't See?",
    },
    {
        "name": "Exoplanet Data Lab",
        "nav_label": "Exoplanet Data Lab",
        "summary": "Explore the exoplanet catalogue yourself.",
        "enabled": True,
        "icon": "🔬",
        "app_experience": "Exoplanet Data Laboratory",
    },
)


def experience_catalog(*, enabled_only: bool = True):
    """Return experience metadata, optionally including disabled experiences."""
    return tuple(
        dict(experience)
        for experience in EXPERIENCES
        if not enabled_only or experience["enabled"]
    )


def explore_catalog(*, enabled_only: bool = True):
    """Return Explore resource metadata, optionally including disabled entries."""
    return tuple(
        dict(resource)
        for resource in EXPLORE_RESOURCES
        if not enabled_only or resource["enabled"]
    )


def enabled_experience_names() -> tuple[str, ...]:
    """Return the public names shown in normal navigation."""
    return tuple(experience["name"] for experience in experience_catalog())


def enabled_explore_resource_names() -> tuple[str, ...]:
    """Return the public Explore names shown in normal navigation."""
    return tuple(resource["name"] for resource in explore_catalog())


def get_experience(name: str, *, enabled_only: bool = True):
    """Return metadata for one public experience name, if it is available."""
    for experience in experience_catalog(enabled_only=enabled_only):
        if experience["name"] == name:
            return experience
    return None


def get_explore_resource(name: str, *, enabled_only: bool = True):
    """Return one Explore resource by its public name, if it is available."""
    for resource in explore_catalog(enabled_only=enabled_only):
        if resource["name"] == name:
            return resource
    return None


def get_explore_resource_for_route(app_experience: str, *, enabled_only: bool = True):
    """Return the enabled Explore resource associated with an internal route."""
    for resource in explore_catalog(enabled_only=enabled_only):
        if resource["app_experience"] == app_experience:
            return resource
    return None


def enabled_app_experience_names() -> tuple[str, ...]:
    """Return all enabled internal routes from guided and Explore collections."""
    return tuple(
        dict.fromkeys(
            entry["app_experience"]
            for entry in (*experience_catalog(), *explore_catalog())
        )
    )


def enabled_pathway_names() -> tuple[str, ...]:
    """Return enabled classroom/facilitated pathway names."""
    return tuple(
        experience["pathway"]
        for experience in experience_catalog()
        if experience["pathway"] is not None
    )


def is_enabled_app_experience(app_experience: str) -> bool:
    """Return whether an internal app route has an enabled public experience."""
    return app_experience in enabled_app_experience_names()
