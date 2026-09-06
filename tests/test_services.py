import os
import tempfile
import unittest

from db.database import Database
from services.csv_importer import CSVImporter
from services.search import SearchService


class TestDatabaseAndServices(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")  # noqa: SIM115
        self.tmp_file.close()
        self.db = Database(db_path=self.tmp_file.name)
        self.search_svc = SearchService(db=self.db)
        self.csv_imp = CSVImporter(db=self.db)

    def tearDown(self):
        del self.db
        del self.search_svc
        del self.csv_imp
        try:
            if os.path.exists(self.tmp_file.name):
                os.remove(self.tmp_file.name)
        except OSError:
            pass

    def test_upsert_product_and_provenance(self):
        pid = self.db.upsert_product(
            slug="test-os",
            name="Test OS",
            label="Test OS",
            category="os",
            tags=["os", "linux"]
        )
        self.assertGreater(pid, 0)

        prov_id = self.db.add_provenance(
            entity_type="product",
            entity_id=pid,
            source_name="Official Vendor Spec",
            source_url="https://vendor.com/eol",
            license="MIT",
            confidence_score=0.98
        )
        self.assertGreater(prov_id, 0)

        prov_records = self.db.get_provenance("product", pid)
        self.assertEqual(len(prov_records), 1)
        self.assertEqual(prov_records[0]["source_name"], "Official Vendor Spec")

    def test_csv_importer_and_risk_calc(self):
        csv_data = (
            "Runtime / Platform,Version,Release Type,Deployment Environment,Release Date,End of Active Support,End of Life (EOL) Date,Lifecycle Phase,Days to EOL,Risk Level,Target Upgrade Path,Migration Action Status\n"
            "Node.js,18,LTS,Gateway-A,2022-04-19,2023-10-18,2025-04-30,End of Life,-494,CRITICAL (EOL),Node.js 22 LTS,In Progress\n"
            "Python,3.12,Standard,ML-Runner,2023-10-02,2025-04-02,2028-10-02,Active Support,757,LOW,Stay on Python 3.12,No Action Needed\n"
        )

        import io
        buf = io.StringIO(csv_data)
        count = self.csv_imp.import_inventory_csv(buf, source_name="Test CSV")
        self.assertEqual(count, 2)

        summary = self.search_svc.get_inventory_risk_summary()
        self.assertEqual(summary["total_items"], 2)
        self.assertEqual(summary["critical_eol_count"], 1)
        self.assertEqual(summary["low_risk_count"], 1)

if __name__ == "__main__":
    unittest.main()
