"""Shared step-state and navigation mechanics for the classroom pathways."""

import streamlit as st

from ui_helpers import scroll_to_top_if_requested, step_tabs


def select_step(step_labels: list[str], part_count: int) -> int:
    """Render classroom step tabs and return the selected step index."""
    if "demographics_part" not in st.session_state:
        st.session_state["demographics_part"] = 0
    part = max(0, min(int(st.session_state["demographics_part"]), part_count - 1))
    _, selected_part = step_tabs(step_labels, "demographics_step_selector", part)
    if selected_part != part:
        part = selected_part
        st.session_state["demographics_part"] = part
        st.session_state["demographics_scroll_to_top"] = True
    scroll_to_top_if_requested("demographics_scroll_to_top")
    return part
