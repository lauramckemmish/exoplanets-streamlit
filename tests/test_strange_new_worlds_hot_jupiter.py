"""Focused checks for the Screen 2 hot-Jupiter prediction and reveal."""

import unittest
import inspect
from unittest.mock import patch

import pandas as pd

from experiences import strange_new_worlds


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))
        return record


class _Dependencies:
    def __init__(self, events, revealed):
        self.events = events
        self.revealed = revealed

    def hard_reveal(self, *args, **kwargs):
        self.events.append(("hard_reveal", args, kwargs))
        return self.revealed


class StrangeNewWorldsHotJupiterTests(unittest.TestCase):
    def _render(self, revealed):
        events = []
        dependencies = _Dependencies(events, revealed)
        with (
            patch.object(strange_new_worlds, "st", _StreamlitRecorder(events)),
            patch.object(strange_new_worlds, "predict_prompt", lambda prompt: events.append(("predict", (prompt,), {}))),
            patch.object(strange_new_worlds, "revise_prompt", lambda prompt: events.append(("revise", (prompt,), {}))),
        ):
            strange_new_worlds.render_lesson(pd.DataFrame(), 2, dependencies)
        return events

    def test_prediction_precedes_hidden_evidence(self):
        events = self._render(revealed=False)
        names = [event[0] for event in events]
        rendered_before_reveal = " ".join(
            str(event[1]) for event in events[:names.index("hard_reveal")]
        ).lower()

        self.assertLess(names.index("predict"), names.index("hard_reveal"))
        self.assertIn("planets around other stars", rendered_before_reveal)
        self.assertIn("called an **exoplanet**", rendered_before_reveal)
        self.assertIn("1995", rendered_before_reveal)
        self.assertIn("sun-like star", rendered_before_reveal)
        self.assertIn("giant planet", rendered_before_reveal)
        self.assertNotIn("dataframe", names)
        self.assertNotIn("revise", names)

    def test_reveal_shows_comparison_before_revision_prompt(self):
        events = self._render(revealed=True)
        names = [event[0] for event in events]

        self.assertLess(names.index("predict"), names.index("hard_reveal"))
        self.assertLess(names.index("hard_reveal"), names.index("dataframe"))
        self.assertLess(names.index("dataframe"), names.index("revise"))
        reveal_write_text = " ".join(
            str(event[1]) for event in events[names.index("dataframe") + 1:]
        )
        self.assertIn("Well. Our Solar System had not prepared us for that.", reveal_write_text)
        self.assertIn("If giant planets are easier to build farther from their star, what is this one doing here?", reveal_write_text)
        self.assertIn("One important possibility is **migration**", reveal_write_text)
        self.assertIn("not necessarily frozen", reveal_write_text)
        self.assertIn("The Solar System had given scientists a sensible story. Hot Jupiters meant that story needed some work.", reveal_write_text)
        self.assertLess(
            reveal_write_text.index("what is this one doing here?"),
            reveal_write_text.index("One important possibility is **migration**"),
        )

    def test_temperature_scale_appears_only_after_reveal(self):
        hidden = self._render(revealed=False)
        self.assertNotIn("bar_chart", [event[0] for event in hidden])

        revealed = self._render(revealed=True)
        names = [event[0] for event in revealed]
        self.assertIn("bar_chart", names)
        self.assertLess(names.index("dataframe"), names.index("bar_chart"))
        scale = next(event[1][0] for event in revealed if event[0] == "bar_chart")
        self.assertEqual(scale["Temperature (°C)"].tolist(), [430, 460, 660, 1000, 1175])
        rendered = " ".join(str(event[1]) for event in revealed)
        self.assertIn("roughly around a thousand degrees Celsius", rendered)
        self.assertIn("gas giant", rendered)
        self.assertIn("not a solid surface temperature", rendered)
        self.assertNotIn("exactly 1000", rendered)

    def test_temperature_context_is_not_added_to_browser_or_population_state(self):
        screen4_source = inspect.getsource(strange_new_worlds.render_lesson).split("elif part == 4:", 1)[1].split("elif part == 5:", 1)[0]
        self.assertNotIn("temperature", screen4_source.lower())

    def test_static_comparison_uses_expected_rounded_values(self):
        self.assertEqual(strange_new_worlds._hot_jupiter_comparison_table().to_dict("records"), [
            {"Planet and star": "Jupiter — Sun", "Mass (Earth = 1)": "318", "Distance from star (AU)": "5.20"},
            {"Planet and star": "Mercury — Sun", "Mass (Earth = 1)": "0.0553", "Distance from star (AU)": "0.387"},
            {"Planet and star": "51 Pegasi b — 51 Pegasi", "Mass (Earth = 1)": "≈146 (estimate)", "Distance from star (AU)": "0.052"},
        ])

    def test_migration_is_only_introduced_after_the_anomaly(self):
        source = inspect.getsource(strange_new_worlds.render_lesson)
        screen_two = source.split("elif part == 2:", 1)[1].split("elif part == 3:", 1)[0]

        self.assertLess(screen_two.index("Well. Our Solar System had not prepared us for that."), screen_two.index("**migration**"))
        before_reveal = screen_two.split("if hot_jupiter_revealed:", 1)[0].lower()
        self.assertNotIn("migration", before_reveal)


if __name__ == "__main__":
    unittest.main()
