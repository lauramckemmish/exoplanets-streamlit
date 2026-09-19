"""Portable manifest and stable-launch tests."""

from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch

from experiences import portfolio, router
from tools.portfolio_metadata_validator import load_manifest, validate_manifest


MANIFEST_PATH = Path(__file__).resolve().parent.parent / "portfolio-manifest.json"


class PortfolioPublicationTests(unittest.TestCase):
    def test_manifest_is_valid_against_the_v1_validator(self):
        self.assertEqual(validate_manifest(load_manifest(MANIFEST_PATH)), [])

    def test_manifest_ids_and_launches_match_the_public_mapping(self):
        manifest = load_manifest(MANIFEST_PATH)
        published = {entry["experience_id"]: entry for entry in manifest["experiences"]}
        self.assertEqual(set(published), {entry.experience_id for entry in portfolio.DESTINATIONS})
        for experience_id, entry in published.items():
            with self.subTest(experience_id=experience_id):
                self.assertEqual(entry["launch"]["url"], portfolio.launch_url(experience_id))

    def test_each_guided_public_id_uses_existing_catalogue_selection(self):
        for destination in portfolio.DESTINATIONS:
            if destination.collection != "experience":
                continue
            with self.subTest(experience_id=destination.experience_id):
                with patch.object(router, "select_catalog_experience") as select:
                    self.assertTrue(router.select_portfolio_experience(destination.experience_id))
                select.assert_called_once_with(destination.catalogue_name)

    def test_data_lab_public_id_uses_existing_explore_selection(self):
        with patch.object(router, "select_explore_resource") as select:
            self.assertTrue(router.select_portfolio_experience("planets-beyond/exoplanet-data-lab"))
        select.assert_called_once_with("Exoplanet Data Lab")

    def test_unknown_public_id_fails_without_changing_local_navigation(self):
        with patch.object(router, "select_catalog_experience") as select_experience, patch.object(router, "select_explore_resource") as select_explore:
            self.assertFalse(router.select_portfolio_experience("planets-beyond/not-a-real-experience"))
        select_experience.assert_not_called()
        select_explore.assert_not_called()

    def test_public_ids_are_stable_and_do_not_contain_local_route_fields(self):
        for destination in portfolio.DESTINATIONS:
            self.assertNotIn("app_experience", destination.experience_id)
            self.assertNotIn("pathway", destination.experience_id)


if __name__ == "__main__":
    unittest.main()
