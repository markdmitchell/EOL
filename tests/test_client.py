import unittest
from unittest.mock import patch, MagicMock
import json
import io

from endoflife import EndoflifeClient, ProductSummary, ProductDetails, ReleaseCycle
from endoflife.client import ResourceNotFoundError, EndoflifeAPIError

class TestEndoflifeClientMocked(unittest.TestCase):

    def setUp(self):
        self.client = EndoflifeClient()

    @patch("urllib.request.urlopen")
    def test_get_products(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "schema_version": "1.2.1",
            "result": [
                {
                    "name": "python",
                    "label": "Python",
                    "aliases": [],
                    "category": "lang",
                    "tags": ["lang"],
                    "uri": "https://endoflife.date/api/v1/products/python"
                }
            ]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        products = self.client.get_products()
        self.assertEqual(len(products), 1)
        self.assertIsInstance(products[0], ProductSummary)
        self.assertEqual(products[0].name, "python")
        self.assertEqual(products[0].label, "Python")

    @patch("urllib.request.urlopen")
    def test_get_product(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "schema_version": "1.2.1",
            "result": {
                "name": "python",
                "label": "Python",
                "category": "lang",
                "tags": ["lang"],
                "versionCommand": "python --version",
                "releases": [
                    {
                        "name": "3.14",
                        "releaseDate": "2025-10-07",
                        "isEol": False,
                        "eolFrom": "2030-10-31",
                        "isLts": False,
                        "latest": {
                            "name": "3.14.0",
                            "date": "2025-10-07"
                        }
                    }
                ]
            }
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        details = self.client.get_product("python")
        self.assertIsInstance(details, ProductDetails)
        self.assertEqual(details.name, "python")
        self.assertEqual(len(details.releases), 1)
        self.assertEqual(details.releases[0].name, "3.14")
        self.assertFalse(details.releases[0].is_eol)
        self.assertEqual(details.releases[0].latest.name, "3.14.0")

class TestEndoflifeClientLive(unittest.TestCase):

    def setUp(self):
        self.client = EndoflifeClient()

    def test_live_get_products(self):
        products = self.client.get_products()
        self.assertGreater(len(products), 100)
        names = [p.name for p in products]
        self.assertIn("python", names)
        self.assertIn("ubuntu", names)

    def test_live_get_product_python(self):
        details = self.client.get_product("python")
        self.assertEqual(details.name, "python")
        self.assertEqual(details.label, "Python")
        self.assertGreater(len(details.releases), 5)

    def test_live_get_not_found(self):
        with self.assertRaises(ResourceNotFoundError):
            self.client.get_product("non_existent_product_xyz123")

if __name__ == "__main__":
    unittest.main()
