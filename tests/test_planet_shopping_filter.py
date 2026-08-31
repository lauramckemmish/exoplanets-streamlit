"""Stage 3 filtering checks for Planet Shopping."""

import unittest

import pandas as pd

from experiences.planet_shopping import (
    STAGE_LABELS,
    _UNKNOWN_TEMPERATURE_CONTROL_KEY,
    _UNKNOWN_TEMPERATURE_DECISION_KEY,
    _UNKNOWN_TEMPERATURE_OPTIONS,
    _filter_distance_light_years,
    _initialise_unknown_temperature_control,
    _known_distance_population,
    _split_temperature_groups,
    _temperature_candidates,
)


class PlanetShoppingTemperatureFilterTests(unittest.TestCase):
    def test_unknown_temperature_control_is_separate_and_restores_durable_decision(self):
        state = {_UNKNOWN_TEMPERATURE_DECISION_KEY: _UNKNOWN_TEMPERATURE_OPTIONS[1]}

        control_value = _initialise_unknown_temperature_control(state)

        self.assertNotEqual(_UNKNOWN_TEMPERATURE_CONTROL_KEY, _UNKNOWN_TEMPERATURE_DECISION_KEY)
        self.assertEqual(control_value, _UNKNOWN_TEMPERATURE_OPTIONS[1])
        state[_UNKNOWN_TEMPERATURE_DECISION_KEY] = control_value
        self.assertEqual(state[_UNKNOWN_TEMPERATURE_DECISION_KEY], _UNKNOWN_TEMPERATURE_OPTIONS[1])

    def test_stage_shell_matches_established_six_screen_sequence(self):
        self.assertEqual(
            STAGE_LABELS,
            ["Launch", "Meet a Planet", "Distance", "Temperature", "Combine", "Data Science"],
        )

    def test_temperature_groups_partition_every_catalogue_record(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Cool", "In range", "Warm", "Unknown"],
                "pl_eqt": [250.0, 273.15, 330.0, None],
            }
        )

        matches, does_not_match, unknown = _split_temperature_groups(data, (0, 30))

        self.assertEqual(matches["pl_name"].tolist(), ["In range"])
        self.assertEqual(does_not_match["pl_name"].tolist(), ["Cool", "Warm"])
        self.assertEqual(unknown["pl_name"].tolist(), ["Unknown"])
        self.assertEqual(len(matches) + len(does_not_match) + len(unknown), len(data))

    def test_distance_filter_uses_light_years_and_omits_missing_distances(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Near", "Far", "No distance"],
                "sy_dist": [1.0, 4.0, None],
                "pl_eqt": [273.15, 273.15, 273.15],
            }
        )

        population = _known_distance_population(data)
        filtered = _filter_distance_light_years(population, 10)

        self.assertEqual(population["pl_name"].tolist(), ["Near", "Far"])
        self.assertEqual(filtered["pl_name"].tolist(), ["Near"])
        self.assertEqual(data.loc[0, "sy_dist"], 1.0)

    def test_temperature_filter_uses_the_distance_filtered_population(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Near match", "Near unknown", "Far match"],
                "sy_dist": [1.0, 1.5, 10.0],
                "pl_eqt": [273.15, None, 273.15],
            }
        )
        distance_filtered = _filter_distance_light_years(_known_distance_population(data), 5)
        matches, does_not_match, unknown = _split_temperature_groups(distance_filtered, (0, 30))

        self.assertEqual(matches["pl_name"].tolist(), ["Near match"])
        self.assertEqual(does_not_match["pl_name"].tolist(), [])
        self.assertEqual(unknown["pl_name"].tolist(), ["Near unknown"])
        self.assertEqual(len(matches) + len(does_not_match) + len(unknown), len(distance_filtered))
        self.assertEqual(len(_temperature_candidates(matches, unknown, True)), 2)
        self.assertEqual(len(_temperature_candidates(matches, unknown, False)), 1)

    def test_temperature_groups_can_use_the_full_population_independently(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Near match", "Far match", "Unknown"],
                "sy_dist": [1.0, 10.0, 1.5],
                "pl_eqt": [273.15, 273.15, None],
            }
        )

        matches, does_not_match, unknown = _split_temperature_groups(data, (0, 30))

        self.assertEqual(matches["pl_name"].tolist(), ["Near match", "Far match"])
        self.assertEqual(does_not_match["pl_name"].tolist(), [])
        self.assertEqual(unknown["pl_name"].tolist(), ["Unknown"])


if __name__ == "__main__":
    unittest.main()
