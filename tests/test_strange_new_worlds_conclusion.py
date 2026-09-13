"""Focused checks for the short Strange New Worlds conclusion."""

import unittest
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events
        self.session_state = {}

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))

        return record


class StrangeNewWorldsConclusionTest(unittest.TestCase):
    def test_conclusion_is_a_short_synthesis_without_new_graph_or_response_box(self):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(
                strange_new_worlds,
                "conclude_prompt",
                lambda prompt: events.append(("conclude", (prompt,), {})),
            ),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 8, object())

        names = [event[0] for event in events]
        rendered = " ".join(str(event[1]) for event in events)
        self.assertEqual(names[0], "header")
        self.assertIn("conclude", names)
        self.assertIn("changed or strengthened", rendered)
        self.assertIn("not every planet that exists", rendered)
        self.assertNotIn("plotly_chart", names)
        self.assertNotIn("text_area", names)

    def test_facilitator_guidance_is_a_brief_cautious_synthesis(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[8]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[8]

        self.assertEqual(note["timing"], "3–5 minutes (Lesson 2 close)")
        self.assertIn("synthesis, not new content", note["facilitation"])
        self.assertIn("SC4-DA1-01 and SC4-OTU-01", note["alignment"])
        self.assertIn("not every planet", note["misconceptions"])
        self.assertIn("observations and data → expectation → representation", background)


if __name__ == "__main__":
    unittest.main()
