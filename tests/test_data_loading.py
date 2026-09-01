"""Deterministic loading and fallback checks without contacting NASA."""

import unittest
from unittest.mock import patch

import pandas as pd

import data


def raw_catalogue(*names: str) -> pd.DataFrame:
    """Return the minimum valid archive-shaped data for loader tests."""

    return pd.DataFrame(
        {
            "pl_name": names,
            "ra": list(range(len(names))),
            "dec": list(range(len(names))),
        }
    )


class CatalogueLoadingTests(unittest.TestCase):
    def setUp(self):
        data._prepare_live_catalogue.clear()
        data._prepare_sample_catalogue.clear()

    @patch("data.load_sample")
    @patch("data.load_live")
    def test_live_catalogue_returns_live_source_metadata(self, mock_live, mock_sample):
        mock_live.return_value = raw_catalogue("Live One", "Live Two")

        result = data.load_catalogue()

        self.assertTrue(result.source.is_live)
        self.assertEqual(result.source.kind, "live")
        self.assertEqual(result.source.label, "Live NASA Exoplanet Archive")
        self.assertEqual(result.source.provenance, "NASA Exoplanet Archive")
        self.assertEqual(len(result.data), 2)
        mock_sample.assert_not_called()

    @patch("data.load_sample")
    @patch("data.load_live")
    def test_live_failure_uses_bundled_sample_with_its_own_metadata(self, mock_live, mock_sample):
        mock_live.side_effect = data.LiveCatalogueError("test timeout")
        mock_sample.return_value = raw_catalogue("Bundled One")

        with self.assertLogs("data", level="WARNING"):
            result = data.load_catalogue()

        self.assertFalse(result.source.is_live)
        self.assertEqual(result.source.kind, "bundled")
        self.assertEqual(result.source.label, "Bundled notebook sample")
        self.assertEqual(len(result.data), 1)
        mock_sample.assert_called_once()

    @patch("data.load_sample")
    @patch("data.load_live")
    def test_unusable_live_response_uses_bundled_sample(self, mock_live, mock_sample):
        mock_live.return_value = pd.DataFrame({"unexpected": ["response"]})
        mock_sample.return_value = raw_catalogue("Bundled One", "Bundled Two", "Bundled Three")

        with self.assertLogs("data", level="WARNING"):
            result = data.load_catalogue()

        self.assertEqual(result.source.kind, "bundled")
        self.assertEqual(len(result.data), 3)

    @patch("data._prepare_catalogue", wraps=data._prepare_catalogue)
    @patch("data.load_sample")
    @patch("data.load_live")
    def test_repeated_catalogue_loads_reuse_preparation(self, mock_live, mock_sample, mock_prepare):
        raw = raw_catalogue("Cached One", "Cached Two")
        mock_live.return_value = raw

        first = data.load_catalogue()
        second = data.load_catalogue()

        self.assertEqual(mock_prepare.call_count, 1)
        self.assertTrue(first.source.is_live)
        self.assertTrue(second.source.is_live)
        self.assertEqual(first.data["pl_name"].tolist(), ["Cached One", "Cached Two"])
        self.assertEqual(second.data["pl_name"].tolist(), ["Cached One", "Cached Two"])
        mock_sample.assert_not_called()


if __name__ == "__main__":
    unittest.main()
