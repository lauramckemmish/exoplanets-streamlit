"""Authoritative catalogue for the learning experiences.

Change an experience's ``enabled`` value here to show or hide it throughout
the app. The landing page, sidebar and router all use this catalogue.
"""

EXPERIENCES = (
    {
        "name": "Is Our Solar System Normal?",
        "summary": "A fast-paced, facilitator-led CURIOUS experience. Compare planets, change graph scales and discuss why the planets we detect may not tell the whole story.",
        "enabled": True,
        "icon": "🪐",
        "app_experience": "Exoplanet Demographics",
        "pathway": "Is Our Solar System Normal?",
    },
    {
        "name": "Strange New Worlds",
        "summary": "A two-lesson classroom experience for exploring individual discoveries, growing datasets and the wonderfully varied planetary systems beyond our own.",
        "enabled": True,
        "icon": "✨",
        "app_experience": "Exoplanet Demographics",
        "pathway": "Strange New Worlds",
    },
    {
        "name": "The Planets We Haven't Found",
        "summary": "A two-lesson classroom experience that investigates how different ways of finding planets shape the evidence we have—and the planets we have not yet found.",
        "enabled": True,
        "icon": "🔭",
        "app_experience": "Exoplanet Demographics",
        "pathway": "The Planets We Haven't Found",
    },
    {
        "name": "Exoplanet Data Laboratory",
        "summary": "An open exploration space for inspecting the NASA dataset, choosing variables, building graphs and testing your own questions.",
        "enabled": True,
        "icon": "🔬",
        "app_experience": "Exoplanet Data Laboratory",
        "pathway": None,
    },
    {
        "name": "Find Your Perfect Planet",
        "summary": "A guided data-science mission: turn a planet idea into testable criteria, inspect candidate worlds and communicate uncertainty in your conclusion.",
        "enabled": True,
        "icon": "🌅",
        "app_experience": "Guided Tatooine Mission",
        "pathway": None,
    },
    {
        "name": "Planet Shopping Outside Our Solar System",
        "summary": "Use real exoplanet data to find your perfect planet.",
        "enabled": True,
        "icon": "🛒",
        "app_experience": "Planet Shopping Outside Our Solar System",
        "pathway": None,
    },
)


def experience_catalog(*, enabled_only: bool = True):
    """Return experience metadata, optionally including disabled experiences."""
    return tuple(
        dict(experience)
        for experience in EXPERIENCES
        if not enabled_only or experience["enabled"]
    )


def enabled_experience_names() -> tuple[str, ...]:
    """Return the public names shown in normal navigation."""
    return tuple(experience["name"] for experience in experience_catalog())


def get_experience(name: str, *, enabled_only: bool = True):
    """Return metadata for one public experience name, if it is available."""
    for experience in experience_catalog(enabled_only=enabled_only):
        if experience["name"] == name:
            return experience
    return None


def enabled_pathway_names() -> tuple[str, ...]:
    """Return enabled classroom/facilitated pathway names."""
    return tuple(
        experience["pathway"]
        for experience in experience_catalog()
        if experience["pathway"] is not None
    )


def is_enabled_app_experience(app_experience: str) -> bool:
    """Return whether an internal app route has an enabled public experience."""
    return any(
        experience["app_experience"] == app_experience
        for experience in experience_catalog()
    )
