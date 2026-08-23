"""Find Tatooine experience entry point.

The implementation is injected by ``app.py`` so this module does not import
the Streamlit application back into itself (which would create a cycle).
"""

STEP_LABELS = [
    "Briefing", "Archive", "Evidence", "Two suns", "Three planets",
    "Earth-sized", "Compare", "Report",
]
STEP_COUNT = len(STEP_LABELS)


def render(data, presenter_mode, implementation):
    return implementation(data, presenter_mode)
