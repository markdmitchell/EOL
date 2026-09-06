import os
import tempfile
import unittest

from db.database import Database
from services.nvd_cpe import ingest_nvd_cpe_into_db, parse_cpe_23


class TestNVDCPE(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")  # noqa: SIM115
        self.tmp_file.close()
        self.db = Database(db_path=self.tmp_file.name)

    def tearDown(self):
        del self.db
        try:
            if os.path.exists(self.tmp_file.name):
                os.remove(self.tmp_file.name)
        except OSError:
            pass

    def test_parse_cpe_23(self):
        cpe_str = "cpe:2.3:a:oracle:database_server:19c:*:*:*:*:*:*:*"
        parsed = parse_cpe_23(cpe_str)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["type"], "Application")
        self.assertEqual(parsed["vendor"], "Oracle")
        self.assertEqual(parsed["product"], "Database Server")
        self.assertEqual(parsed["version"], "19c")

    def test_ingest_cpe_records(self):
        mock_records = [
            {
                "type": "Application",
                "vendor": "Atlassian",
                "product": "Jira",
                "version": "9.12.0",
                "update": "",
                "raw_cpe": "cpe:2.3:a:atlassian:jira:9.12.0:*:*:*:*:*:*:*",
                "title": "Atlassian Jira 9.12.0",
                "cpe_id": "TEST-CPE-ID-123",
                "last_modified": "2024-01-01"
            }
        ]
        count = ingest_nvd_cpe_into_db(db=self.db, records=mock_records)
        self.assertEqual(count, 1)

        product = self.db.get_product_by_slug("atlassian-jira")
        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Jira")

if __name__ == "__main__":
    unittest.main()
