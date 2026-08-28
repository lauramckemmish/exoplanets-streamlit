"""Shared UNSW visual-token checks."""

import unittest

from visual_system import SEMANTIC_TOKENS, UNSW_PALETTE


class UNSWVisualSystemTests(unittest.TestCase):
    def test_official_core_palette_is_preserved(self):
        self.assertEqual(UNSW_PALETTE["yellow"], "#FFDC00")
        self.assertEqual(UNSW_PALETTE["black"], "#000000")
        self.assertEqual(UNSW_PALETTE["white"], "#FFFFFF")

    def test_primary_actions_use_black_on_unsw_yellow(self):
        self.assertEqual(SEMANTIC_TOKENS["primary_action"], UNSW_PALETTE["yellow"])
        self.assertEqual(SEMANTIC_TOKENS["primary_action_text"], UNSW_PALETTE["black"])

    def test_functional_roles_use_the_official_accents(self):
        self.assertEqual(SEMANTIC_TOKENS["information"], UNSW_PALETTE["indigo"])
        self.assertEqual(SEMANTIC_TOKENS["success"], UNSW_PALETTE["green"])
        self.assertEqual(SEMANTIC_TOKENS["warning_error"], UNSW_PALETTE["red"])


if __name__ == "__main__":
    unittest.main()
