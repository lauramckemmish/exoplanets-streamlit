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
        /* Shared interaction grammar: THINK is a cue, while REVEAL protects evidence. */
        [data-testid="stAlert"][data-baseweb="notification"] {{
            border-left: 3px solid var(--unsw-information);
            background: rgba(63, 97, 196, 0.08);
        }}
        .st-key-think_q {{
            border-left: 3px solid currentColor;
            padding-left: 0.65rem;
            margin: 0.5rem 0;
        }}
        .st-key-think_q .interaction-marker,
        [class*="st-key-hard_reveal_"] .interaction-marker {{
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.08em;
            line-height: 1;
            margin: 0.05rem 0 0.35rem;
        }}
        .st-key-think_q [data-testid="stMarkdownContainer"] {{ background: transparent; }}
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
