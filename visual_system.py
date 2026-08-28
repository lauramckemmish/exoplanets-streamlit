"""Shared UNSW-derived visual tokens and restrained Streamlit component styles."""

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
    "primary_action": UNSW_PALETTE["yellow"],
    "primary_action_text": UNSW_PALETTE["black"],
    "information": UNSW_PALETTE["indigo"],
    "exploration": UNSW_PALETTE["purple"],
    "secondary_accent": UNSW_PALETTE["teal"],
    "success": UNSW_PALETTE["green"],
    "warning_error": UNSW_PALETTE["red"],
    "focus_selected": UNSW_PALETTE["yellow"],
}


def apply_visual_system() -> None:
    """Apply the shared visual treatment without overriding the active theme."""

    st.markdown(
        f"""
        <style>
        :root {{
            --unsw-brand: {SEMANTIC_TOKENS['brand']};
            --unsw-primary-action: {SEMANTIC_TOKENS['primary_action']};
            --unsw-primary-action-text: {SEMANTIC_TOKENS['primary_action_text']};
            --unsw-information: {SEMANTIC_TOKENS['information']};
            --unsw-exploration: {SEMANTIC_TOKENS['exploration']};
            --unsw-secondary-accent: {SEMANTIC_TOKENS['secondary_accent']};
            --unsw-success: {SEMANTIC_TOKENS['success']};
            --unsw-warning-error: {SEMANTIC_TOKENS['warning_error']};
        }}

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap: 0.35rem; }}
        [data-testid="stSidebar"] {{ border-right: 1px solid rgba(255, 220, 0, 0.35); }}
        [data-testid="stSidebar"] [data-testid="stButton"] > button {{
            min-height: 2rem;
            padding: 0.2rem 0.45rem;
            font-size: 0.88rem;
        }}

        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button[kind="primary"] {{
            background: var(--unsw-primary-action);
            border-color: var(--unsw-primary-action);
            color: var(--unsw-primary-action-text);
            font-weight: 650;
        }}
        [data-testid="stButton"] > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {{
            background: #FFE54D;
            border-color: #FFE54D;
            color: var(--unsw-primary-action-text);
        }}
        [data-testid="stButton"] > button[kind="secondary"] {{
            background: rgba(63, 97, 196, 0.08);
            border-color: rgba(63, 97, 196, 0.65);
        }}
        [data-testid="stButton"] > button:focus-visible,
        [data-testid="stFormSubmitButton"] > button:focus-visible,
        [data-testid="stTabs"] button:focus-visible {{
            outline: 3px solid var(--unsw-primary-action-text);
            outline-offset: 2px;
            box-shadow: 0 0 0 5px var(--unsw-brand);
        }}

        [data-testid="stTabs"] button[aria-selected="true"] {{
            background: var(--unsw-brand);
            color: var(--unsw-primary-action-text);
            border-radius: 0.3rem 0.3rem 0 0;
        }}
        [data-testid="stTabs"] button[aria-selected="true"] p {{
            color: var(--unsw-primary-action-text);
            font-weight: 650;
        }}
        [data-testid="stExpander"] {{ border-left: 3px solid rgba(63, 97, 196, 0.7); }}
        [data-testid="stMetric"] {{ border-left: 3px solid var(--unsw-brand); padding-left: 0.55rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
