"""Find Tatooine experience entry point.

The implementation is injected by ``app.py`` so this module does not import
the Streamlit application back into itself (which would create a cycle).
"""


def render(data, presenter_mode, implementation):
    return implementation(data, presenter_mode)
