import csv
import io
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from db.database import Database

class CSVImporter:
    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def import_inventory_csv(self, file_path_or_buffer, source_name: str = "Enterprise Runtime Inventory CSV") -> int:
        """
        Imports runtime environment inventory records from a CSV path or file buffer.
        """
        if isinstance(file_path_or_buffer, str):
            with open(file_path_or_buffer, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        else:
            # File-like object (buffer)
            content = file_path_or_buffer.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(content))
            rows = list(reader)

        imported_count = 0
        today = date.today()

        for row in rows:
            platform = row.get("Runtime / Platform") or row.get("Platform") or row.get("Software") or ""
            version = row.get("Version") or ""
            if not platform or not version:
                continue

            release_type = row.get("Release Type", "Standard")
            deployment_env = row.get("Deployment Environment") or row.get("Environment") or "Production"
            release_date = row.get("Release Date")
            eoas_date = row.get("End of Active Support")
            eol_date = row.get("End of Life (EOL) Date") or row.get("EOL Date")
            target_upgrade = row.get("Target Upgrade Path", "N/A")
            migration_status = row.get("Migration Action Status", "No Action Needed")

            # Calculate days_to_eol and risk level dynamically if eol_date is present
            days_to_eol = None
            lifecycle_phase = row.get("Lifecycle Phase", "Unknown")
            risk_level = row.get("Risk Level", "LOW")

            if eol_date:
                try:
                    eol_dt = datetime.strptime(eol_date.strip(), "%Y-%m-%d").date()
                    delta = (eol_dt - today).days
                    days_to_eol = delta

                    if delta <= 0:
                        risk_level = "CRITICAL (EOL)"
                        lifecycle_phase = "End of Life"
                    elif delta <= 180:
                        risk_level = "HIGH"
                        lifecycle_phase = "Security Support"
                    else:
                        risk_level = "LOW"
                        lifecycle_phase = "Active Support"
                except ValueError:
                    pass

            item_id = self.db.upsert_inventory_item(
                platform=platform.strip(),
                version=version.strip(),
                release_type=release_type.strip(),
                deployment_env=deployment_env.strip(),
                release_date=release_date.strip() if release_date else None,
                eoas_date=eoas_date.strip() if eoas_date else None,
                eol_date=eol_date.strip() if eol_date else None,
                lifecycle_phase=lifecycle_phase,
                days_to_eol=days_to_eol if days_to_eol is not None else 0,
                risk_level=risk_level,
                target_upgrade_path=target_upgrade.strip(),
                migration_status=migration_status.strip()
            )

            # Record Provenance
            self.db.add_provenance(
                entity_type="inventory",
                entity_id=item_id,
                source_name=source_name,
                source_url=file_path_or_buffer if isinstance(file_path_or_buffer, str) else "Uploaded CSV Buffer",
                license="Internal Enterprise Audit",
                confidence_score=0.95,
                notes=f"Inventory record for {platform} {version} in {deployment_env}"
            )

            imported_count += 1

        return imported_count
