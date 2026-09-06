import logging
from typing import Any

from db.database import Database

logger = logging.getLogger(__name__)

class EnterpriseVendorService:
    def __init__(self, db: Database | None = None):
        self.db = db or Database()

    def get_enterprise_vendor_catalog(self) -> list[dict[str, Any]]:
        return [
            # ==========================================
            # ATLASSIAN SUITE
            # ==========================================
            {
                "slug": "jira",
                "name": "Jira Software",
                "label": "Atlassian Jira Software (Data Center & Server)",
                "category": "server-app",
                "vendor": "Atlassian",
                "tags": ["atlassian", "jira", "issue-tracker", "agile", "enterprise"],
                "source_name": "Atlassian Support EOL Policy",
                "source_url": "https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html",
                "cycles": [
                    {"cycle": "10.0", "release_date": "2024-10-15", "eoas_date": "2026-10-15", "eol_date": "2026-10-15", "is_lts": False, "is_eol": False},
                    {"cycle": "9.12", "release_date": "2023-11-20", "eoas_date": "2025-11-20", "eol_date": "2025-11-20", "is_lts": True, "is_eol": False},
                    {"cycle": "9.4", "release_date": "2022-11-14", "eoas_date": "2024-11-14", "eol_date": "2024-11-14", "is_lts": True, "is_eol": True},
                    {"cycle": "8.20", "release_date": "2021-10-19", "eoas_date": "2023-10-19", "eol_date": "2023-10-19", "is_lts": True, "is_eol": True},
                    {"cycle": "8.5", "release_date": "2019-10-21", "eoas_date": "2021-10-21", "eol_date": "2021-10-21", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "jira-service-management",
                "name": "Jira Service Management",
                "label": "Atlassian Jira Service Management",
                "category": "server-app",
                "vendor": "Atlassian",
                "tags": ["atlassian", "jira", "itsm", "service-desk"],
                "source_name": "Atlassian Support EOL Policy",
                "source_url": "https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html",
                "cycles": [
                    {"cycle": "5.12", "release_date": "2023-11-20", "eoas_date": "2025-11-20", "eol_date": "2025-11-20", "is_lts": True, "is_eol": False},
                    {"cycle": "5.4", "release_date": "2022-11-14", "eoas_date": "2024-11-14", "eol_date": "2024-11-14", "is_lts": True, "is_eol": True},
                    {"cycle": "4.20", "release_date": "2021-10-19", "eoas_date": "2023-10-19", "eol_date": "2023-10-19", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "confluence",
                "name": "Confluence",
                "label": "Atlassian Confluence (Data Center & Server)",
                "category": "server-app",
                "vendor": "Atlassian",
                "tags": ["atlassian", "confluence", "wiki", "documentation"],
                "source_name": "Atlassian Support EOL Policy",
                "source_url": "https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html",
                "cycles": [
                    {"cycle": "8.9", "release_date": "2024-05-14", "eoas_date": "2026-05-14", "eol_date": "2026-05-14", "is_lts": False, "is_eol": False},
                    {"cycle": "8.5", "release_date": "2023-08-22", "eoas_date": "2025-08-22", "eol_date": "2025-08-22", "is_lts": True, "is_eol": False},
                    {"cycle": "7.19", "release_date": "2022-08-16", "eoas_date": "2024-08-16", "eol_date": "2024-08-16", "is_lts": True, "is_eol": True},
                    {"cycle": "7.13", "release_date": "2021-08-17", "eoas_date": "2023-08-17", "eol_date": "2023-08-17", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "bitbucket",
                "name": "Bitbucket Data Center",
                "label": "Atlassian Bitbucket Data Center",
                "category": "server-app",
                "vendor": "Atlassian",
                "tags": ["atlassian", "bitbucket", "git", "devops"],
                "source_name": "Atlassian Support EOL Policy",
                "source_url": "https://confluence.atlassian.com/support/atlassian-support-end-of-life-policy-201851003.html",
                "cycles": [
                    {"cycle": "8.19", "release_date": "2024-03-12", "eoas_date": "2026-03-12", "eol_date": "2026-03-12", "is_lts": True, "is_eol": False},
                    {"cycle": "8.9", "release_date": "2023-03-14", "eoas_date": "2025-03-14", "eol_date": "2025-03-14", "is_lts": True, "is_eol": False},
                    {"cycle": "7.21", "release_date": "2022-02-15", "eoas_date": "2024-02-15", "eol_date": "2024-02-15", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # OPENTEXT / MICRO FOCUS SUITE
            # ==========================================
            {
                "slug": "opentext-alm",
                "name": "OpenText / Micro Focus ALM (Quality Center)",
                "label": "OpenText ALM / Quality Center",
                "category": "server-app",
                "vendor": "OpenText / Micro Focus",
                "tags": ["opentext", "microfocus", "alm", "quality-center", "testing"],
                "source_name": "OpenText Product Support Lifecycle",
                "source_url": "https://www.opentext.com/services/support-services/product-lifecycle",
                "cycles": [
                    {"cycle": "24.1", "release_date": "2024-04-15", "eoas_date": "2027-04-15", "eol_date": "2029-04-15", "is_lts": True, "is_eol": False},
                    {"cycle": "16.0", "release_date": "2022-06-20", "eoas_date": "2025-06-30", "eol_date": "2027-06-30", "is_lts": True, "is_eol": False},
                    {"cycle": "15.5", "release_date": "2021-03-15", "eoas_date": "2024-03-31", "eol_date": "2026-03-31", "is_lts": True, "is_eol": False},
                    {"cycle": "15.0", "release_date": "2020-04-10", "eoas_date": "2023-04-30", "eol_date": "2025-04-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "opentext-content-suite",
                "name": "OpenText Content Suite / Server",
                "label": "OpenText Content Suite (Content Server)",
                "category": "server-app",
                "vendor": "OpenText / Micro Focus",
                "tags": ["opentext", "content-server", "ecm", "document-management"],
                "source_name": "OpenText Product Support Lifecycle",
                "source_url": "https://www.opentext.com/services/support-services/product-lifecycle",
                "cycles": [
                    {"cycle": "23.4", "release_date": "2023-11-15", "eoas_date": "2026-11-15", "eol_date": "2028-11-15", "is_lts": True, "is_eol": False},
                    {"cycle": "21.4", "release_date": "2021-11-01", "eoas_date": "2024-11-30", "eol_date": "2026-11-30", "is_lts": True, "is_eol": False},
                    {"cycle": "16.2", "release_date": "2017-04-01", "eoas_date": "2022-04-30", "eol_date": "2024-04-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "vertica",
                "name": "Micro Focus Vertica Analytics",
                "label": "OpenText / Micro Focus Vertica Analytics DB",
                "category": "database",
                "vendor": "OpenText / Micro Focus",
                "tags": ["opentext", "microfocus", "vertica", "analytics", "database"],
                "source_name": "OpenText Product Support Lifecycle",
                "source_url": "https://www.opentext.com/services/support-services/product-lifecycle",
                "cycles": [
                    {"cycle": "24.1", "release_date": "2024-03-01", "eoas_date": "2027-03-01", "eol_date": "2029-03-01", "is_lts": True, "is_eol": False},
                    {"cycle": "12.0", "release_date": "2022-08-15", "eoas_date": "2025-08-31", "eol_date": "2027-08-31", "is_lts": True, "is_eol": False},
                    {"cycle": "11.1", "release_date": "2021-12-10", "eoas_date": "2024-12-31", "eol_date": "2026-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "10.1", "release_date": "2020-11-20", "eoas_date": "2023-11-30", "eol_date": "2025-11-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "netiq-identity-manager",
                "name": "NetIQ Identity Manager",
                "label": "OpenText NetIQ Identity Manager",
                "category": "server-app",
                "vendor": "OpenText / Micro Focus",
                "tags": ["opentext", "netiq", "iam", "identity", "security"],
                "source_name": "OpenText Product Support Lifecycle",
                "source_url": "https://www.opentext.com/services/support-services/product-lifecycle",
                "cycles": [
                    {"cycle": "4.8", "release_date": "2020-03-31", "eoas_date": "2025-03-31", "eol_date": "2027-03-31", "is_lts": True, "is_eol": False},
                    {"cycle": "4.7", "release_date": "2018-07-31", "eoas_date": "2023-07-31", "eol_date": "2025-07-31", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "groupwise",
                "name": "GroupWise",
                "label": "OpenText GroupWise Mail & Collaboration",
                "category": "server-app",
                "vendor": "OpenText / Micro Focus",
                "tags": ["opentext", "groupwise", "email", "collaboration"],
                "source_name": "OpenText Product Support Lifecycle",
                "source_url": "https://www.opentext.com/services/support-services/product-lifecycle",
                "cycles": [
                    {"cycle": "18.4", "release_date": "2022-09-15", "eoas_date": "2025-09-30", "eol_date": "2027-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "18.3", "release_date": "2021-03-30", "eoas_date": "2024-03-31", "eol_date": "2026-03-31", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # IBM ENTERPRISE SOFTWARE
            # ==========================================
            {
                "slug": "websphere-app-server",
                "name": "IBM WebSphere Application Server",
                "label": "IBM WebSphere Application Server (WAS)",
                "category": "server-app",
                "vendor": "IBM Corporation",
                "tags": ["ibm", "websphere", "java-ee", "middleware", "application-server"],
                "source_name": "IBM Software Lifecycle Portal",
                "source_url": "https://www.ibm.com/support/pages/ibm-software-support-lifecycle-policies",
                "cycles": [
                    {"cycle": "9.0.5", "release_date": "2019-06-28", "eoas_date": "2030-12-31", "eol_date": "2033-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "8.5.5", "release_date": "2012-06-15", "eoas_date": "2030-12-31", "eol_date": "2033-12-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "ibm-db2",
                "name": "IBM DB2 Database",
                "label": "IBM Db2 Database",
                "category": "database",
                "vendor": "IBM Corporation",
                "tags": ["ibm", "db2", "database", "relational"],
                "source_name": "IBM Software Lifecycle Portal",
                "source_url": "https://www.ibm.com/support/pages/ibm-software-support-lifecycle-policies",
                "cycles": [
                    {"cycle": "11.5", "release_date": "2019-06-25", "eoas_date": "2026-09-30", "eol_date": "2029-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "11.1", "release_date": "2016-06-15", "eoas_date": "2022-04-30", "eol_date": "2025-04-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "ibm-mq",
                "name": "IBM MQ",
                "label": "IBM MQ Enterprise Messaging",
                "category": "server-app",
                "vendor": "IBM Corporation",
                "tags": ["ibm", "mq", "messaging", "middleware"],
                "source_name": "IBM Software Lifecycle Portal",
                "source_url": "https://www.ibm.com/support/pages/ibm-software-support-lifecycle-policies",
                "cycles": [
                    {"cycle": "9.3", "release_date": "2022-06-23", "eoas_date": "2027-09-30", "eol_date": "2030-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "9.2", "release_date": "2020-07-23", "eoas_date": "2025-09-30", "eol_date": "2028-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "9.1", "release_date": "2018-07-23", "eoas_date": "2023-09-30", "eol_date": "2026-09-30", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # SAP ENTERPRISE APPLICATIONS
            # ==========================================
            {
                "slug": "sap-s4hana",
                "name": "SAP S/4HANA",
                "label": "SAP S/4HANA ERP Platform",
                "category": "server-app",
                "vendor": "SAP SE",
                "tags": ["sap", "s4hana", "erp", "enterprise"],
                "source_name": "SAP Product Lifecycle Portal",
                "source_url": "https://support.sap.com/en/release-notes.html",
                "cycles": [
                    {"cycle": "2023", "release_date": "2023-10-11", "eoas_date": "2030-12-31", "eol_date": "2035-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "2022", "release_date": "2022-10-12", "eoas_date": "2027-12-31", "eol_date": "2030-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "2021", "release_date": "2021-10-13", "eoas_date": "2026-12-31", "eol_date": "2029-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "2020", "release_date": "2020-10-07", "eoas_date": "2025-12-31", "eol_date": "2028-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "1909", "release_date": "2019-09-20", "eoas_date": "2024-12-31", "eol_date": "2027-12-31", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # CISCO NETWORKING
            # ==========================================
            {
                "slug": "cisco-ios-xe",
                "name": "Cisco IOS-XE",
                "label": "Cisco IOS-XE Network OS",
                "category": "os",
                "vendor": "Cisco Systems",
                "tags": ["cisco", "ios-xe", "networking", "router", "switch"],
                "source_name": "Cisco End-of-Life Policy",
                "source_url": "https://www.cisco.com/c/en/us/products/eos-eol-policy.html",
                "cycles": [
                    {"cycle": "17.9", "release_date": "2022-07-31", "eoas_date": "2025-07-31", "eol_date": "2027-07-31", "is_lts": True, "is_eol": False},
                    {"cycle": "17.6", "release_date": "2021-07-31", "eoas_date": "2024-07-31", "eol_date": "2026-07-31", "is_lts": True, "is_eol": False},
                    {"cycle": "17.3", "release_date": "2020-08-15", "eoas_date": "2023-08-15", "eol_date": "2025-08-15", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # SERVICENOW & SPLUNK
            # ==========================================
            {
                "slug": "servicenow",
                "name": "ServiceNow Platform",
                "label": "ServiceNow Now Platform",
                "category": "server-app",
                "vendor": "ServiceNow, Inc.",
                "tags": ["servicenow", "itsm", "cloud", "platform"],
                "source_name": "ServiceNow Release Policy",
                "source_url": "https://docs.servicenow.com/bundle/family-release-notes.html",
                "cycles": [
                    {"cycle": "Washington DC", "release_date": "2024-03-20", "eoas_date": "2025-09-30", "eol_date": "2025-09-30", "is_lts": False, "is_eol": False},
                    {"cycle": "Vancouver", "release_date": "2023-09-20", "eoas_date": "2025-03-31", "eol_date": "2025-03-31", "is_lts": False, "is_eol": False},
                    {"cycle": "Utah", "release_date": "2023-03-22", "eoas_date": "2024-09-30", "eol_date": "2024-09-30", "is_lts": False, "is_eol": True},
                    {"cycle": "Tokyo", "release_date": "2022-09-21", "eoas_date": "2024-03-31", "eol_date": "2024-03-31", "is_lts": False, "is_eol": True}
                ]
            },
            {
                "slug": "splunk",
                "name": "Splunk Enterprise",
                "label": "Splunk Enterprise Platform",
                "category": "server-app",
                "vendor": "Splunk / Cisco",
                "tags": ["splunk", "siem", "logs", "analytics", "security"],
                "source_name": "Splunk Product Support Policy",
                "source_url": "https://www.splunk.com/en_us/legal/splunk-software-support-policy.html",
                "cycles": [
                    {"cycle": "9.3", "release_date": "2024-06-11", "eoas_date": "2026-06-11", "eol_date": "2027-06-11", "is_lts": True, "is_eol": False},
                    {"cycle": "9.2", "release_date": "2024-02-14", "eoas_date": "2026-02-14", "eol_date": "2027-02-14", "is_lts": True, "is_eol": False},
                    {"cycle": "9.1", "release_date": "2023-06-06", "eoas_date": "2025-06-06", "eol_date": "2026-06-06", "is_lts": True, "is_eol": False},
                    {"cycle": "9.0", "release_date": "2022-06-14", "eoas_date": "2024-06-14", "eol_date": "2025-06-14", "is_lts": True, "is_eol": False},
                    {"cycle": "8.2", "release_date": "2021-05-18", "eoas_date": "2023-05-18", "eol_date": "2024-05-18", "is_lts": True, "is_eol": True}
                ]
            }
        ]

    def ingest_all_enterprise_suites(self) -> int:
        """
        Ingests all enterprise vendor suites into database with provenance records.
        """
        catalog = self.get_enterprise_vendor_catalog()
        ingested_count = 0

        for item in catalog:
            pid = self.db.upsert_product(
                slug=item["slug"],
                name=item["name"],
                label=item["label"],
                category=item["category"],
                vendor=item["vendor"],
                tags=item["tags"]
            )

            ds = self.db.get_data_source_by_name(item["source_name"])
            ds_id = ds["id"] if ds else None
            conf = ds["confidence_score"] if ds else 0.95

            self.db.add_provenance(
                entity_type="product",
                entity_id=pid,
                data_source_id=ds_id,
                source_name=item["source_name"],
                source_url=item["source_url"],
                license="Official Vendor Documentation",
                confidence_score=conf,
                notes=f"Enterprise suite ingestion for {item['label']}"
            )

            for c in item["cycles"]:
                cid = self.db.upsert_release_cycle(
                    product_id=pid,
                    cycle=c["cycle"],
                    release_date=c.get("release_date"),
                    eoas_date=c.get("eoas_date"),
                    eol_date=c.get("eol_date"),
                    is_lts=c.get("is_lts", False),
                    is_eol=c.get("is_eol", False),
                    is_maintained=not c.get("is_eol", False)
                )

                self.db.add_provenance(
                    entity_type="release_cycle",
                    entity_id=cid,
                    data_source_id=ds_id,
                    source_name=item["source_name"],
                    source_url=item["source_url"],
                    license="Official Vendor Documentation",
                    confidence_score=conf,
                    notes=f"Release cycle {c['cycle']} for {item['label']}"
                )

            ingested_count += 1

        return ingested_count
