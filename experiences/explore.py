"""Lightweight shells for independent Explore resources.

These resources are not guided classroom experiences. Detailed scientific
content can be added here independently as each resource is developed.
"""

import streamlit as st


def render_placeholder(resource: dict[str, str]) -> None:
    """Render a deliberately minimal shell for an Explore resource in development."""
    st.title(resource["name"])
    st.caption(resource["summary"])
    st.info("This Explore resource is being prepared.")
