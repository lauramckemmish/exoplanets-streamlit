"""Catalogue-level navigation checks that do not require Streamlit to run."""

import unittest

from experiences import catalog


class PublicDestinationCatalogueTests(unittest.TestCase):
    def test_all_experiences_are_publicly_enabled(self):
        self.assertEqual(
            catalog.enabled_experience_names(),
            tuple(entry["name"] for entry in catalog.EXPERIENCES),
        )

    def test_guided_experiences_and_explore_resources_are_separate(self):
        experience_names = {entry["name"] for entry in catalog.experience_catalog()}
        explore_names = {entry["name"] for entry in catalog.explore_catalog()}

        self.assertEqual(experience_names, {entry["name"] for entry in catalog.EXPERIENCES})
        self.assertEqual(explore_names, {entry["name"] for entry in catalog.EXPLORE_RESOURCES})

    def test_data_lab_explore_resource_reuses_the_existing_route(self):
        resource = catalog.get_explore_resource("Exoplanet Data Lab")
        self.assertEqual(resource["app_experience"], "Exoplanet Data Laboratory")

    def test_all_explore_resources_are_available(self):
        for resource in catalog.EXPLORE_RESOURCES:
            self.assertIsNotNone(catalog.get_explore_resource(resource["name"]))


if __name__ == "__main__":
    unittest.main()
