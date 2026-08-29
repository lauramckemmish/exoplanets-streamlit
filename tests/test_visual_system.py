"""Shared UNSW visual-token checks."""

import unittest
from pathlib import Path

from visual_system import SEMANTIC_TOKENS, UNSW_PALETTE


class UNSWVisualSystemTests(unittest.TestCase):
    def test_official_core_palette_is_preserved(self):
        self.assertEqual(UNSW_PALETTE["yellow"], "#FFDC00")
        self.assertEqual(UNSW_PALETTE["black"], "#000000")
        self.assertEqual(UNSW_PALETTE["white"], "#FFFFFF")

    def test_yellow_is_reserved_for_active_and_high_value_emphasis(self):
        self.assertEqual(SEMANTIC_TOKENS["active_emphasis"], UNSW_PALETTE["yellow"])
        self.assertEqual(SEMANTIC_TOKENS["high_value_action"], UNSW_PALETTE["yellow"])
        self.assertEqual(SEMANTIC_TOKENS["filled_yellow_text"], UNSW_PALETTE["black"])

    def test_functional_roles_use_the_official_accents(self):
        self.assertEqual(SEMANTIC_TOKENS["information"], UNSW_PALETTE["indigo"])
        self.assertEqual(SEMANTIC_TOKENS["success"], UNSW_PALETTE["green"])
        self.assertEqual(SEMANTIC_TOKENS["warning_error"], UNSW_PALETTE["red"])

    def test_native_streamlit_theme_uses_shared_primary_and_info_colours(self):
        theme = Path(".streamlit/config.toml").read_text()
        self.assertIn('primaryColor = "#FFDC00"', theme)
        self.assertIn('blueColor = "#3F61C4"', theme)

    def test_staged_navigation_uses_a_compact_yellow_location_cue(self):
        styles = Path("visual_system.py").read_text()
        self.assertIn('[role="tablist"]', styles)
        self.assertIn('[data-testid="stTab"] hr {{ display: none; }}', styles)
        self.assertIn('border-left: 4px solid var(--unsw-active-emphasis)', styles)
        self.assertIn('[role="tab"] {{\n            min-height: 2rem;', styles)
        self.assertIn('border-radius: 0.3rem;\n            color: inherit;', styles)

    def test_shared_interaction_grammar_has_semantic_surfaces(self):
        styles = Path("visual_system.py").read_text()
        helpers = Path("ui_helpers.py").read_text()
        self.assertIn('[data-testid="stAlert"][data-baseweb="notification"]', styles)
        self.assertIn('st-key-hard_reveal_', styles)
        self.assertIn('💭', helpers)
        self.assertIn('🧩 {label}', helpers)
        self.assertIn('#### 🧭 {prompt}', helpers)


if __name__ == "__main__":
    unittest.main()
