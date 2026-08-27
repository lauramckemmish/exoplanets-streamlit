"""Planet Shopping Outside Our Solar System learning experience.

This module is intentionally a standalone shell. Future workshop content can
be added here without changing the existing Find Your Perfect Planet mission.
"""

import pandas as pd
import streamlit as st

from ui_helpers import scroll_to_top_if_requested, step_buttons, step_tabs

TITLE = "Planet Shopping Outside Our Solar System"
SUBTITLE = "Use real exoplanet data to find your perfect planet."

STAGE_LABELS = [
    "Where can we go?",
    "What's on your shopping list?",
    "Go planet shopping",
    "Meet your planet",
]

# These keys belong only to this experience. Do not reuse the mission or
# demographics keys: this workshop must remain independent while it is built.
_STAGE_KEY = "planet_shopping_stage"
_TAB_KEY = "planet_shopping_tab"
_SCROLL_KEY = "planet_shopping_scroll_to_top"


def render(data: pd.DataFrame) -> None:
    """Render the initial four-stage shell using the shared prepared dataset."""
    if _STAGE_KEY not in st.session_state:
        st.session_state[_STAGE_KEY] = 0

    stage = max(0, min(int(st.session_state[_STAGE_KEY]), len(STAGE_LABELS) - 1))
    st.title(TITLE)
    st.caption(SUBTITLE)
    st.caption(f"This experience is using the currently selected NASA exoplanet dataset ({len(data):,} planet records).")

    _, selected_stage = step_tabs(STAGE_LABELS, _TAB_KEY, stage)
    if selected_stage != stage:
        stage = selected_stage
        st.session_state[_STAGE_KEY] = stage
    scroll_to_top_if_requested(_SCROLL_KEY)

    st.subheader(STAGE_LABELS[stage])
    st.info(f"Placeholder for Stage {stage + 1}: {STAGE_LABELS[stage]}")

    step_buttons(
        STAGE_LABELS,
        _TAB_KEY,
        _STAGE_KEY,
        _SCROLL_KEY,
        stage,
        "planet_shopping",
    )
