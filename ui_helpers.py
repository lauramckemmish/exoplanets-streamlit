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


def log_scale_reveal(prompt: str, key: str) -> bool:
    """Create a deliberate, persistent reveal before showing a log–log graph."""
    st.markdown(f"### Pause and predict\n{prompt}")
    if key not in st.session_state:
        st.session_state[key] = False
    if not st.session_state[key]:
        st.button(
            "Reveal a new way to view the same data →",
            type="primary",
            key=f"{key}_button",
            on_click=lambda: st.session_state.__setitem__(key, True),
        )
        return False
    st.success(
        "**Same planets. Same variables. Different spacing.** A log scale spreads out the small values "
        "while keeping the giant planets on the same graph."
    )
    st.write(
        "The variables do not change: the graph still shows planet mass and orbital distance. On a log scale, "
        "equal spaces represent multiplication. For example, the gap from **0.1 to 1** is the same size as "
        "the gap from **1 to 10**. You do not need to calculate logarithms to read the graph."
    )
    return True


def response_box(step: int, prompt: str, sentence_starters: str) -> None:
    pathway = st.session_state.get("demographics_pathway", "classroom")
    st.markdown(f"### Discuss your conclusion\n{prompt}")
    st.caption(f"**Sentence starters:** {sentence_starters}")
    st.text_area(
        "Write your explanation",
        key=f"demographics_response_{pathway}_{step}",
        height=100,
        label_visibility="collapsed",
    )


def learn_more_prompt(key_prefix: str) -> None:
    st.markdown("### What would you most like to find out next?")
    st.write(
        "Exoplanets connect to many different questions. Choose something that interested you, then turn it into a "
        "question you could investigate."
    )
    st.markdown(
        "- **Worlds and space:** planetary formation, unusual systems, telescopes and future missions\n"
        "- **Life beyond Earth:** astrobiology, atmospheres, molecules, spectra and possible signs of life\n"
        "- **People and ideas:** aliens, philosophy, culture, media, politics and how humanity might respond to a discovery"
    )
    st.text_area("My learn-more question", key=f"{key_prefix}_learn_more", height=90, placeholder="I would like to find out…")
    if st.session_state.get("demographics_teacher_view", False):
        with st.expander("Teacher guide: helping students follow their interest"):
            st.markdown(
                "These are optional engagement routes, not additional required curriculum. Invite students to choose "
                "one question and identify useful search terms or an appropriate source. Possible prompts include:\n\n"
                "- How do planets and planetary systems form?\n"
                "- How can a spectrum reveal molecules in an exoplanet atmosphere?\n"
                "- What might count as evidence of life?\n"
                "- Which future telescope or mission could answer this question?\n"
                "- How might scientists communicate a possible discovery of life?\n"
                "- How have different cultures imagined other worlds?\n\n"
                "Atmospheric molecules, spectra and biosignatures belong here as learn-more possibilities. They are "
                "not assumed knowledge or required content in either classroom pathway."
            )


def guidance_box(mode: str, student_text: str, teacher_text: str | None = None) -> None:
    if mode == "Student":
        st.info(student_text)
    elif mode == "Teacher" and teacher_text:
        st.info(student_text)
        with st.expander("Teacher guidance", expanded=False):
            st.write(teacher_text)
