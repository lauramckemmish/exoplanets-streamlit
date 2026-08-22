"""Routing for the named exoplanet-demographics experiences."""


def render_pathway(pathway, data, facilitated_pathway, stage4_pathway, curious_render, stage4_render, stage5_render, curious_implementation, classroom_implementation):
    """Dispatch a selected pathway to its independent experience entry point."""
    if pathway == facilitated_pathway:
        return curious_render(data, curious_implementation)
    if pathway == stage4_pathway:
        return stage4_render(data, classroom_implementation)
    return stage5_render(data, classroom_implementation)
