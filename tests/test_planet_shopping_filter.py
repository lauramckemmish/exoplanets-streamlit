"""Stage 3 filtering checks for Planet Shopping."""

import unittest

import pandas as pd

from experiences.planet_shopping import _split_temperature_groups


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


if __name__ == "__main__":
    unittest.main()
