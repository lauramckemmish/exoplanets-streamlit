"""Small, reusable presentation helpers shared by the teaching experiences."""

import streamlit as st


def key_idea(text: str, evidence: str) -> None:
    """Close a step with a student-friendly science idea and observation prompt."""
    st.success(f"**Big idea:** {text}\n\n**Look for:** {evidence}")


def graph_guide(*instructions: str) -> None:
    st.info(
        "**How to read this graph**\n\n"
        + "\n".join(f"- {instruction}" for instruction in instructions)
    )


def graph_questions(find: str, compare: str) -> None:
    st.markdown("### Find and explore")
    st.markdown(f"1. **Find:** {find}\n2. **Compare:** {compare}")


def data_detective_challenge() -> None:
    """Give students focused, optional ways to read the combined planet graph."""
    st.markdown("### Data detective challenge")
    st.write("**Everyone:** Find Earth’s pink diamond. Are there blue points nearby? Does that prove we have found another Earth?")
    st.caption(
        "Hover over a blue point to find its name and measurements. This graph shows mass and orbital distance, "
        "but not everything we would need to call a planet Earth-like."
    )
    st.markdown("**Then choose one further challenge:**")
    st.markdown(
        "1. **Find an extreme:** Which plotted exoplanet is closest to its host star **or** has the greatest mass?\n"
        "2. **Find a small neighbour:** Choose Mercury or Mars. Are there blue points near it?\n"
        "3. **Find an outer neighbour:** Look near Uranus and Neptune. Are there blue points with similar mass and orbital distance?\n"
        "4. **Describe a typical detected planet:** What mass and orbital distance seem common **in this detected dataset**?"
    )
