"""
Database Seeding Script:
Registers all 24 software EOL data sources, ingests official vendor lifecycle catalogs,
syncs popular software products from endoflife.date API, and imports enterprise runtime inventory CSV.
"""

import os

from db.database import Database
from services.csv_importer import CSVImporter
from services.multi_source import MultiSourceService
from services.sync import SyncService


def seed():
    print("=== Initializing EOL/EOS Database ===")
    db = Database()

    print("=== Registering 24 Software EOL Data Sources ===")
    ms_svc = MultiSourceService(db=db)
    sources_count = ms_svc.register_all_sources()
    print(f"Registered {sources_count} software EOL data sources into database.")

    print("\n=== Ingesting Official Vendor Lifecycle Catalogs ===")
    vendor_count = ms_svc.ingest_vendor_lifecycle_catalog()
    print(f"Ingested {vendor_count} official vendor product lifecycles.")

    print("\n=== Ingesting Popular Products from endoflife.date API ===")
    sync_svc = SyncService(db=db)
    popular_list = ["python", "ubuntu", "nodejs", "php", "dotnet", "react", "postgresql", "mysql", "nginx", "windows-server", "alpine-linux", "rhel", "debian"]
    
    synced_count = 0
    for slug in popular_list:
        if sync_svc.sync_product(slug):
            synced_count += 1
    print(f"Synced {synced_count}/{len(popular_list)} primary API products successfully.")

    print("\n=== Importing Active Runtime Environment Inventory CSV ===")
    csv_path = os.path.join(os.path.dirname(__file__), "data", "active_inventory.csv")
    if os.path.exists(csv_path):
        importer = CSVImporter(db=db)
        count = importer.import_inventory_csv(csv_path)
        print(f"Imported {count} active runtime environment records.")

    print("\n=== Database Seeding Complete! ===")

if __name__ == "__main__":
    seed()
