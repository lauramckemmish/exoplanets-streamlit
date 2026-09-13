"""Focused checks for the Screen 5 real-world browser."""

import random
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events, state):
        self.events = events
        self.session_state = state

    def container(self, *args, **kwargs):
        self.events.append(("container", args, kwargs))
        return nullcontext()

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record

    def text_area(self, *args, **kwargs):
        self.events.append(("text_area", args, kwargs))
        return self.session_state.get(kwargs["key"], "")


class StrangeNewWorldsRealWorldBrowserTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame(
            {
                "pl_name": ["Complete b", "No mass b", "No orbit b", "Zero mass b", "Complete b", "Far b"],
                "pl_bmasse": [1.0, None, 2.0, 0.0, 9.0, 120.0],
                "pl_orbsmax": [1.0, 0.2, None, 0.4, 9.0, 4.0],
                "pl_eqt": [300, 400, 500, 600, 700, 800],
            }
        )

    def test_pool_requires_a_name_mass_and_orbital_distance(self):
        eligible = strange_new_worlds._eligible_browser_planets(self.data)

        self.assertEqual(eligible["pl_name"].tolist(), ["Complete b", "Far b"])
        self.assertEqual(eligible.columns.tolist(), ["pl_name", "pl_bmasse", "pl_orbsmax"])

    def test_first_planet_counts_and_three_distinct_planets_are_preferred(self):
        eligible = pd.DataFrame(
            {
                "pl_name": ["A b", "B b", "C b", "D b"],
                "pl_bmasse": [1.0, 2.0, 3.0, 4.0],
                "pl_orbsmax": [0.2, 0.5, 1.0, 2.0],
            }
        )
        state = {}

        first = strange_new_worlds._choose_browser_planet(eligible, rng=random.Random(2))
        state[strange_new_worlds._BROWSER_PLANET_KEY] = first
        self.assertEqual(strange_new_worlds._record_browsed_planet(state, first), [first])
        second = strange_new_worlds._show_another_browser_planet(eligible, state, rng=random.Random(3))
        third = strange_new_worlds._show_another_browser_planet(eligible, state, rng=random.Random(4))

        self.assertEqual(len(state[strange_new_worlds._BROWSER_SEEN_KEY]), 3)
        self.assertEqual(len({first, second, third}), 3)

    def test_screen_blocks_progress_until_three_distinct_planets(self):
        events, state = [], {}
        eligible_data = pd.DataFrame(
            {
                "pl_name": ["A b", "B b", "C b"],
                "pl_bmasse": [1.0, 10.0, 100.0],
                "pl_orbsmax": [0.1, 1.0, 10.0],
            }
        )
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "completion_gate", lambda complete: events.append(("gate", (complete,), {}))),
        ):
            strange_new_worlds.render_lesson(eligible_data, 4, object())

        self.assertIn(("gate", (False,), {}), events)
        self.assertIn("notice", [event[0] for event in events])
        self.assertNotIn("text_area", [event[0] for event in events])
        self.assertEqual(len(state[strange_new_worlds._BROWSER_SEEN_KEY]), 1)

    def test_profile_is_limited_to_the_two_core_variables(self):
        events, state = [], {}
        planet = pd.Series({"pl_name": "Example b", "pl_bmasse": 1.0, "pl_orbsmax": 0.3})
        with patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)):
            strange_new_worlds._render_browser_profile(planet)

        rendered = " ".join(str(arguments) for _, arguments, _ in events)
        self.assertIn("Mass:", rendered)
        self.assertIn("Orbital distance:", rendered)
        self.assertNotIn("Temperature", rendered)
        self.assertNotIn("Size", rendered)
        self.assertNotIn("year length", rendered.lower())

    def test_facilitator_guidance_matches_the_browser_boundary(self):
        note = strange_new_worlds.TEACHER_NOTE_OVERRIDES[4]
        background = strange_new_worlds.TEACHER_BACKGROUNDS[4]

        self.assertEqual(note["title"], "Meet some real worlds")
        self.assertIn("three distinct", note["purpose"])
        self.assertIn("not a representative sample", note["misconceptions"])
        self.assertIn("only mass and orbital distance", background)

        source = Path("experiences/strange_new_worlds.py").read_text()
        screen_four = source.split("elif part == 4:", 1)[1].split("elif part == 5:", 1)[0].lower()
        self.assertIn("those systems showed us that planetary systems can surprise us", screen_four)
        self.assertIn("inspect a few real detected planets yourself", screen_four)
        self.assertNotIn("holiday", screen_four)
        self.assertNotIn("destination", screen_four)
        self.assertNotIn("filter", screen_four)

    def test_prediction_is_required_after_three_distinct_planets_and_uses_session_state(self):
        events = []
        state = {
            strange_new_worlds._BROWSER_PLANET_KEY: "A b",
            strange_new_worlds._BROWSER_SEEN_KEY: ["A b", "B b", "C b"],
        }
        data = pd.DataFrame(
            {"pl_name": ["A b"], "pl_bmasse": [1.0], "pl_orbsmax": [1.0]}
        )
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "completion_gate", lambda complete: events.append(("gate", (complete,), {}))),
        ):
            strange_new_worlds.render_lesson(data, 4, object())

        text_area = next(event for event in events if event[0] == "text_area")
        self.assertEqual(text_area[2]["key"], strange_new_worlds._POPULATION_PREDICTION_KEY)
        self.assertEqual(text_area[2]["persist_state"], "session")
        self.assertIn(("gate", (False,), {}), events)

        state[strange_new_worlds._POPULATION_PREDICTION_KEY] = "I expect a wide spread of planets."
        events.clear()
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events, state)),
            patch.object(strange_new_worlds, "notice_prompt", lambda prompt: events.append(("notice", (prompt,), {}))),
            patch.object(strange_new_worlds, "completion_gate", lambda complete: events.append(("gate", (complete,), {}))),
        ):
            strange_new_worlds.render_lesson(data, 4, object())

        self.assertNotIn(("gate", (False,), {}), events)
        self.assertEqual(state[strange_new_worlds._POPULATION_PREDICTION_KEY], "I expect a wide spread of planets.")


if __name__ == "__main__":
    unittest.main()
