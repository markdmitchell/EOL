import os
import tempfile
import unittest

from db.database import Database
from services.enterprise_vendors import EnterpriseVendorService
from services.search import SearchService


class TestEnterpriseVendors(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.tmp_file.close()
        self.db = Database(db_path=self.tmp_file.name)
        self.ent_svc = EnterpriseVendorService(db=self.db)
        self.search_svc = SearchService(db=self.db)

    def tearDown(self):
        del self.db
        del self.ent_svc
        del self.search_svc
        try:
            if os.path.exists(self.tmp_file.name):
                os.remove(self.tmp_file.name)
        except OSError:
            pass

    def test_ingest_enterprise_suites(self):
        count = self.ent_svc.ingest_all_enterprise_suites()
        self.assertGreaterEqual(count, 15)

        # 1. Verify Atlassian Jira
        jira = self.db.get_product_by_slug("jira")
        self.assertIsNotNone(jira)
        self.assertEqual(jira["vendor"], "Atlassian")
        jira_cycles = self.db.get_release_cycles_for_product(jira["id"])
        self.assertGreaterEqual(len(jira_cycles), 4)

        # 2. Verify OpenText ALM / Quality Center
        alm = self.db.get_product_by_slug("opentext-alm")
        self.assertIsNotNone(alm)
        self.assertEqual(alm["vendor"], "OpenText / Micro Focus")

        # 3. Verify IBM WebSphere & DB2
        was = self.db.get_product_by_slug("websphere-app-server")
        self.assertIsNotNone(was)
        self.assertEqual(was["vendor"], "IBM Corporation")

        # 4. Verify SAP S/4HANA
        sap = self.db.get_product_by_slug("sap-s4hana")
        self.assertIsNotNone(sap)
        self.assertEqual(sap["vendor"], "SAP SE")

        # 5. Verify Cisco IOS-XE
        cisco = self.db.get_product_by_slug("cisco-ios-xe")
        self.assertIsNotNone(cisco)
        self.assertEqual(cisco["vendor"], "Cisco Systems")

        # 6. Verify Search Integration
        results = self.search_svc.search_catalog(query="Jira")
        self.assertGreaterEqual(len(results), 1)
        found_slugs = [r["product"]["slug"] for r in results]
        self.assertIn("jira", found_slugs)

if __name__ == "__main__":
    unittest.main()
