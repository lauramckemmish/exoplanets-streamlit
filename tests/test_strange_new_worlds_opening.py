"""Focused checks for the rebuilt opening of Strange New Worlds."""

import unittest

from experiences.strange_new_worlds import STEP_LABELS, _format_solar_system_table


class StrangeNewWorldsOpeningTests(unittest.TestCase):
    def test_solar_system_table_is_in_orbital_order_with_display_rounding(self):
        table = _format_solar_system_table()

        self.assertEqual(list(table.columns), ["Planet", "Mass (Earth = 1)", "Orbital distance (AU)"])
        self.assertEqual(table.to_dict("records"), [
            {"Planet": "Mercury", "Mass (Earth = 1)": "0.0553", "Orbital distance (AU)": "0.387"},
            {"Planet": "Venus", "Mass (Earth = 1)": "0.815", "Orbital distance (AU)": "0.723"},
            {"Planet": "Earth", "Mass (Earth = 1)": "1", "Orbital distance (AU)": "1"},
            {"Planet": "Mars", "Mass (Earth = 1)": "0.107", "Orbital distance (AU)": "1.52"},
            {"Planet": "Jupiter", "Mass (Earth = 1)": "318", "Orbital distance (AU)": "5.20"},
            {"Planet": "Saturn", "Mass (Earth = 1)": "95.2", "Orbital distance (AU)": "9.54"},
            {"Planet": "Uranus", "Mass (Earth = 1)": "14.5", "Orbital distance (AU)": "19.2"},
            {"Planet": "Neptune", "Mass (Earth = 1)": "17.1", "Orbital distance (AU)": "30.1"},
        ])

    def test_first_screen_labels_preserve_later_navigation(self):
        self.assertEqual(STEP_LABELS[:3], [
            "Welcome",
            "1 · Our Solar System as data",
            "2 · Could Jupiter be here?",
        ])


if __name__ == "__main__":
    unittest.main()
