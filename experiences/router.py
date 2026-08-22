"""Routing for the named exoplanet-demographics experiences."""


def normalise_pathway(pathway, facilitated_pathway, stage4_pathway, stage5_pathway):
    """Return a current pathway name for current or legacy session values."""
    migrations = {
        "CURIOUS workshop": facilitated_pathway,
        "50-minute facilitated experience": facilitated_pathway,
        "Year 8 classroom": stage4_pathway,
        "Year 10 classroom": stage5_pathway,
    }
    pathway = migrations.get(pathway, pathway)
    valid = {facilitated_pathway, stage4_pathway, stage5_pathway}
    return pathway if pathway in valid else None


def render_pathway(pathway, data, facilitated_pathway, stage4_pathway, curious_render, stage4_render, stage5_render, curious_implementation, classroom_implementation):
    """Dispatch a selected pathway to its independent experience entry point."""
    if pathway == facilitated_pathway:
        return curious_render(data, curious_implementation)
    if pathway == stage4_pathway:
        return stage4_render(data, classroom_implementation)
    return stage5_render(data, classroom_implementation)
