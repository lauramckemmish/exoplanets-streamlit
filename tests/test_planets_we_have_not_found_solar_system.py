"""Focused checks for Year 10's Solar System reference screen."""

import unittest
from unittest.mock import patch

import pandas as pd

from experiences import planets_we_have_not_found


class _StreamlitRecorder:
    def __init__(self, events):
        self.events = events

    def __getattr__(self, name):
        def record(*args, **kwargs):
            self.events.append((name, args, kwargs))

        return record


class _Dependencies:
    def __init__(self, events):
        self.graph_questions = lambda *args: events.append(("graph_questions", args, {}))
        self.response_box = lambda *args: events.append(("response_box", args, {}))
        self.key_idea = lambda *args: events.append(("key_idea", args, {}))


class PlanetsWeHaveNotFoundSolarSystemTests(unittest.TestCase):
    def test_solar_system_stage_renders_authoritative_reference_data_and_comparison_action(self):
        events = []
        with (
            patch.object(planets_we_have_not_found, "st", _StreamlitRecorder(events)),
            patch.object(planets_we_have_not_found, "render_facilitator_support"),
        ):
            planets_we_have_not_found.render_lesson(pd.DataFrame(), 1, _Dependencies(events))

        names = [event[0] for event in events]
        self.assertIn("dataframe", names)
        self.assertIn("graph_questions", names)
        self.assertIn("response_box", names)
        self.assertIn("key_idea", names)
        self.assertNotIn("plotly_chart", names)
        self.assertEqual(events[names.index("response_box")][1][0], 1)

        table = events[names.index("dataframe")][1][0]
        self.assertEqual(
            list(table.columns),
            ["Planet", "Distance from the Sun (AU)", "Mass (Earth = 1)"],
        )
        self.assertEqual(table.loc[table["Planet"] == "Earth", "Mass (Earth = 1)"].iloc[0], 1.0)
        self.assertEqual(table.loc[table["Planet"] == "Jupiter", "Distance from the Sun (AU)"].iloc[0], 5.203)


if __name__ == "__main__":
    unittest.main()
