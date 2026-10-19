"""Shared UNSW-derived visual tokens and restrained Streamlit component styles."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path

import streamlit as st


UNSW_PALETTE = {
    "yellow": "#FFDC00",
    "black": "#000000",
    "white": "#FFFFFF",
    "indigo": "#3F61C4",
    "purple": "#8A68C8",
    "teal": "#007882",
    "pink": "#FA91B6",
    "red": "#FF635D",
    "green": "#1AC987",
    "facilitator_navy": "#294C70",
}

SEMANTIC_TOKENS = {
    "brand": UNSW_PALETTE["yellow"],
    "active_emphasis": UNSW_PALETTE["yellow"],
    "high_value_action": UNSW_PALETTE["yellow"],
    "filled_yellow_text": UNSW_PALETTE["black"],
    "information": UNSW_PALETTE["indigo"],
    "exploration": UNSW_PALETTE["purple"],
    "secondary_accent": UNSW_PALETTE["teal"],
    "success": UNSW_PALETTE["green"],
    "warning_error": UNSW_PALETTE["red"],
    "focus_selected": UNSW_PALETTE["yellow"],
    "facilitator_annotation": UNSW_PALETTE["facilitator_navy"],
}


def semantic_heading(text: str, role: str) -> None:
    """Render a semantic heading with an intentional shared visual role."""
    level = {"major-section": 2, "subsection": 3, "resource-identity": 3}[role]
    st.markdown(
        f'<h{level} class="type-{role}">{escape(text)}</h{level}>',
        unsafe_allow_html=True,
    )


def logo_plate(
    image_path: Path,
    *,
    width: int = 125,
    alt: str = "UNSW Sydney",
    plate_background: str = "#FFFFFF",
) -> None:
    """Render approved logo artwork on a compact theme-safe plate."""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    st.markdown(
        f"<div class='unsw-logo-plate' style='display:inline-block;background:{plate_background};padding:6px;border-radius:2px;line-height:0'>"
        f"<img src='data:image/png;base64,{encoded}' alt='{alt}' style='display:block;width:{width}px;height:auto'></div>",
        unsafe_allow_html=True,
    )


def resource_identity(title: str, logo_path: Path | None = None, *, logo_width: int = 125) -> None:
    """Render the About identity as one self-contained, responsive HTML component."""
    title_html = escape(title)
    logo_html = ""
    if logo_path:
        encoded = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        logo_html = (
            "<div class='resource-identity__logo'>"
            f"<img src='data:image/png;base64,{encoded}' alt='UNSW Sydney' "
            f"style='width:{logo_width}px;max-width:100%;height:auto;display:block'>"
            "</div>"
        )
    st.html(f"""
        <style>
        .resource-identity-container {{ container-type: inline-size; width: 100%; }}
        .resource-identity {{ display: grid; grid-template-columns: max-content minmax(0, 1fr); align-items: center; gap: 1rem; }}
        .resource-identity__logo {{ box-sizing: content-box; width: {logo_width}px; max-width: 100%; padding: 6px; background: #fff; border-radius: 2px; line-height: 0; }}
        .resource-identity__title {{ min-width: 0; margin: 0; overflow-wrap: anywhere; }}
        @container (max-width: 560px) {{ .resource-identity {{ grid-template-columns: minmax(0, 1fr); }} }}
        </style>
        <div class='resource-identity-container'>
            <div class='resource-identity' role='group' aria-label='Resource identity'>
                {logo_html}
                <h3 class='resource-identity__title type-resource-identity'>{title_html}</h3>
            </div>
        </div>
        """)


def apply_visual_system() -> None:
    """Apply the shared visual treatment without overriding the active theme."""

    st.markdown(
        f"""
        <style>
        :root {{
            --unsw-brand: {SEMANTIC_TOKENS['brand']};
            --unsw-active-emphasis: {SEMANTIC_TOKENS['active_emphasis']};
            --unsw-filled-yellow-text: {SEMANTIC_TOKENS['filled_yellow_text']};
            --unsw-information: {SEMANTIC_TOKENS['information']};
            --unsw-exploration: {SEMANTIC_TOKENS['exploration']};
            --unsw-secondary-accent: {SEMANTIC_TOKENS['secondary_accent']};
            --unsw-success: {SEMANTIC_TOKENS['success']};
            --unsw-warning-error: {SEMANTIC_TOKENS['warning_error']};
            --unsw-facilitator-annotation: {SEMANTIC_TOKENS['facilitator_annotation']};
        }}

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap: 0.35rem; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid rgba(255, 220, 0, 0.35); }}
        [class*="st-key-media_text_"] [data-testid="stHorizontalBlock"] {{ align-items: center; }}
        @media (max-width: 700px) {{
            [class*="st-key-media_text_"] [data-testid="stHorizontalBlock"] {{ flex-direction: column; gap: 0.65rem; }}
            [class*="st-key-media_text_"] [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; }}
        }}
        [data-testid="stSidebar"] .st-key-sidebar_brand {{
            background: var(--unsw-brand);
            color: var(--unsw-filled-yellow-text);
            padding: 0.65rem 0.7rem 0.6rem;
            margin: -0.15rem -0.35rem 0.6rem;
            border-radius: 0 0 0.3rem 0.3rem;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_brand h3,
        [data-testid="stSidebar"] .st-key-sidebar_brand p,
        [data-testid="stSidebar"] .st-key-sidebar_brand [data-testid="stCaptionContainer"] {{
            color: var(--unsw-filled-yellow-text) !important;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_brand [data-testid="stCaptionContainer"] p {{
            color: var(--unsw-filled-yellow-text) !important;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_brand .unsw-logo-plate {{
            background: transparent !important;
            padding: 0 !important;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_data_source {{
            background: #111827;
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 0.3rem;
            padding: 0.55rem 0.65rem 0.5rem;
            margin: 0 0 0.55rem;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_data_source p,
        [data-testid="stSidebar"] .st-key-sidebar_data_source [data-testid="stCaptionContainer"] {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_data_source [data-testid="stMarkdownContainer"] p {{
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.2rem;
        }}
        [data-testid="stSidebar"] .st-key-sidebar_data_count {{ margin-bottom: 0.4rem; }}
        [data-testid="stSidebar"] .st-key-sidebar_data_source hr {{
            margin: 0.25rem 0 !important;
            border-color: rgba(255, 255, 255, 0.22);
        }}
        .st-key-landing_about_label {{
            display: flex;
            align-items: center;
            min-height: 2.1rem;
            background: #111827;
            color: #FFFFFF;
            padding: 0.35rem 0.65rem;
            margin: 0.15rem 0 0.7rem;
            border-radius: 0.25rem;
        }}
        .st-key-landing_about_label p {{
            color: #FFFFFF !important;
            font-weight: 650;
            line-height: 1.2;
            margin: 0;
        }}
        /* Intentional landing roles: content sections lead; institutional identity stays quiet. */
        .type-major-section {{
            font-size: clamp(1.35rem, 2.2vw, 1.65rem);
            line-height: 1.2;
        }}
        .type-subsection {{
            font-size: 1.25rem;
            line-height: 1.25;
        }}
        .type-resource-identity {{
            font-size: clamp(1.25rem, 2.1vw, 1.55rem);
            line-height: 1.2;
        }}
        .st-key-unsw_identity_row .unsw-logo-plate {{
            box-sizing: content-box;
            min-width: 60px;
        }}
        .st-key-unsw_identity_row [data-testid="column"]:has(.unsw-logo-plate) {{
            min-width: 72px;
            flex-shrink: 0;
        }}
        @media (max-width: 700px) {{
            .st-key-unsw_identity_row [data-testid="stHorizontalBlock"] {{
                flex-direction: column;
                gap: 0.65rem;
            }}
            .st-key-unsw_identity_row [data-testid="column"] {{
                width: 100% !important;
                flex: 1 1 100% !important;
            }}
        }}
        .st-key-landing_stewardship {{
            border-left: 3px solid var(--unsw-active-emphasis);
            background: rgba(63, 97, 196, 0.06);
            padding: 0.55rem 0.65rem 0.75rem;
        }}
        .st-key-landing_stewardship p {{
            line-height: 1.4;
            margin-bottom: 0.15rem;
        }}
        .st-key-graph_reading_support {{
            border-left: 2px solid var(--unsw-secondary-accent);
            background: rgba(0, 120, 130, 0.06);
            padding: 0.45rem 0.65rem;
            margin: 0.35rem 0 0.55rem;
        }}
        .st-key-graph_reading_support p {{ margin-bottom: 0.2rem; }}
        /* Facilitator preparation is quiet; live cues are deliberately scan-friendly. */
        [class*="st-key-facilitator_preparation_"] {{
            border-left: 3px solid var(--unsw-facilitator-annotation);
            background: rgba(41, 76, 112, 0.045);
            padding: 0.15rem 0.45rem;
            margin: 0.55rem 0 0.8rem;
        }}
        [class*="st-key-facilitator_preparation_"] [data-testid="stExpander"] {{ border-left: 0; }}
        [class*="st-key-facilitator_live_"] {{
            box-sizing: border-box;
            min-width: 0;
            max-width: 100%;
            border-left: 4px solid var(--unsw-facilitator-annotation);
            background: rgba(41, 76, 112, 0.10);
            padding: 0.4rem 0.65rem;
            margin: 0.35rem 0;
            overflow-wrap: anywhere;
        }}
        .facilitator-live__label {{
            display: block;
            color: var(--unsw-facilitator-annotation);
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.08em;
            line-height: 1.2;
        }}
        [class*="st-key-facilitator_live_"] p {{ margin-bottom: 0.15rem; line-height: 1.4; }}
        .st-key-curriculum_summary {{
            border-left: 3px solid var(--unsw-facilitator-annotation);
            background: rgba(41, 76, 112, 0.045);
            padding: 0.45rem 0.65rem 1.05rem;
            margin: 0.45rem 0 0.7rem;
        }}
        .curriculum-summary p {{ margin: 0 0 0.22rem; }}
        .curriculum-summary__title {{
            color: var(--unsw-facilitator-annotation);
            font-size: 0.82rem;
            font-weight: 750;
            letter-spacing: 0.03em;
        }}
        .curriculum-summary__outcome {{ font-size: 0.82rem; }}
        .curriculum-summary__outcome span,
        .curriculum-summary__legend,
        .curriculum-summary__note {{ color: rgba(49, 51, 63, 0.82); font-size: 0.76rem; }}
        .curriculum-summary__body {{ font-size: 0.9rem; line-height: 1.4; }}
        .curriculum-summary__note {{ margin-bottom: 0 !important; }}
        [class*="st-key-curriculum_tags_"] {{ margin: -0.3rem 0 0.55rem; }}
        .curriculum-tags {{
            color: rgba(49, 51, 63, 0.88);
            font-size: 0.78rem;
            line-height: 1.5;
            overflow-wrap: anywhere;
        }}
        .curriculum-tags__label {{ color: var(--unsw-facilitator-annotation); font-weight: 700; }}
        .curriculum-tags__item {{ white-space: nowrap; }}
        .st-key-facilitator_orientation {{
            border-left: 3px solid var(--unsw-facilitator-annotation);
            background: rgba(41, 76, 112, 0.06);
            padding: 0.5rem 0.7rem;
            margin: 0.45rem 0 0.8rem;
        }}
        /* Shared interaction grammar: named cognitive prompts never gate progress. */
        [data-testid="stAlert"][data-baseweb="notification"] {{
            border-left: 3px solid var(--unsw-information);
            background: rgba(63, 97, 196, 0.08);
        }}
        .st-key-notice_prompt, .st-key-compare_prompt, .st-key-predict_prompt,
        .st-key-explain_prompt, .st-key-conclude_prompt, .st-key-revise_prompt,
        .st-key-recall_prompt {{
            border-left: 2px solid currentColor;
            padding: 0.1rem 0 0.1rem 0.65rem;
            margin: 0.5rem 0 0.7rem;
        }}
        .st-key-notice_prompt .cognitive-prompt__label,
        .st-key-compare_prompt .cognitive-prompt__label,
        .st-key-predict_prompt .cognitive-prompt__label,
        .st-key-explain_prompt .cognitive-prompt__label,
        .st-key-conclude_prompt .cognitive-prompt__label,
        .st-key-revise_prompt .cognitive-prompt__label,
        .st-key-recall_prompt .cognitive-prompt__label,
        [class*="st-key-hard_reveal_"] .interaction-marker {{
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.08em;
            line-height: 1;
            margin: 0.05rem 0 0.35rem;
        }}
        .st-key-notice_prompt [data-testid="stMarkdownContainer"],
        .st-key-compare_prompt [data-testid="stMarkdownContainer"],
        .st-key-predict_prompt [data-testid="stMarkdownContainer"],
        .st-key-explain_prompt [data-testid="stMarkdownContainer"],
        .st-key-conclude_prompt [data-testid="stMarkdownContainer"],
        .st-key-revise_prompt [data-testid="stMarkdownContainer"],
        .st-key-recall_prompt [data-testid="stMarkdownContainer"] {{ background: transparent; }}
        [class*="st-key-hard_reveal_"] {{
            border-left: 3px solid var(--unsw-active-emphasis);
            padding-left: 0.65rem;
        }}
        [data-testid="stExpander"] {{ border-left: 3px solid var(--unsw-exploration); }}
        [data-testid="stSidebar"] [data-testid="stButton"] > button {{
            min-height: 2rem;
            padding: 0.2rem 0.45rem;
            font-size: 0.88rem;
        }}

        /* Primary is a clear action, not automatically a yellow surface. */
        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button[kind="primary"],
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-primaryFormSubmit"] {{
            background: transparent;
            border: 2px solid var(--unsw-active-emphasis);
            color: inherit;
            font-weight: 650;
        }}
        [data-testid="stButton"] > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover,
        [data-testid="stBaseButton-primary"]:hover,
        [data-testid="stBaseButton-primaryFormSubmit"]:hover {{
            background: rgba(255, 220, 0, 0.10);
            border-color: var(--unsw-active-emphasis);
            color: inherit;
        }}
        [data-testid="stButton"] > button[kind="secondary"] {{
            background: rgba(63, 97, 196, 0.08);
            border-color: rgba(63, 97, 196, 0.65);
        }}
        [data-testid="stButton"] > button:focus-visible,
        [data-testid="stFormSubmitButton"] > button:focus-visible,
        [data-testid="stTabs"] button:focus-visible,
        [data-testid="stTabs"] [role="tab"]:focus-visible {{
            outline: 3px solid currentColor;
            outline-offset: 2px;
            box-shadow: 0 0 0 5px var(--unsw-brand);
        }}

        [data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"] {{
            background: rgba(255, 220, 0, 0.10);
            border-color: transparent;
            border-left: 4px solid var(--unsw-active-emphasis);
            color: inherit;
            padding-left: calc(0.45rem - 2px);
        }}
        [data-testid="stSidebar"] [data-testid="stButton"] > button[kind="primary"]:hover {{
            background: rgba(255, 220, 0, 0.16);
            border-color: transparent;
            border-left-color: var(--unsw-active-emphasis);
            color: inherit;
        }}

        /* Shared staged navigation: compact location controls, not browser tabs. */
        [data-testid="stTabs"] [role="tablist"] {{
            gap: 0.25rem;
            flex-wrap: wrap;
            border-bottom: 0;
        }}
        [data-testid="stTabs"] [data-testid="stTab"] hr {{ display: none; }}
        [data-testid="stTabs"] [role="tab"] {{
            min-height: 2rem;
            padding: 0.3rem 0.55rem;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 0.3rem;
            color: inherit;
        }}
        [data-testid="stTabs"] [role="tab"]:hover {{
            background: rgba(255, 220, 0, 0.08);
        }}
        [data-testid="stTabs"] [role="tab"][aria-selected="true"],
        [data-testid="stTabs"] [role="tab"][data-selected="true"] {{
            background: transparent;
            border: 1px solid transparent;
            border-left: 4px solid var(--unsw-active-emphasis);
            padding-left: calc(0.55rem - 3px);
        }}
        [data-testid="stTabs"] [role="tab"][aria-selected="true"] p,
        [data-testid="stTabs"] [role="tab"][data-selected="true"] p {{
            color: inherit;
            font-weight: 650;
        }}
        [data-testid="stMetric"] {{ border-left: 3px solid var(--unsw-brand); padding-left: 0.55rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


TYPOGRAPHY_TOKENS = {
    "heading_font": "'Tomorrow'",
    "heading_weight": "700",
    # Body text is Atkinson Hyperlegible. "Tomorrow Digits" is Tomorrow limited to the digits 0-9 (see
    # _DIGIT_FONT_CSS), listed first so stand-alone numbers (slider values, metrics, table cells) keep the
    # Tomorrow look while all other characters fall through. Numbers inside sentences stay in the body font.
    "body_font": "'Atkinson Hyperlegible'",
    "number_font": "'Tomorrow Digits', 'Atkinson Hyperlegible'",
    "body_font_fallback": "'Source Sans', 'Source Sans Pro', sans-serif",
    "body_weight": "400",
    "body_strong_weight": "700",
    # Atkinson Hyperlegible looks smaller than Tomorrow at the same size, so every size is 1px larger than before.
    "learner_min_size": "1.0625rem",
    "facilitator_min_size": "0.9375rem",
}
_HEADING_FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Tomorrow:wght@400;700"
    "&family=Atkinson+Hyperlegible:wght@400;700&display=swap"
)
# Tomorrow restricted to digits, so numbers in body text keep the Tomorrow look. If these files ever move,
# digits quietly fall back to Atkinson Hyperlegible and nothing breaks.
_DIGIT_FONT_CSS = """
@font-face { font-family: 'Tomorrow Digits'; font-weight: 400; font-display: swap; unicode-range: U+0030-0039;
    src: url(https://fonts.gstatic.com/s/tomorrow/v19/WBLmrETNbFtZCeGqgRXSe2DiLsip.woff2) format('woff2'); }
@font-face { font-family: 'Tomorrow Digits'; font-weight: 700; font-display: swap; unicode-range: U+0030-0039;
    src: url(https://fonts.gstatic.com/s/tomorrow/v19/WBLhrETNbFtZCeGqgR1pXnXPDMWDikd5.woff2) format('woff2'); }
"""


def apply_typography(scope_key: str) -> None:
    """Apply bold headings and minimum text sizes only while ``scope_key`` is on the page.

    Typography is opt-in per experience. The experience renders this marker
    container once; the styles apply to the main content area only while the
    marker exists, so other experiences keep their current appearance.
    """

    heading_font = TYPOGRAPHY_TOKENS["heading_font"]
    body_font = TYPOGRAPHY_TOKENS["body_font"]
    number_font = TYPOGRAPHY_TOKENS["number_font"]
    fallback = TYPOGRAPHY_TOKENS["body_font_fallback"]
    weight = TYPOGRAPHY_TOKENS["heading_weight"]
    body_weight = TYPOGRAPHY_TOKENS["body_weight"]
    strong_weight = TYPOGRAPHY_TOKENS["body_strong_weight"]
    learner = TYPOGRAPHY_TOKENS["learner_min_size"]
    facilitator = TYPOGRAPHY_TOKENS["facilitator_min_size"]
    scope = f'[data-testid="stMain"]:has(.st-key-{scope_key})'
    with st.container(key=scope_key):
        st.markdown(
            f"""
            <style>
            @import url('{_HEADING_FONT_URL}');
            {_DIGIT_FONT_CSS}
            {scope} h1, {scope} h2, {scope} h3, {scope} h4 {{
                font-family: {heading_font}, {fallback};
                font-weight: {weight};
            }}
            {scope} h1 *, {scope} h2 *, {scope} h3 *, {scope} h4 * {{ font-weight: {weight}; }}
            /* Body text: Atkinson Hyperlegible, with Tomorrow digits. Targeted, so icon fonts are untouched. */
            {scope} p, {scope} li, {scope} summary, {scope} label,
            {scope} [data-testid="stCaptionContainer"],
            {scope} [data-testid="stMetricValue"], {scope} [data-testid="stMetricLabel"] {{
                font-family: {body_font}, {fallback};
                font-weight: {body_weight};
            }}
            {scope} p strong, {scope} li strong, {scope} p b, {scope} li b {{ font-weight: {strong_weight}; }}
            /* Facilitator live cues: Streamlit pulls each markdown block up by 1rem to cancel its last paragraph's
               margin, but the shared cue style shrinks that margin, so the shaded box ended short of its text.
               Remove the margin and the pull-up together so the box encloses all of the text. */
            {scope} [class*="st-key-facilitator_live_"] {{ gap: 0.1rem; }}
            {scope} [class*="st-key-facilitator_live_"] [data-testid="stMarkdownContainer"] {{ margin-bottom: 0; }}
            {scope} [class*="st-key-facilitator_live_"] p {{ margin-bottom: 0; }}
            /* The curriculum summary box sat only about 1px clear of its last line at the larger text size. */
            {scope} .st-key-curriculum_summary {{ padding-bottom: 1.5rem; }}
            /* Table cells follow the same font (weight is left to the table's own styling). */
            {scope} td, {scope} th {{ font-family: {number_font}, {fallback}; }}
            /* Stand-alone numbers (not part of a sentence) use Tomorrow digits. */
            {scope} [data-testid="stMetricValue"], {scope} [data-testid="stMetricValue"] *,
            {scope} [data-testid="stSliderThumbValue"], {scope} [data-testid="stSliderThumbValue"] p,
            {scope} [data-testid="stSliderTickBarMin"], {scope} [data-testid="stSliderTickBarMax"] {{ font-family: {number_font}, {fallback}; }}
            /* Plain Markdown paragraphs and list items are body text at the learner size. */
            {scope} [data-testid="stMarkdownContainer"] > p,
            {scope} [data-testid="stMarkdownContainer"] > ul li,
            {scope} [data-testid="stMarkdownContainer"] > ol li {{ font-size: {learner}; }}
            /* Learner-facing text: nothing smaller than body size. */
            {scope} [data-testid="stCaptionContainer"],
            {scope} [data-testid="stCaptionContainer"] p,
            {scope} [data-testid="stTabs"] [role="tab"] p,
            {scope} [data-testid="stWidgetLabel"] p,
            {scope} [data-testid="stButton"] button p,
            {scope} [data-testid="stSlider"] p,
            {scope} [data-testid="stRadio"] p,
            {scope} [data-testid="stCheckbox"] p,
            {scope} [data-testid="stMetricLabel"] p,
            {scope} [data-testid="stSliderTickBarMin"],
            {scope} [data-testid="stSliderTickBarMax"],
            {scope} [data-testid="stExpander"] summary p,
            {scope} [class*="st-key-hard_reveal_"] .interaction-marker,
            {scope} [class*="_prompt"] .cognitive-prompt__label {{ font-size: {learner}; }}
            /* Facilitator-only text: smaller is allowed, but not tiny. */
            {scope} .facilitator-live__label,
            {scope} .curriculum-summary__outcome,
            {scope} .curriculum-summary__note,
            {scope} .curriculum-summary__body,
            {scope} .curriculum-summary p,
            {scope} .curriculum-tags {{ font-size: {facilitator}; }}
            {scope} .curriculum-summary__outcome span {{ font-size: 1em; }}
            </style>
            """,
            unsafe_allow_html=True,
        )


SPACING_TOKENS = {
    # Added on top of the normal gap between elements.
    "section_space": "1.75rem",
}


def apply_section_spacing(scope_key: str) -> None:
    """Add a clear break before section headings and REVEAL blocks, while ``scope_key`` is on the page.

    Opt-in per stage, like ``apply_typography``. Only headings that sit directly in the page flow
    are affected, so headings inside columns or bordered boxes (for example the planet portrait and
    profile) keep their alignment.
    """

    space = SPACING_TOKENS["section_space"]
    scope = f'[data-testid="stMain"]:has(.st-key-{scope_key})'
    flow = f'{scope} [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"]'
    with st.container(key=scope_key):
        st.markdown(
            f"""
            <style>
            {flow} > [data-testid="stElementContainer"]:has(h4) {{ margin-top: {space}; }}
            {flow} > [data-testid="stLayoutWrapper"]:has(> [class*="st-key-hard_reveal_"] .interaction-marker) {{ margin-top: {space}; }}
            </style>
            """,
            unsafe_allow_html=True,
        )


SLIDER_TOKENS = {
    "track_height": "7px",  # Streamlit default: 4px
    "thumb_size": "19px",  # Streamlit default: 12px
    "value_size": "1.1rem",  # Streamlit default: 1rem
    "value_lift": "-30px",  # Moves the value above the larger thumb (default: -22px)
    "group_height": "40px",  # Leaves room for the larger thumb and value (default: 40px)
    "group_top_space": "12px",  # Keeps the larger value label clear of the slider's own label
}


def apply_slider_style(scope_key: str) -> None:
    """Make sliders easier to see and grab, while ``scope_key`` is on the page.

    Opt-in per experience, like ``apply_typography``. The changes are deliberately modest:
    a thicker track, a larger handle and a larger value label.
    """

    t = SLIDER_TOKENS
    slider = f'[data-testid="stMain"]:has(.st-key-{scope_key}) [data-testid="stSlider"]'
    with st.container(key=scope_key):
        st.markdown(
            f"""
            <style>
            {slider} [role="group"] {{ height: {t['group_height']}; margin-top: {t['group_top_space']}; }}
            {slider} [role="group"] > div > div:first-child {{
                height: {t['track_height']};
                border-radius: calc({t['track_height']} / 2);
            }}
            {slider} [role="group"] > div > div:has(input[type="range"]) {{
                width: {t['thumb_size']};
                height: {t['thumb_size']};
            }}
            {slider} [data-testid="stSliderThumbValue"] {{ top: {t['value_lift']}; }}
            {slider} [data-testid="stSliderThumbValue"] p {{ font-size: {t['value_size']}; }}
            </style>
            """,
            unsafe_allow_html=True,
        )
