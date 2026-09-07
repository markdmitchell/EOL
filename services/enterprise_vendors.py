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
            # APPLE SUPPORT & MACOS
            # ==========================================
            {
                "slug": "macos",
                "name": "Apple macOS",
                "label": "Apple macOS Operating System",
                "category": "os",
                "vendor": "Apple Inc.",
                "tags": ["os", "apple", "macos", "desktop"],
                "source_name": "Apple Support (Vintage & Obsolete Products)",
                "source_url": "https://support.apple.com/en-us/102772",
                "cycles": [
                    {"cycle": "15", "release_date": "2024-09-16", "eoas_date": "2027-09-30", "eol_date": "2027-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "14", "release_date": "2023-09-26", "eoas_date": "2026-09-30", "eol_date": "2026-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "13", "release_date": "2022-10-24", "eoas_date": "2025-09-30", "eol_date": "2025-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "12", "release_date": "2021-10-25", "eoas_date": "2024-09-30", "eol_date": "2024-09-30", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # FORTINET FORTIOS
            # ==========================================
            {
                "slug": "fortios",
                "name": "Fortinet FortiOS",
                "label": "Fortinet FortiOS Security OS",
                "category": "os",
                "vendor": "Fortinet",
                "tags": ["fortinet", "fortios", "firewall", "security"],
                "source_name": "Fortinet Support Product Lifecycle",
                "source_url": "https://support.fortinet.com/Information/ProductLifeCycle.aspx",
                "cycles": [
                    {"cycle": "7.6", "release_date": "2024-04-10", "eoas_date": "2027-04-10", "eol_date": "2028-10-10", "is_lts": True, "is_eol": False},
                    {"cycle": "7.4", "release_date": "2023-05-11", "eoas_date": "2026-05-11", "eol_date": "2027-11-11", "is_lts": True, "is_eol": False},
                    {"cycle": "7.2", "release_date": "2022-03-31", "eoas_date": "2025-03-31", "eol_date": "2026-09-30", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2021-03-30", "eoas_date": "2024-03-30", "eol_date": "2025-09-30", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # .NET PLATFORM
            # ==========================================
            {
                "slug": "dotnet",
                "name": ".NET",
                "label": "Microsoft .NET Platform",
                "category": "framework",
                "vendor": "Microsoft Corporation",
                "tags": ["dotnet", "microsoft", "csharp", "runtime"],
                "source_name": ".NET Platform Support Policy",
                "source_url": "https://dotnet.microsoft.com/en-us/platform/support/policy",
                "cycles": [
                    {"cycle": "9.0", "release_date": "2024-11-12", "eoas_date": "2026-05-12", "eol_date": "2026-05-12", "is_lts": False, "is_eol": False},
                    {"cycle": "8.0", "release_date": "2023-11-14", "eoas_date": "2026-11-10", "eol_date": "2026-11-10", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2022-11-08", "eoas_date": "2024-05-14", "eol_date": "2024-05-14", "is_lts": False, "is_eol": True},
                    {"cycle": "6.0", "release_date": "2021-11-08", "eoas_date": "2024-11-12", "eol_date": "2024-11-12", "is_lts": True, "is_eol": True}
                ]
            },

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
                "source_name": "Cisco Product Lifecycle & EOL Policy",
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
            # ==========================================
            # VMWARE / BROADCOM VIRTUALIZATION
            # ==========================================
            {
                "slug": "vmware-esxi",
                "name": "VMware ESXi",
                "label": "VMware ESXi Hypervisor / vSphere",
                "category": "os",
                "vendor": "Broadcom / VMware",
                "tags": ["vmware", "esxi", "vsphere", "hypervisor", "virtualization"],
                "source_name": "VMware End of Life Matrix",
                "source_url": "https://www.vmwaremigrationhub.com/guides/vmware-end-of-life",
                "cycles": [
                    {"cycle": "8.0", "release_date": "2022-10-11", "eoas_date": "2027-10-11", "eol_date": "2029-10-11", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2020-04-02", "eoas_date": "2025-04-02", "eol_date": "2027-04-02", "is_lts": True, "is_eol": False},
                    {"cycle": "6.7", "release_date": "2018-04-17", "eoas_date": "2022-10-15", "eol_date": "2023-11-15", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "vmware-vcenter",
                "name": "VMware vCenter Server",
                "label": "VMware vCenter Server Platform",
                "category": "server-app",
                "vendor": "Broadcom / VMware",
                "tags": ["vmware", "vcenter", "vsphere", "management"],
                "source_name": "VMware End of Life Matrix",
                "source_url": "https://www.vmwaremigrationhub.com/guides/vmware-end-of-life",
                "cycles": [
                    {"cycle": "8.0", "release_date": "2022-10-11", "eoas_date": "2027-10-11", "eol_date": "2029-10-11", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2020-04-02", "eoas_date": "2025-04-02", "eol_date": "2027-04-02", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # CISCO NETWORKING & SECURITY
            # ==========================================
            {
                "slug": "cisco-ios",
                "name": "Cisco IOS Classic",
                "label": "Cisco IOS Network Operating System",
                "category": "os",
                "vendor": "Cisco Systems",
                "tags": ["cisco", "ios", "networking", "router", "switch"],
                "source_name": "Cisco Product Lifecycle & EOL Policy",
                "source_url": "https://www.cisco.com/c/en/us/products/eos-eol-policy.html",
                "cycles": [
                    {"cycle": "15.9", "release_date": "2019-03-29", "eoas_date": "2024-07-31", "eol_date": "2026-07-31", "is_lts": True, "is_eol": False},
                    {"cycle": "15.6", "release_date": "2015-12-18", "eoas_date": "2020-11-30", "eol_date": "2022-11-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "cisco-nx-os",
                "name": "Cisco NX-OS",
                "label": "Cisco NX-OS Data Center Switch OS",
                "category": "os",
                "vendor": "Cisco Systems",
                "tags": ["cisco", "nx-os", "nexus", "datacenter", "networking"],
                "source_name": "Cisco Product Lifecycle & EOL Policy",
                "source_url": "https://www.cisco.com/c/en/us/products/eos-eol-policy.html",
                "cycles": [
                    {"cycle": "10.3", "release_date": "2022-08-30", "eoas_date": "2025-08-30", "eol_date": "2027-08-30", "is_lts": True, "is_eol": False},
                    {"cycle": "9.3", "release_date": "2019-07-19", "eoas_date": "2023-07-31", "eol_date": "2025-07-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "cisco-asa",
                "name": "Cisco ASA Software",
                "label": "Cisco ASA Adaptive Security Appliance Software",
                "category": "os",
                "vendor": "Cisco Systems",
                "tags": ["cisco", "asa", "firewall", "security"],
                "source_name": "Cisco Product Lifecycle & EOL Policy",
                "source_url": "https://www.cisco.com/c/en/us/products/eos-eol-policy.html",
                "cycles": [
                    {"cycle": "9.18", "release_date": "2022-05-30", "eoas_date": "2025-05-30", "eol_date": "2027-05-30", "is_lts": True, "is_eol": False},
                    {"cycle": "9.16", "release_date": "2021-05-17", "eoas_date": "2024-05-31", "eol_date": "2026-05-31", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # RED HAT ENTERPRISE SUITE
            # ==========================================
            {
                "slug": "openshift",
                "name": "Red Hat OpenShift",
                "label": "Red Hat OpenShift Container Platform (OCP)",
                "category": "server-app",
                "vendor": "Red Hat, Inc.",
                "tags": ["redhat", "openshift", "kubernetes", "containers", "cloud"],
                "source_name": "Red Hat Customer Portal (access.redhat.com)",
                "source_url": "https://access.redhat.com/support/policy/updates/openshift",
                "cycles": [
                    {"cycle": "4.16", "release_date": "2024-06-25", "eoas_date": "2025-12-25", "eol_date": "2026-06-25", "is_lts": True, "is_eol": False},
                    {"cycle": "4.14", "release_date": "2023-10-31", "eoas_date": "2025-04-30", "eol_date": "2025-10-31", "is_lts": True, "is_eol": False},
                    {"cycle": "4.12", "release_date": "2023-01-17", "eoas_date": "2024-07-17", "eol_date": "2025-01-17", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "ansible-automation-platform",
                "name": "Red Hat Ansible Automation Platform",
                "label": "Red Hat Ansible Automation Platform (AAP)",
                "category": "server-app",
                "vendor": "Red Hat, Inc.",
                "tags": ["redhat", "ansible", "automation", "devops"],
                "source_name": "Red Hat Customer Portal (access.redhat.com)",
                "source_url": "https://access.redhat.com/support/policy/updates/ansible-automation-platform",
                "cycles": [
                    {"cycle": "2.4", "release_date": "2023-06-27", "eoas_date": "2025-06-27", "eol_date": "2026-06-27", "is_lts": True, "is_eol": False},
                    {"cycle": "2.3", "release_date": "2022-11-29", "eoas_date": "2024-11-29", "eol_date": "2025-11-29", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # MICROSOFT ENTERPRISE SUITE
            # ==========================================
            {
                "slug": "exchange-server",
                "name": "Microsoft Exchange Server",
                "label": "Microsoft Exchange Server",
                "category": "server-app",
                "vendor": "Microsoft Corporation",
                "tags": ["microsoft", "exchange", "email", "server"],
                "source_name": "Microsoft Support & Lifecycle Portal",
                "source_url": "https://support.microsoft.com/en-us/lifecycle/search",
                "cycles": [
                    {"cycle": "Subscription Edition", "release_date": "2025-07-01", "eoas_date": "2030-10-14", "eol_date": "2035-10-14", "is_lts": True, "is_eol": False},
                    {"cycle": "2019", "release_date": "2018-10-22", "eoas_date": "2025-10-14", "eol_date": "2025-10-14", "is_lts": True, "is_eol": False},
                    {"cycle": "2016", "release_date": "2015-10-01", "eoas_date": "2020-10-13", "eol_date": "2025-10-14", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "sharepoint-server",
                "name": "Microsoft SharePoint Server",
                "label": "Microsoft SharePoint Server",
                "category": "server-app",
                "vendor": "Microsoft Corporation",
                "tags": ["microsoft", "sharepoint", "intranet", "collaboration"],
                "source_name": "Microsoft Support & Lifecycle Portal",
                "source_url": "https://support.microsoft.com/en-us/lifecycle/search",
                "cycles": [
                    {"cycle": "Subscription Edition", "release_date": "2021-11-02", "eoas_date": "2026-07-14", "eol_date": "2031-07-14", "is_lts": True, "is_eol": False},
                    {"cycle": "2019", "release_date": "2018-10-22", "eoas_date": "2023-01-10", "eol_date": "2026-07-14", "is_lts": True, "is_eol": False},
                    {"cycle": "2016", "release_date": "2016-03-14", "eoas_date": "2021-07-13", "eol_date": "2026-07-14", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "windows-11-enterprise",
                "name": "Windows 11 Enterprise",
                "label": "Microsoft Windows 11 Enterprise Edition",
                "category": "os",
                "vendor": "Microsoft Corporation",
                "tags": ["microsoft", "windows", "windows11", "enterprise", "os"],
                "source_name": "Microsoft Support & Lifecycle Portal",
                "source_url": "https://learn.microsoft.com/en-us/lifecycle/products/windows-11-enterprise-and-education",
                "cycles": [
                    {"cycle": "24H2", "release_date": "2024-10-01", "eoas_date": "2027-10-12", "eol_date": "2027-10-12", "is_lts": True, "is_eol": False},
                    {"cycle": "23H2", "release_date": "2023-10-31", "eoas_date": "2026-11-10", "eol_date": "2026-11-10", "is_lts": True, "is_eol": False},
                    {"cycle": "22H2", "release_date": "2022-09-20", "eoas_date": "2025-10-14", "eol_date": "2025-10-14", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # HASHICORP INFRASTRUCTURE SUITE
            # ==========================================
            {
                "slug": "hashicorp-vault",
                "name": "HashiCorp Vault",
                "label": "HashiCorp Vault Security Platform",
                "category": "server-app",
                "vendor": "HashiCorp",
                "tags": ["hashicorp", "vault", "secrets", "security", "cloud"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://developer.hashicorp.com/vault/docs/upgrading/support-maintenance-policy",
                "cycles": [
                    {"cycle": "1.16", "release_date": "2024-03-19", "eoas_date": "2026-03-19", "eol_date": "2026-03-19", "is_lts": True, "is_eol": False},
                    {"cycle": "1.15", "release_date": "2023-10-03", "eoas_date": "2025-10-03", "eol_date": "2025-10-03", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # PALO ALTO, CHECK POINT & F5 NETWORK SECURITY
            # ==========================================
            {
                "slug": "palo-alto-pan-os",
                "name": "Palo Alto Networks PAN-OS",
                "label": "Palo Alto Networks PAN-OS Security OS",
                "category": "os",
                "vendor": "Palo Alto Networks",
                "tags": ["paloalto", "pan-os", "firewall", "security", "network"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://www.paloaltonetworks.com/services/support/end-of-life-summary/end-of-life-pan-os",
                "cycles": [
                    {"cycle": "11.1", "release_date": "2023-11-15", "eoas_date": "2026-11-15", "eol_date": "2027-11-15", "is_lts": True, "is_eol": False},
                    {"cycle": "10.2", "release_date": "2022-03-16", "eoas_date": "2025-03-16", "eol_date": "2026-03-16", "is_lts": True, "is_eol": False},
                    {"cycle": "10.1", "release_date": "2021-06-09", "eoas_date": "2024-06-09", "eol_date": "2024-12-09", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "check-point-gaia",
                "name": "Check Point Gaia OS",
                "label": "Check Point Gaia Security OS",
                "category": "os",
                "vendor": "Check Point Software",
                "tags": ["checkpoint", "gaia", "firewall", "security"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://www.checkpoint.com/support-services/support-life-cycle-policy/",
                "cycles": [
                    {"cycle": "R81.20", "release_date": "2022-11-14", "eoas_date": "2025-11-30", "eol_date": "2027-11-30", "is_lts": True, "is_eol": False},
                    {"cycle": "R81.10", "release_date": "2021-07-12", "eoas_date": "2024-07-31", "eol_date": "2025-07-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "f5-big-ip",
                "name": "F5 BIG-IP TMOS",
                "label": "F5 BIG-IP Local Traffic Manager (TMOS)",
                "category": "server-app",
                "vendor": "F5 Networks",
                "tags": ["f5", "big-ip", "load-balancer", "tmos", "security"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://my.f5.com/manage/s/article/K8947",
                "cycles": [
                    {"cycle": "17.1", "release_date": "2023-05-18", "eoas_date": "2026-05-18", "eol_date": "2028-05-18", "is_lts": True, "is_eol": False},
                    {"cycle": "16.1", "release_date": "2021-05-06", "eoas_date": "2024-05-06", "eol_date": "2026-05-06", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # ENTERPRISE DATA & ANALYTICS PLATFORMS
            # ==========================================
            {
                "slug": "databricks-runtime",
                "name": "Databricks Runtime",
                "label": "Databricks Runtime (DBR) Spark Platform",
                "category": "server-app",
                "vendor": "Databricks",
                "tags": ["databricks", "spark", "analytics", "data-lake", "ai"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://docs.databricks.com/en/release-notes/runtime/index.html",
                "cycles": [
                    {"cycle": "14.3 LTS", "release_date": "2024-02-15", "eoas_date": "2027-02-15", "eol_date": "2027-02-15", "is_lts": True, "is_eol": False},
                    {"cycle": "13.3 LTS", "release_date": "2023-07-20", "eoas_date": "2026-07-20", "eol_date": "2026-07-20", "is_lts": True, "is_eol": False},
                    {"cycle": "12.2 LTS", "release_date": "2023-02-16", "eoas_date": "2026-02-16", "eol_date": "2026-02-16", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "mongodb",
                "name": "MongoDB Enterprise",
                "label": "MongoDB Enterprise Database",
                "category": "database",
                "vendor": "MongoDB, Inc.",
                "tags": ["mongodb", "nosql", "database", "document"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://www.mongodb.com/support-policy/lifecycles",
                "cycles": [
                    {"cycle": "7.0", "release_date": "2023-08-15", "eoas_date": "2026-08-15", "eol_date": "2026-08-15", "is_lts": True, "is_eol": False},
                    {"cycle": "6.0", "release_date": "2022-07-19", "eoas_date": "2025-07-31", "eol_date": "2025-07-31", "is_lts": True, "is_eol": False},
                    {"cycle": "5.0", "release_date": "2021-07-13", "eoas_date": "2024-10-31", "eol_date": "2024-10-31", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "elasticsearch",
                "name": "Elasticsearch",
                "label": "Elasticsearch Enterprise Search Platform",
                "category": "database",
                "vendor": "Elastic N.V.",
                "tags": ["elastic", "elasticsearch", "search", "logs", "database"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://www.elastic.co/support/eol",
                "cycles": [
                    {"cycle": "8.12", "release_date": "2024-01-25", "eoas_date": "2026-07-25", "eol_date": "2026-07-25", "is_lts": True, "is_eol": False},
                    {"cycle": "7.17", "release_date": "2022-01-31", "eoas_date": "2025-01-31", "eol_date": "2025-01-31", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # NVIDIA & CITRIX ENTERPRISE INFRASTRUCTURE
            # ==========================================
            {
                "slug": "nvidia-ai-enterprise",
                "name": "NVIDIA AI Enterprise",
                "label": "NVIDIA AI Enterprise & CUDA Software Suite",
                "category": "framework",
                "vendor": "NVIDIA Corporation",
                "tags": ["nvidia", "cuda", "ai", "gpu", "machine-learning"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://docs.nvidia.com/ai-enterprise/latest/product-support-matrix/index.html",
                "cycles": [
                    {"cycle": "5.0", "release_date": "2024-03-15", "eoas_date": "2027-03-15", "eol_date": "2027-03-15", "is_lts": True, "is_eol": False},
                    {"cycle": "4.0", "release_date": "2023-08-15", "eoas_date": "2026-08-15", "eol_date": "2026-08-15", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "citrix-cvad",
                "name": "Citrix Virtual Apps and Desktops",
                "label": "Citrix Virtual Apps & Desktops (CVAD / XenApp)",
                "category": "server-app",
                "vendor": "Cloud Software Group / Citrix",
                "tags": ["citrix", "cvad", "xenapp", "vdi", "virtualization"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://support.citrix.com/article/CTX200466",
                "cycles": [
                    {"cycle": "2402 LTSR", "release_date": "2024-02-28", "eoas_date": "2029-02-28", "eol_date": "2034-02-28", "is_lts": True, "is_eol": False},
                    {"cycle": "2203 LTSR", "release_date": "2022-03-23", "eoas_date": "2027-03-23", "eol_date": "2032-03-23", "is_lts": True, "is_eol": False},
                    {"cycle": "1912 LTSR", "release_date": "2019-12-18", "eoas_date": "2024-12-18", "eol_date": "2029-12-18", "is_lts": True, "is_eol": False}
                ]
            },

            # ==========================================
            # SPRING & OPEN SOURCE DATABASES
            # ==========================================
            {
                "slug": "spring-boot",
                "name": "Spring Boot",
                "label": "Spring Boot Java Framework",
                "category": "framework",
                "vendor": "VMware / Broadcom",
                "tags": ["spring", "springboot", "java", "framework"],
                "source_name": "HeroDevs NES Documentation",
                "source_url": "https://spring.io/projects/spring-boot#support",
                "cycles": [
                    {"cycle": "3.2", "release_date": "2023-11-23", "eoas_date": "2024-11-23", "eol_date": "2025-11-23", "is_lts": True, "is_eol": False},
                    {"cycle": "3.1", "release_date": "2023-05-18", "eoas_date": "2024-05-18", "eol_date": "2024-11-18", "is_lts": False, "is_eol": True},
                    {"cycle": "2.7", "release_date": "2022-05-19", "eoas_date": "2023-11-24", "eol_date": "2025-08-24", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "postgresql",
                "name": "PostgreSQL Database",
                "label": "PostgreSQL Relational Database",
                "category": "database",
                "vendor": "PostgreSQL Global Development Group",
                "tags": ["postgresql", "postgres", "sql", "database"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://www.postgresql.org/support/versioning/",
                "cycles": [
                    {"cycle": "16", "release_date": "2023-09-14", "eoas_date": "2028-11-09", "eol_date": "2028-11-09", "is_lts": True, "is_eol": False},
                    {"cycle": "15", "release_date": "2022-10-13", "eoas_date": "2027-11-11", "eol_date": "2027-11-11", "is_lts": True, "is_eol": False},
                    {"cycle": "14", "release_date": "2021-09-30", "eoas_date": "2026-11-12", "eol_date": "2026-11-12", "is_lts": True, "is_eol": False},
                    {"cycle": "13", "release_date": "2020-09-24", "eoas_date": "2025-11-13", "eol_date": "2025-11-13", "is_lts": True, "is_eol": False},
                    {"cycle": "12", "release_date": "2019-10-03", "eoas_date": "2024-11-14", "eol_date": "2024-11-14", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "mysql",
                "name": "MySQL Server",
                "label": "Oracle MySQL Database Server",
                "category": "database",
                "vendor": "Oracle Corporation",
                "tags": ["mysql", "oracle", "sql", "database"],
                "source_name": "Oracle Lifetime Support Policy",
                "source_url": "https://www.oracle.com/support/lifetime-support/software.html",
                "cycles": [
                    {"cycle": "8.4 LTS", "release_date": "2024-04-30", "eoas_date": "2029-04-30", "eol_date": "2032-04-30", "is_lts": True, "is_eol": False},
                    {"cycle": "8.0", "release_date": "2018-04-19", "eoas_date": "2023-04-30", "eol_date": "2026-04-30", "is_lts": True, "is_eol": False},
                    {"cycle": "5.7", "release_date": "2013-10-23", "eoas_date": "2018-10-31", "eol_date": "2023-10-31", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # PUBLIC CLOUD & MANAGED KUBERNETES (AWS, AZURE, GCP)
            # ==========================================
            {
                "slug": "amazon-linux",
                "name": "Amazon Linux",
                "label": "Amazon Linux Operating System",
                "category": "os",
                "vendor": "Amazon Web Services",
                "tags": ["aws", "amazon", "linux", "cloud", "os"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://aws.amazon.com/amazon-linux-2023/faqs/",
                "cycles": [
                    {"cycle": "2023", "release_date": "2023-03-15", "eoas_date": "2028-03-15", "eol_date": "2028-03-15", "is_lts": True, "is_eol": False},
                    {"cycle": "2", "release_date": "2017-12-13", "eoas_date": "2024-06-30", "eol_date": "2025-06-30", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "aws-eks",
                "name": "AWS Elastic Kubernetes Service (EKS)",
                "label": "AWS EKS Kubernetes Runtime",
                "category": "server-app",
                "vendor": "Amazon Web Services",
                "tags": ["aws", "eks", "kubernetes", "cloud", "containers"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html",
                "cycles": [
                    {"cycle": "1.30", "release_date": "2024-05-23", "eoas_date": "2025-07-31", "eol_date": "2025-07-31", "is_lts": False, "is_eol": False},
                    {"cycle": "1.29", "release_date": "2024-01-23", "eoas_date": "2025-03-31", "eol_date": "2025-03-31", "is_lts": False, "is_eol": False},
                    {"cycle": "1.28", "release_date": "2023-09-26", "eoas_date": "2024-11-30", "eol_date": "2024-11-30", "is_lts": False, "is_eol": False}
                ]
            },
            {
                "slug": "azure-aks",
                "name": "Azure Kubernetes Service (AKS)",
                "label": "Microsoft Azure Kubernetes Service",
                "category": "server-app",
                "vendor": "Microsoft Corporation",
                "tags": ["azure", "aks", "kubernetes", "cloud", "microsoft"],
                "source_name": "Azure Updates",
                "source_url": "https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions",
                "cycles": [
                    {"cycle": "1.30", "release_date": "2024-05-30", "eoas_date": "2025-05-30", "eol_date": "2025-05-30", "is_lts": False, "is_eol": False},
                    {"cycle": "1.29", "release_date": "2024-03-01", "eoas_date": "2025-03-01", "eol_date": "2025-03-01", "is_lts": False, "is_eol": False},
                    {"cycle": "1.28", "release_date": "2023-11-01", "eoas_date": "2024-11-01", "eol_date": "2024-11-01", "is_lts": False, "is_eol": False}
                ]
            },
            {
                "slug": "gke",
                "name": "Google Kubernetes Engine (GKE)",
                "label": "Google Kubernetes Engine",
                "category": "server-app",
                "vendor": "Google",
                "tags": ["gcp", "gke", "google", "kubernetes", "cloud"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://cloud.google.com/kubernetes-engine/docs/release-schedule",
                "cycles": [
                    {"cycle": "1.30", "release_date": "2024-06-01", "eoas_date": "2025-07-01", "eol_date": "2025-07-01", "is_lts": False, "is_eol": False},
                    {"cycle": "1.29", "release_date": "2024-02-01", "eoas_date": "2025-03-01", "eol_date": "2025-03-01", "is_lts": False, "is_eol": False},
                    {"cycle": "1.28", "release_date": "2023-10-01", "eoas_date": "2024-11-01", "eol_date": "2024-11-01", "is_lts": False, "is_eol": False}
                ]
            },

            # ==========================================
            # ENTERPRISE LINUX DISTRIBUTIONS (SLES, DEBIAN, ALMALINUX, ROCKY, FREEBSD)
            # ==========================================
            {
                "slug": "sles",
                "name": "SUSE Linux Enterprise Server (SLES)",
                "label": "SUSE Linux Enterprise Server",
                "category": "os",
                "vendor": "SUSE Software Solutions",
                "tags": ["suse", "sles", "linux", "enterprise", "os"],
                "source_name": "Platform EOL Radar",
                "source_url": "https://www.suse.com/lifecycle/",
                "cycles": [
                    {"cycle": "15 SP5", "release_date": "2023-06-20", "eoas_date": "2028-07-31", "eol_date": "2031-07-31", "is_lts": True, "is_eol": False},
                    {"cycle": "15 SP4", "release_date": "2022-06-21", "eoas_date": "2023-12-31", "eol_date": "2026-12-31", "is_lts": True, "is_eol": False},
                    {"cycle": "12 SP5", "release_date": "2019-12-09", "eoas_date": "2024-10-31", "eol_date": "2027-10-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "debian",
                "name": "Debian GNU/Linux",
                "label": "Debian GNU/Linux Operating System",
                "category": "os",
                "vendor": "Debian Project",
                "tags": ["debian", "linux", "os", "open-source"],
                "source_name": "Platform EOL Radar",
                "source_url": "https://wiki.debian.org/LTS",
                "cycles": [
                    {"cycle": "12", "release_date": "2023-06-10", "eoas_date": "2026-06-10", "eol_date": "2028-06-30", "is_lts": True, "is_eol": False},
                    {"cycle": "11", "release_date": "2021-08-14", "eoas_date": "2024-07-31", "eol_date": "2026-06-30", "is_lts": True, "is_eol": False},
                    {"cycle": "10", "release_date": "2019-07-06", "eoas_date": "2022-07-18", "eol_date": "2024-06-30", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "almalinux",
                "name": "AlmaLinux",
                "label": "AlmaLinux OS (Enterprise Linux)",
                "category": "os",
                "vendor": "AlmaLinux OS Foundation",
                "tags": ["almalinux", "rhel", "linux", "enterprise", "os"],
                "source_name": "Platform EOL Radar",
                "source_url": "https://wiki.almalinux.org/release-notes/",
                "cycles": [
                    {"cycle": "9", "release_date": "2022-05-26", "eoas_date": "2027-05-31", "eol_date": "2032-05-31", "is_lts": True, "is_eol": False},
                    {"cycle": "8", "release_date": "2021-03-30", "eoas_date": "2024-05-31", "eol_date": "2029-05-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "rocky-linux",
                "name": "Rocky Linux",
                "label": "Rocky Linux (Enterprise Linux)",
                "category": "os",
                "vendor": "Rocky Enterprise Software Foundation",
                "tags": ["rocky", "rhel", "linux", "enterprise", "os"],
                "source_name": "Platform EOL Radar",
                "source_url": "https://docs.rockylinux.org/release_notes/",
                "cycles": [
                    {"cycle": "9", "release_date": "2022-07-14", "eoas_date": "2027-05-31", "eol_date": "2032-05-31", "is_lts": True, "is_eol": False},
                    {"cycle": "8", "release_date": "2021-04-30", "eoas_date": "2024-05-31", "eol_date": "2029-05-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "freebsd",
                "name": "FreeBSD",
                "label": "FreeBSD Operating System",
                "category": "os",
                "vendor": "FreeBSD Project",
                "tags": ["freebsd", "bsd", "unix", "os"],
                "source_name": "Platform EOL Radar",
                "source_url": "https://www.freebsd.org/security/#sup",
                "cycles": [
                    {"cycle": "14.0", "release_date": "2023-11-20", "eoas_date": "2028-11-30", "eol_date": "2028-11-30", "is_lts": True, "is_eol": False},
                    {"cycle": "13.2", "release_date": "2023-04-11", "eoas_date": "2024-06-30", "eol_date": "2024-06-30", "is_lts": False, "is_eol": True}
                ]
            },

            # ==========================================
            # ENTERPRISE FIREWALLS & MIDDLEWARE (SONICWALL, SOPHOS, WATCHGUARD, NGINX PLUS, TOMCAT)
            # ==========================================
            {
                "slug": "sonicwall-sonicos",
                "name": "SonicWall SonicOS",
                "label": "SonicWall SonicOS Firewall Firmware",
                "category": "os",
                "vendor": "SonicWall",
                "tags": ["sonicwall", "sonicos", "firewall", "security"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://www.sonicwall.com/support/product-lifecycle-information/",
                "cycles": [
                    {"cycle": "7.1", "release_date": "2023-11-15", "eoas_date": "2026-11-15", "eol_date": "2028-11-15", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2020-09-15", "eoas_date": "2024-09-15", "eol_date": "2025-09-15", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "sophos-sfos",
                "name": "Sophos Firewall (SFOS)",
                "label": "Sophos Firewall Operating System (SFOS)",
                "category": "os",
                "vendor": "Sophos",
                "tags": ["sophos", "sfos", "firewall", "security"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://support.sophos.com/support/s/article/KB-000035279",
                "cycles": [
                    {"cycle": "20.0", "release_date": "2023-11-14", "eoas_date": "2026-11-14", "eol_date": "2027-11-14", "is_lts": True, "is_eol": False},
                    {"cycle": "19.5", "release_date": "2022-11-16", "eoas_date": "2025-05-31", "eol_date": "2026-05-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "nginx-plus",
                "name": "NGINX Plus",
                "label": "F5 NGINX Plus Enterprise Web Server",
                "category": "server-app",
                "vendor": "F5 / NGINX",
                "tags": ["nginx", "f5", "webserver", "load-balancer"],
                "source_name": "Flexera Technopedia Catalog",
                "source_url": "https://docs.nginx.com/nginx/releases/",
                "cycles": [
                    {"cycle": "R31", "release_date": "2024-02-14", "eoas_date": "2025-02-14", "eol_date": "2025-02-14", "is_lts": True, "is_eol": False},
                    {"cycle": "R30", "release_date": "2023-08-23", "eoas_date": "2024-08-23", "eol_date": "2024-08-23", "is_lts": True, "is_eol": True}
                ]
            },
            {
                "slug": "apache-tomcat",
                "name": "Apache Tomcat",
                "label": "Apache Tomcat Application Server",
                "category": "server-app",
                "vendor": "Apache Software Foundation",
                "tags": ["apache", "tomcat", "java", "servlet", "webserver"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://tomcat.apache.org/whichversion.html",
                "cycles": [
                    {"cycle": "10.1", "release_date": "2022-09-26", "eoas_date": "2027-09-26", "eol_date": "2027-09-26", "is_lts": True, "is_eol": False},
                    {"cycle": "9.0", "release_date": "2018-01-18", "eoas_date": "2027-03-31", "eol_date": "2027-03-31", "is_lts": True, "is_eol": False},
                    {"cycle": "8.5", "release_date": "2016-03-24", "eoas_date": "2024-03-31", "eol_date": "2024-03-31", "is_lts": True, "is_eol": True}
                ]
            },

            # ==========================================
            # JAVA / OPENJDK & LANGUAGE RUNTIMES
            # ==========================================
            {
                "slug": "openjdk",
                "name": "Java / OpenJDK",
                "label": "OpenJDK / Java SE Platform",
                "category": "lang",
                "vendor": "Oracle / OpenJDK Community",
                "tags": ["java", "openjdk", "jdk", "runtime", "lang"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://www.oracle.com/java/technologies/java-se-support-roadmap.html",
                "cycles": [
                    {"cycle": "21", "release_date": "2023-09-19", "eoas_date": "2028-09-19", "eol_date": "2031-09-19", "is_lts": True, "is_eol": False},
                    {"cycle": "17", "release_date": "2021-09-14", "eoas_date": "2026-09-14", "eol_date": "2029-09-14", "is_lts": True, "is_eol": False},
                    {"cycle": "11", "release_date": "2018-09-25", "eoas_date": "2023-09-25", "eol_date": "2026-09-25", "is_lts": True, "is_eol": False},
                    {"cycle": "8", "release_date": "2014-03-18", "eoas_date": "2022-03-31", "eol_date": "2030-12-31", "is_lts": True, "is_eol": False}
                ]
            },
            {
                "slug": "golang",
                "name": "Go (Golang)",
                "label": "Go Programming Language Runtime",
                "category": "lang",
                "vendor": "Google",
                "tags": ["go", "golang", "google", "lang", "runtime"],
                "source_name": "Go Release Policy",
                "source_url": "https://go.dev/doc/devel/release",
                "cycles": [
                    {"cycle": "1.22", "release_date": "2024-02-06", "eoas_date": "2025-02-06", "eol_date": "2025-02-06", "is_lts": False, "is_eol": False},
                    {"cycle": "1.21", "release_date": "2023-08-08", "eoas_date": "2024-08-08", "eol_date": "2024-08-08", "is_lts": False, "is_eol": True}
                ]
            },
            {
                "slug": "rust",
                "name": "Rust",
                "label": "Rust Programming Language Compiler",
                "category": "lang",
                "vendor": "Rust Foundation",
                "tags": ["rust", "compiler", "lang", "systems"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://www.rust-lang.org/policies/security",
                "cycles": [
                    {"cycle": "1.78", "release_date": "2024-05-02", "eoas_date": "2024-06-13", "eol_date": "2024-06-13", "is_lts": False, "is_eol": False},
                    {"cycle": "1.77", "release_date": "2024-03-21", "eoas_date": "2024-05-02", "eol_date": "2024-05-02", "is_lts": False, "is_eol": True}
                ]
            },
            {
                "slug": "rails",
                "name": "Ruby on Rails",
                "label": "Ruby on Rails Web Framework",
                "category": "framework",
                "vendor": "Rails Core Team",
                "tags": ["rails", "ruby", "framework", "web"],
                "source_name": "Versio.io Software Lifecycle API",
                "source_url": "https://rubyonrails.org/maintenance",
                "cycles": [
                    {"cycle": "7.1", "release_date": "2023-10-05", "eoas_date": "2025-10-05", "eol_date": "2026-10-05", "is_lts": True, "is_eol": False},
                    {"cycle": "7.0", "release_date": "2021-12-15", "eoas_date": "2023-10-05", "eol_date": "2025-04-05", "is_lts": True, "is_eol": False},
                    {"cycle": "6.1", "release_date": "2020-12-09", "eoas_date": "2022-12-09", "eol_date": "2024-10-01", "is_lts": True, "is_eol": True}
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
