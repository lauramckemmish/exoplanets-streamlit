"""Routing for the named exoplanet-demographics experiences."""

import streamlit as st


def reset_navigation() -> None:
    """Start a selected demographics pathway with independent step state."""
    st.session_state["demographics_part"] = 0
    st.session_state["curious_part"] = 0
    st.session_state.pop("demographics_step_selector", None)
    st.session_state.pop("curious_step_selector", None)
    st.session_state["demographics_scroll_to_top"] = True
    st.session_state["curious_scroll_to_top"] = True


def select_experience(name: str) -> None:
    st.session_state["experience"] = name


def select_demographics_pathway(pathway: str) -> None:
    st.session_state["demographics_pathway"] = pathway
    reset_navigation()
    st.session_state["demographics_started"] = True
    st.session_state["experience"] = "Exoplanet Demographics"


def open_experience(name: str, facilitated_pathway: str, stage4_pathway: str, stage5_pathway: str) -> None:
    """Open an experience from the Introduction catalogue."""
    if name in {facilitated_pathway, stage4_pathway, stage5_pathway}:
        select_demographics_pathway(name)
    elif name == "Find Your Perfect Planet":
        select_experience("Guided Tatooine Mission")
    else:
        select_experience(name)


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


def render_pathway(pathway, data, facilitated_pathway, stage4_pathway, stage5_pathway, curious_render, stage4_render, stage5_render, curious_implementation, classroom_implementation):
    """Dispatch a selected pathway to its independent experience entry point."""
    if pathway == facilitated_pathway:
        return curious_render(data, curious_implementation)
    if pathway == stage4_pathway:
        return stage4_render(data, classroom_implementation)
    return stage5_render(data, classroom_implementation)


def render_demographics_shell(data, demographics_started, pathway, title, facilitated_pathway, stage4_pathway, stage5_pathway, landing, curious_render, stage4_render, stage5_render, curious_implementation, classroom_implementation):
    """Render the common demographics heading, toggle and pathway dispatch."""
    if not demographics_started:
        return landing(data)
    pathway = normalise_pathway(pathway, facilitated_pathway, stage4_pathway, stage5_pathway)
    if pathway is None:
        st.session_state["experience"] = "Introduction"
        st.rerun()
    st.session_state["demographics_pathway"] = pathway
    heading, activity_controls = st.columns([4, 2])
    with heading:
        st.title(pathway)
        st.markdown(f"*{title}*")
    with activity_controls:
        st.toggle("Teacher view", key="demographics_teacher_view", help="Show learning purpose, facilitation guidance and syllabus connections within each step.")
    return render_pathway(pathway, data, facilitated_pathway, stage4_pathway, stage5_pathway, curious_render, stage4_render, stage5_render, curious_implementation, classroom_implementation)
