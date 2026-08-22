"""Small, reusable presentation helpers shared by the teaching experiences."""

import streamlit as st
import streamlit.components.v1 as components


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


def step_navigation_bar(labels: list[str], key: str) -> str:
    """Render a compact tab-like step bar."""
    st.markdown(
        """
        <style>
        div[data-testid="stRadio"] div[role="radiogroup"] {gap: 0.2rem; border-bottom: 1px solid rgba(128, 128, 128, 0.35); flex-wrap: wrap;}
        div[data-testid="stRadio"] div[role="radio"] {border-radius: 0; border: 0; border-bottom: 3px solid transparent; padding: 0.35rem 0.55rem 0.45rem; margin-bottom: -1px;}
        div[data-testid="stRadio"] div[role="radio"] > div:first-child {display: none;}
        div[data-testid="stRadio"] div[role="radio"][aria-checked="true"] {border-bottom-color: rgb(255, 75, 75); color: rgb(255, 75, 75);}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return st.radio("Go to a step", labels, key=key, horizontal=True, label_visibility="collapsed")


def select_tab_step(tab_key: str, labels: list[str], step_key: str, scroll_key: str, step: int) -> None:
    st.session_state[tab_key] = labels[step]
    st.session_state[step_key] = step
    st.session_state[scroll_key] = True


def step_tabs(labels: list[str], key: str, current_step: int):
    current_step = max(0, min(current_step, len(labels) - 1))
    if st.session_state.get(key) not in labels:
        st.session_state[key] = labels[current_step]
    tabs = st.tabs(labels, default=st.session_state[key], key=key, on_change="rerun")
    return tabs, labels.index(st.session_state.get(key, labels[current_step]))


def step_buttons(labels: list[str], tab_key: str, step_key: str, scroll_key: str, step: int, button_prefix: str) -> None:
    back, spacer, next_step = st.columns([1, 4, 1])
    with back:
        if step > 0:
            st.button("← Back", use_container_width=True, key=f"{button_prefix}_back", on_click=select_tab_step, args=(tab_key, labels, step_key, scroll_key, step - 1))
    with next_step:
        if step < len(labels) - 1:
            st.button("Continue →", type="primary", use_container_width=True, key=f"{button_prefix}_continue", on_click=select_tab_step, args=(tab_key, labels, step_key, scroll_key, step + 1))


def scroll_to_top_if_requested(key: str) -> None:
    if not st.session_state.pop(key, False):
        return
    components.html(
        """
        <script>
            const parentDocument = window.parent.document;
            const scrollContainer = parentDocument.querySelector('[data-testid="stAppViewContainer"]') || parentDocument.querySelector('section.main');
            if (scrollContainer) scrollContainer.scrollTo({top: 0, left: 0, behavior: 'instant'});
            window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
        </script>
        """,
        height=0,
    )
