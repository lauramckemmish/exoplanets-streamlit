"""Catalogue-level navigation checks that do not require Streamlit to run."""

import unittest

from experiences import catalog


class PublicDestinationCatalogueTests(unittest.TestCase):
    def test_guided_experiences_and_explore_resources_are_separate(self):
        experience_names = {entry["name"] for entry in catalog.experience_catalog()}
        explore_names = {entry["name"] for entry in catalog.explore_catalog()}

        self.assertNotIn("Exoplanet Data Lab", experience_names)
        self.assertEqual(
            explore_names,
            {
                "How We Found Other Worlds",
                "How Do We Find a Planet We Can't See?",
                "Exoplanet Data Lab",
            },
        )

    def test_data_lab_explore_resource_reuses_the_existing_route(self):
        resource = catalog.get_explore_resource("Exoplanet Data Lab")
        self.assertEqual(resource["app_experience"], "Exoplanet Data Laboratory")

    def test_placeholder_explore_routes_are_enabled_and_resolvable(self):
        for name in (
            "How We Found Other Worlds",
            "How Do We Find a Planet We Can't See?",
        ):
            resource = catalog.get_explore_resource(name)
            self.assertIsNotNone(resource)
            self.assertEqual(
                catalog.get_explore_resource_for_route(resource["app_experience"])["name"],
                name,
            )


if __name__ == "__main__":
    unittest.main()
