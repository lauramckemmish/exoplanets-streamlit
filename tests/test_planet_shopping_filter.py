"""Stage 3 filtering checks for Planet Shopping."""

import unittest

import pandas as pd

from experiences.planet_shopping import (
    PARSEC_TO_LIGHT_YEARS,
    STAGE_LABELS,
    _APPLIED_DISTANCE_KEY,
    _APPLIED_DESTINATION_KEY,
    _DISTANCE_CONTROL_KEY,
    _DISTANCE_INTERACTED_KEY,
    _format_travel_years,
    _initialise_distance_control,
    _record_distance_interaction,
    _TEMPERATURE_DEFAULT_RANGE_C,
    _passenger_plane_travel_years,
    _distance_profile,
    _planet_display_value,
    _random_planet_name,
    _temperature_profile,
    _UNKNOWN_TEMPERATURE_OPTIONS,
    _combine_groups,
    _candidate_names,
    _filter_destination_candidates,
    _initialise_destination_control,
    _record_destination_selection,
    _UNKNOWN_TEMPERATURE_CONTROL_KEY,
    _UNKNOWN_TEMPERATURE_DECISION_KEY,
    _filter_distance_light_years,
    _initialise_unknown_temperature_control,
    _known_distance_population,
    _split_temperature_groups,
)


class PlanetShoppingTemperatureFilterTests(unittest.TestCase):
    def test_passenger_plane_anchor_uses_approximate_years_per_light_year(self):
        self.assertEqual(_passenger_plane_travel_years(1), 1_200_000)
        self.assertEqual(_format_travel_years(_passenger_plane_travel_years(100)), "120 million years")

    def test_fresh_temperature_range_is_deliberately_hot(self):
        self.assertEqual(_TEMPERATURE_DEFAULT_RANGE_C, (1_000, 2_000))

    def test_random_planet_name_comes_from_named_catalogue_and_changes_when_possible(self):
        data = pd.DataFrame({"pl_name": ["Planet A", "Planet B", None]})

        selected = _random_planet_name(data, current="Planet A")

        self.assertEqual(selected, "Planet B")

    def test_profile_values_use_learner_facing_units(self):
        self.assertEqual(_temperature_profile(273.15)[0], "0 °C")
        self.assertEqual(_distance_profile(1.0)[0], f"{PARSEC_TO_LIGHT_YEARS:.0f} light-years")

    def test_temperature_profile_uses_distinct_high_temperature_bands(self):
        self.assertEqual(_temperature_profile(373.15)[1], "Hotter than a summer day on Earth.")
        self.assertEqual(_temperature_profile(773.15)[1], "Very hot.")
        self.assertEqual(_temperature_profile(1272.15)[1], "Extremely hot.")
        self.assertEqual(_temperature_profile(1274.15)[1], "Over 1,000 °C — extraordinarily hot.")

    def test_profile_missing_value_is_explicitly_unknown(self):
        value, interpretation = _planet_display_value(None, _temperature_profile)

        self.assertEqual(value, "Unknown")
        self.assertEqual(interpretation, "We don't know this one yet.")

    def test_distance_result_stays_hidden_until_slider_moves_and_choice_is_durable(self):
        state = {}

        self.assertEqual(_initialise_distance_control(state), 500)
        self.assertNotIn(_DISTANCE_INTERACTED_KEY, state)
        self.assertFalse(_record_distance_interaction(state, 500))
        state[_DISTANCE_CONTROL_KEY] = 600
        self.assertTrue(_record_distance_interaction(state, 600))
        self.assertEqual(state[_APPLIED_DISTANCE_KEY], 600)
        self.assertTrue(state[_DISTANCE_INTERACTED_KEY])

    def test_unknown_temperature_control_is_separate_and_restores_durable_decision(self):
        state = {_UNKNOWN_TEMPERATURE_DECISION_KEY: _UNKNOWN_TEMPERATURE_OPTIONS[1]}

        control_value = _initialise_unknown_temperature_control(state)

        self.assertNotEqual(_UNKNOWN_TEMPERATURE_CONTROL_KEY, _UNKNOWN_TEMPERATURE_DECISION_KEY)
        self.assertEqual(control_value, _UNKNOWN_TEMPERATURE_OPTIONS[1])
        state[_UNKNOWN_TEMPERATURE_DECISION_KEY] = control_value
        self.assertEqual(state[_UNKNOWN_TEMPERATURE_DECISION_KEY], _UNKNOWN_TEMPERATURE_OPTIONS[1])

    def test_stage_shell_matches_established_seven_screen_sequence(self):
        self.assertEqual(
            STAGE_LABELS,
            [
                "Launch", "Meet a Planet", "Distance", "Temperature", "Combine",
                "Choose Your Destination", "Data Science",
            ],
        )

    def test_destination_selection_is_durable_and_must_be_a_shortlist_member(self):
        names = ["Planet A", "Planet B"]
        state = {}

        self.assertIsNone(_initialise_destination_control(state, names))
        self.assertFalse(_record_destination_selection(state, None))
        self.assertTrue(_record_destination_selection(state, "Planet B"))
        self.assertEqual(state[_APPLIED_DESTINATION_KEY], "Planet B")

        restored = {_APPLIED_DESTINATION_KEY: "Planet B"}
        self.assertEqual(_initialise_destination_control(restored, names), "Planet B")

    def test_destination_control_discards_stale_selection(self):
        state = {_APPLIED_DESTINATION_KEY: "Not a candidate"}

        self.assertIsNone(_initialise_destination_control(state, ["Planet A"]))
        self.assertIsNone(state[_APPLIED_DESTINATION_KEY])

    def test_destination_shortlist_has_only_named_catalogue_planets(self):
        candidates = pd.DataFrame({"pl_name": [f"Planet {i}" for i in range(20)] + [None]})

        self.assertEqual(len(_candidate_names(candidates)), 20)
        self.assertEqual(_candidate_names(candidates.iloc[0:0]), [])

    def test_destination_optional_filters_use_and_logic_and_missing_policy(self):
        candidates = pd.DataFrame(
            {
                "pl_name": ["Both", "Size only", "Unknown size", "Wrong stars"],
                "pl_rade": [1.0, 1.0, None, 1.0],
                "sy_snum": [1, 2, 1, 2],
                "pl_orbper": [365.0, 365.0, 365.0, 365.0],
                "sy_pnum": [2, 2, 2, 2],
            }
        )

        safe = _filter_destination_candidates(
            candidates, size_range=(0.9, 1.1), stars_range=(1, 1), keep_unknowns=False
        )
        risk = _filter_destination_candidates(
            candidates, size_range=(0.9, 1.1), stars_range=(1, 1), keep_unknowns=True
        )

        self.assertEqual(safe["pl_name"].tolist(), ["Both"])
        self.assertEqual(risk["pl_name"].tolist(), ["Both", "Unknown size"])

    def test_destination_year_and_system_planet_filters_are_optional_and_live(self):
        candidates = pd.DataFrame(
            {
                "pl_name": ["Fast", "Slow", "Many"],
                "pl_rade": [1.0, 1.0, 1.0],
                "sy_snum": [1, 1, 1],
                "pl_orbper": [30.0, 400.0, 30.0],
                "sy_pnum": [2, 2, 5],
            }
        )

        filtered = _filter_destination_candidates(
            candidates,
            year_range=(1, 100),
            planets_range=(1, 2),
            keep_unknowns=False,
        )

        self.assertEqual(filtered["pl_name"].tolist(), ["Fast"])

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

    def test_combine_intersection_is_distinct_from_independent_temperature_filter(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Near match", "Near unknown", "Far match"],
                "sy_dist": [1.0, 1.5, 10.0],
                "pl_eqt": [273.15, None, 273.15],
            }
        )
        distance, temperature, known_both, distance_unknown, candidates = _combine_groups(
            data, 5, (0, 30), True
        )

        self.assertEqual(len(distance), 2)
        self.assertEqual(len(temperature), 2)
        self.assertEqual(known_both["pl_name"].tolist(), ["Near match"])
        self.assertEqual(distance_unknown["pl_name"].tolist(), ["Near unknown"])
        self.assertEqual(candidates["pl_name"].tolist(), ["Near match", "Near unknown"])

    def test_combine_separates_counts_and_applies_risk_policy(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Near both", "Near unknown", "Far both", "Near cold"],
                "sy_dist": [1.0, 1.5, 10.0, 1.2],
                "pl_eqt": [273.15, None, 273.15, 350.0],
            }
        )

        distance, temperature, known_both, distance_unknown, risk_candidates = _combine_groups(
            data, 5, (0, 30), True
        )
        _, _, _, _, safe_candidates = _combine_groups(data, 5, (0, 30), False)

        self.assertEqual(len(distance), 3)
        self.assertEqual(len(temperature), 2)
        self.assertEqual(known_both["pl_name"].tolist(), ["Near both"])
        self.assertEqual(distance_unknown["pl_name"].tolist(), ["Near unknown"])
        self.assertEqual(risk_candidates["pl_name"].tolist(), ["Near both", "Near unknown"])
        self.assertEqual(safe_candidates["pl_name"].tolist(), ["Near both"])

    def test_combine_keeps_missing_values_unknown_and_shortlist_real_survivors(self):
        data = pd.DataFrame(
            {
                "pl_name": ["Unknown temperature", "No distance", None],
                "sy_dist": [1.0, None, 1.0],
                "pl_eqt": [None, 273.15, 273.15],
            }
        )

        _, _, known_both, distance_unknown, candidates = _combine_groups(data, 5, (0, 30), True)

        self.assertEqual(known_both["pl_name"].tolist(), [None])
        self.assertEqual(distance_unknown["pl_name"].tolist(), ["Unknown temperature"])
        self.assertEqual(_candidate_names(candidates), ["Unknown temperature"])

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
