"""Focused contracts for the CURIOUS reveal and formative-check sequence."""

import unittest
from pathlib import Path


CURIOUS_SOURCE = Path("experiences/curious.py").read_text()


class CuriousInteractionTests(unittest.TestCase):
    def test_steps_one_two_and_four_add_collapsed_self_checks(self):
        for label in (
            "Check your reading",
            "Check your comparison",
            "Check what the graph can support",
        ):
            self.assertIn(f'with self_check("{label}"):', CURIOUS_SOURCE)

    def test_log_scale_explanation_follows_the_notice_prompt_in_a_self_check(self):
        notice_index = CURIOUS_SOURCE.index("What can you see now that was difficult to see before?")
        check_index = CURIOUS_SOURCE.index('with self_check("Check what changed"):')
        self.assertLess(notice_index, check_index)
        self.assertIn("The planets, variables and values did not change.", CURIOUS_SOURCE)

    def test_method_interpretation_is_a_hard_reveal_after_the_graph(self):
        graph_index = CURIOUS_SOURCE.index("st.plotly_chart(demographics_methods_chart")
        reveal_index = CURIOUS_SOURCE.index('"curious_method_pattern_revealed"')
        discussion_index = CURIOUS_SOURCE.index('st.markdown("### Discuss")', reveal_index)
        self.assertLess(graph_index, reveal_index)
        self.assertLess(reveal_index, discussion_index)
        self.assertNotIn('with soft_reveal("What pattern does the evidence support?"):', CURIOUS_SOURCE)

    def test_transit_animation_and_conclusion_remain_soft_reveals(self):
        self.assertIn('with soft_reveal("Watch transit detection in motion"):', CURIOUS_SOURCE)
        self.assertIn('with soft_reveal("How planetary systems form"):', CURIOUS_SOURCE)


if __name__ == "__main__":
    unittest.main()
