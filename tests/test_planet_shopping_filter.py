"""Stage 3 filtering checks for Planet Shopping."""

import unittest

import pandas as pd

from experiences.planet_shopping import (
    _filter_distance_light_years,
    _known_distance_population,
    _split_temperature_groups,
    _temperature_candidates,
)


class PlanetShoppingTemperatureFilterTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
