"""Focused checks for the evidence-history Strange New Worlds conclusion."""

import unittest
from contextlib import nullcontext
from pathlib import Path
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

    def container(self, *args, **kwargs):
        self.events.append(("container", args, kwargs))
        return nullcontext()


class StrangeNewWorldsConclusionTest(unittest.TestCase):
    def test_conclusion_connects_growing_evidence_without_a_new_response_or_gate(self):
        events = []
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "soft_reveal", lambda label: nullcontext()),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 8, object())

        names = [event[0] for event in events]
        rendered = " ".join(str(event[1]) for event in events)
        self.assertEqual(names[0], "header")
        self.assertNotIn("conclude", names)
        self.assertIn("The journey you just made is very close to the one astronomers made.", rendered)
        self.assertIn("sample size was one planetary system", rendered)
        self.assertIn("Five planets were visible", rendered)
        self.assertIn("same planetary system", rendered)
        self.assertIn("51 Pegasi b helped change the game", rendered)
        self.assertIn("much bigger sample is not a complete one", rendered)
        self.assertIn("easier for us to find and measure", rendered)
        self.assertIn("New telescopes and observations", rendered)
        self.assertIn("evidence got better", rendered)
        self.assertNotIn("plotly_chart", names)
        self.assertNotIn("text_area", names)

    def test_pluto_is_a_collapsed_optional_evidence_and_classification_parallel(self):
        source = Path("experiences/strange_new_worlds.py").read_text()
        screen_eight = source.split("elif part == 8:", 1)[1]

        self.assertIn('with soft_reveal("Wait — hasn’t this happened in our Solar System too?"):', screen_eight)
        self.assertIn("more Pluto-like worlds, including objects such as Eris", screen_eight)
        self.assertIn("In 2006, astronomers agreed on a new definition of a planet", screen_eight)
        self.assertIn("More discoveries changed the way scientists organised the evidence.", screen_eight)
        self.assertNotIn("1992", screen_eight)

    def test_facilitator_guidance_is_a_brief_evidence_history_close(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[8]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[8]

        self.assertEqual(note["timing"], "3–5 minutes (Lesson 2 close)")
        self.assertIn("Screen 7 has already done that work", note["facilitation"])
        self.assertIn("SC4-DA1-01 and SC4-OTU-01", note["alignment"])
        self.assertIn("easier to find and measure", note["misconceptions"])
        self.assertIn("initial sample of one planetary system", background)
        self.assertIn("1995 and 51 Pegasi b", background)
        self.assertIn("optional Pluto parallel", background)


if __name__ == "__main__":
    unittest.main()
