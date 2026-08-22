"""Routing for the named exoplanet-demographics experiences."""


def render_pathway(pathway, data, facilitated_pathway, stage4_pathway, curious_render, stage4_render, stage5_render):
    """Dispatch a selected pathway to its independent experience entry point."""
    if pathway == facilitated_pathway:
        return curious_render(data)
    if pathway == stage4_pathway:
        return stage4_render(data)
    return stage5_render(data)
