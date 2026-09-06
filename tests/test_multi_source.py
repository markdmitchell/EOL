import os
import tempfile
import unittest

from db.database import Database
from services.multi_source import MultiSourceService


class TestMultiSourceIntegration(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")  # noqa: SIM115
        self.tmp_file.close()
        self.db = Database(db_path=self.tmp_file.name)
        self.ms_svc = MultiSourceService(db=self.db)

    def tearDown(self):
        del self.db
        del self.ms_svc
        try:
            if os.path.exists(self.tmp_file.name):
                os.remove(self.tmp_file.name)
        except OSError:
            pass

    def test_register_sources_and_vendor_catalog(self):
        sources_count = self.ms_svc.register_all_sources()
        self.assertGreaterEqual(sources_count, 24)

        all_sources = self.db.get_all_data_sources()
        self.assertEqual(len(all_sources), sources_count)

        vendor_count = self.ms_svc.ingest_vendor_lifecycle_catalog()
        self.assertGreaterEqual(vendor_count, 8)

        # Verify specific vendor product lifecycles
        win_server = self.db.get_product_by_slug("windows-server")
        self.assertIsNotNone(win_server)
        self.assertEqual(win_server["label"], "Microsoft Windows Server")

        rhel = self.db.get_product_by_slug("rhel")
        self.assertIsNotNone(rhel)

        # Verify provenance linkage to data_sources table
        prov = self.db.get_provenance("product", win_server["id"])
        self.assertGreater(len(prov), 0)
        self.assertEqual(prov[0]["source_name"], "Microsoft Lifecycle")

if __name__ == "__main__":
    unittest.main()
