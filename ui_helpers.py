"""Small, reusable presentation helpers shared by the teaching experiences."""

import base64
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def logo_plate(image_path: Path, *, width: int, alt: str) -> None:
    """Render approved logo artwork on a small, theme-independent white plate."""

    encoded_image = base64.b64encode(image_path.read_bytes()).decode("ascii")
    st.markdown(
        f"<div style='display: inline-block; background: white; padding: 6px; "
        f"border-radius: 2px; line-height: 0;'>"
        f"<img src='data:image/png;base64,{encoded_image}' alt='{alt}' "
        f"style='display: block; width: {width}px; height: auto;'></div>",
        unsafe_allow_html=True,
    )


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
    """Render shared compact, keyboard-accessible staged navigation."""
    current_step = max(0, min(current_step, len(labels) - 1))
    if st.session_state.get(key) not in labels:
        st.session_state[key] = labels[current_step]
    tabs = st.tabs(labels, default=st.session_state[key], key=key, on_change="rerun")
    return tabs, labels.index(st.session_state.get(key, labels[current_step]))


def step_buttons(
    labels: list[str],
    tab_key: str,
    step_key: str,
    scroll_key: str,
    step: int,
    button_prefix: str,
    allow_next: bool = True,
) -> None:
    """Render Back/Continue controls, optionally withholding Continue."""
    back, _, next_step = st.columns([1, 4, 1])
    with back:
        if step > 0:
            st.button(
                "← Back",
                use_container_width=True,
                key=f"{button_prefix}_back",
                on_click=select_tab_step,
                args=(tab_key, labels, step_key, scroll_key, step - 1),
            )
    with next_step:
        if allow_next and step < len(labels) - 1:
            st.button(
                "Continue →",
                type="primary",
                use_container_width=True,
                key=f"{button_prefix}_continue",
                on_click=select_tab_step,
                args=(tab_key, labels, step_key, scroll_key, step + 1),
            )


def scroll_to_top_if_requested(key: str) -> None:
    if not st.session_state.pop(key, False):
        return
    components.html(
        """
        <script>
            const doc = window.parent.document;
            const container = doc.querySelector('[data-testid="stAppViewContainer"]') || doc.querySelector('section.main');
            if (container) container.scrollTo({top: 0, left: 0, behavior: 'instant'});
            window.parent.scrollTo({top: 0, left: 0, behavior: 'instant'});
        </script>
        """,
        height=0,
    )


def persistent_reveal(
    prompt: str,
    key: str,
    *,
    reveal_label: str,
    revealed_message: str | None = None,
    explanation: str | None = None,
) -> bool:
    """Backward-compatible alias for a persistent hard reveal."""
    return hard_reveal(
        prompt,
        key,
        reveal_label=reveal_label,
        revealed_message=revealed_message,
        explanation=explanation,
    )


def pause_cue(prompt: str, *, title: str = "Pause and discuss") -> None:
    """Mark a visible, discreet and non-blocking moment for learner reasoning."""
    st.info(f"_{title}_\n\n{prompt}")


def hard_reveal(
    prompt: str,
    key: str,
    *,
    reveal_label: str,
    revealed_message: str | None = None,
    explanation: str | None = None,
    title: str = "Pause and predict",
) -> bool:
    """Persistently reveal essential material after a compact reasoning prompt.

    The calling stage is responsible for passing this return value to
    ``step_buttons(..., allow_next=...)`` when the reveal is required before
    its next stage.
    """
    st.info(f"_{title}_\n\n{prompt}")
    if key not in st.session_state:
        st.session_state[key] = False
    if not st.session_state[key]:
        st.button(
            reveal_label,
            type="primary",
            key=f"{key}_button",
            on_click=lambda: st.session_state.__setitem__(key, True),
        )
        return False
    if revealed_message:
        st.success(revealed_message)
    if explanation:
        st.write(explanation)
    return True


@contextmanager
def soft_reveal(label: str, *, expanded: bool = False) -> Iterator[None]:
    """Provide optional supporting material without gating progression."""
    with st.expander(label, expanded=expanded):
        yield


def choice_reveal(
    prompt: str,
    choices: Mapping[str, str],
    key: str,
    *,
    label: str = "Choose one or more to explore",
) -> list[str]:
    """Offer optional explanations that learners can choose for themselves."""
    st.markdown(f"#### {prompt}")
    selected = st.multiselect(label, list(choices), key=key)
    for choice in selected:
        st.markdown(f"**{choice}**")
        st.write(choices[choice])
    return selected


def _validate_image_role(role: str) -> None:
    if role not in {"context", "evidence", "graph", "support", "hero"}:
        raise ValueError(f"Unknown image role: {role}")


def _render_role_image(image, caption: str | None) -> None:
    st.image(image, caption=caption, width="stretch")


def role_image(image, *, role: str, caption: str | None = None, key: str | None = None) -> None:
    """Render an image responsively according to its pedagogical role.

    Context images are about half width and support images are compact on wide
    screens; both use the available width on narrow screens. Evidence, graph
    and hero images use the useful width. Captions retain supplied context.
    """
    _validate_image_role(role)
    if key is None:
        _render_role_image(image, caption)
        return
    with st.container(key=f"role_image_{role}_{key}"):
        _render_role_image(image, caption)


@contextmanager
def media_text_pair(image, *, role: str, caption: str | None = None, key: str) -> Iterator[None]:
    """Pair context/support media with text, stacking at narrow widths."""
    if role not in {"context", "support"}:
        raise ValueError("A media/text pair must use the context or support role")
    ratios = [1, 1] if role == "context" else [1, 2]
    with st.container(key=f"media_text_{key}"):
        image_column, text_column = st.columns(ratios, gap="medium")
        with image_column:
            _render_role_image(image, caption)
        with text_column:
            yield


def log_scale_reveal(prompt: str, key: str) -> bool:
    """Backward-compatible log-scale reveal used by older deployed modules."""
    return persistent_reveal(
        prompt,
        key,
        reveal_label="Reveal a new way to view the same data →",
        revealed_message=(
            "**Same planets. Same variables. Different spacing.** A log scale "
            "spreads out the small values while keeping the giant planets on the same graph."
        ),
        explanation=(
            "The variables do not change: the graph still shows planet mass and orbital distance. "
            "On a log scale, equal spaces represent multiplication. For example, the gap from "
            "**0.1 to 1** is the same size as the gap from **1 to 10**. You do not need to "
            "calculate logarithms to read the graph."
        ),
    )


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


def sample_note(data, required: list[str], label: str = "records") -> int:
    complete = int(data[required].notna().all(axis=1).sum())
    excluded = len(data) - complete
    st.caption(
        f"**Data used:** {complete:,} of {len(data):,} {label}. "
        f"{excluded:,} are not shown because at least one required value is missing."
    )
    return complete


def teacher_note(
    title: str,
    purpose: str,
    facilitation: str,
    alignment: str = "",
    *,
    timing: str = "",
    evidence: str = "",
    listen_for: str = "",
    background: str = "",
    misconceptions: str = "",
    facilitator_moment: str = "",
    resources: tuple[tuple[str, str], ...] = (),
    teacher_state_key: str = "demographics_teacher_view",
) -> None:
    if not st.session_state.get(teacher_state_key, False):
        return
    with st.container(border=True):
        st.markdown(f"### 👩‍🏫 Teacher view: {title}")
        if timing:
            st.caption(f"Suggested time: {timing} · Use this as guidance, not a required pace.")
        st.markdown(f"**Learning intention:** {purpose}")
        if alignment:
            st.markdown(f"**Relevant NSW syllabus outcomes:** {alignment}")
        if evidence:
            st.markdown(f"**Evidence of learning:** {evidence}")
        with st.expander("Teaching this step"):
            st.markdown(f"**Suggested approach:** {facilitation}")
            if listen_for:
                st.markdown(f"**Listen for:** {listen_for}")
            if facilitator_moment:
                st.markdown(f"**Facilitator-owned moment:** {facilitator_moment}")
        if background or misconceptions:
            with st.expander("Teacher background and possible misconceptions"):
                if background:
                    st.markdown(background)
                if misconceptions:
                    st.markdown(f"**Possible misconceptions:** {misconceptions}")
        if resources:
            with st.expander("Resources and optional extension"):
                for label, url in resources:
                    st.markdown(f"- [{label}]({url})")
                st.caption("These are optional teacher background or no-equipment research resources; they are not additional required activities.")


def demographics_question(wonder: str, data_question: str, plot_description: str) -> None:
    st.markdown(f"### I wonder…\n{wonder}")
    st.markdown(f"### Question we can answer with data\n{data_question}")
    st.markdown(f"### What we will plot\n{plot_description}")


def mission_navigation(step: int, total: int, position: str) -> None:
    left, middle, right = st.columns([1, 4, 1])
    with left:
        if step > 0 and st.button("← Back", use_container_width=True, key=f"{position}_back_{step}"):
            st.session_state["mission_step"] = step - 1
            st.rerun()
    with middle:
        st.progress((step + 1) / total, text=f"Mission stage {step + 1} of {total}")
    with right:
        if step < total - 1 and st.button("Continue →", use_container_width=True, type="primary", key=f"{position}_continue_{step}"):
            st.session_state["mission_step"] = step + 1
            st.rerun()


def presenter_notes(step: int, notes_by_step: dict) -> None:
    notes = notes_by_step[step]
    with st.expander("Demonstrator notes", expanded=False):
        st.markdown(f"**Explain**  \n{notes['explain']}")
        st.markdown(f"**Ask the group**  \n{notes['ask']}")
        st.markdown(f"**Expected response**  \n{notes['expected']}")
        st.markdown(f"**Key data-science idea**  \n{notes['idea']}")
        st.markdown(f"**Watch for**  \n{notes['watch']}")


def variable_card(data, field: str, guidance_mode: str, variables: dict, scale_guidance) -> None:
    details = variables[field]
    status, reason, profile = scale_guidance(data, field, variables)
    st.markdown(f"#### {details['label']}")
    st.write(f"**Field:** `{field}`  ")
    st.write(f"**Unit:** {details['unit']}  ")
    st.write(details["description"])
    if guidance_mode != "Minimal":
        st.caption(details["measurement"])
        st.info(f"**Scale guidance: {status}.** {reason}")
        st.caption(f"Available for {profile['complete']:,} of {len(data):,} records; {profile['missing']:,} values are missing.")
