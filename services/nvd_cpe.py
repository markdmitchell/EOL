import csv
import json
import logging
import re
import time
from typing import Any

import requests

from db.database import Database

logger = logging.getLogger(__name__)

BASE_URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0"

# Set your API key if available (increases rate limit from 5 to 50 req/30s)
# Request a free key at: https://nvd.nist.gov/developers/request-an-api-key
API_KEY: str | None = None

def parse_cpe_23(cpe_uri: str) -> dict[str, str] | None:
    """Parses a CPE 2.3 URI string into standardized components.

    Format: cpe:2.3:part:vendor:product:version:update:edition:language:...
    """
    # Split on unescaped colons
    tokens = re.split(r"(?<!\\):", cpe_uri)
    if len(tokens) < 6 or tokens[0] != "cpe" or tokens[1] != "2.3":
        return None

    part_map = {"a": "Application", "o": "Operating System", "h": "Hardware"}

    part_code = tokens[2]
    # Filter out hardware entries
    if part_code not in ("a", "o"):
        return None

    return {
        "type": part_map.get(part_code, "Unknown"),
        "vendor": tokens[3].replace(r"\:", ":").replace("_", " ").title(),
        "product": tokens[4].replace(r"\:", ":").replace("_", " ").title(),
        "version": tokens[5].replace(r"\:", ":") if tokens[5] != "*" else "Any",
        "update": tokens[6].replace(r"\:", ":") if tokens[6] != "*" else "",
        "raw_cpe": cpe_uri,
    }

def extract_english_title(titles: list[dict[str, str]]) -> str:
    """Extracts the English human-readable title from CPE metadata."""
    for item in titles:
        if item.get("lang") == "en":
            return item.get("title", "")
    return titles[0].get("title", "") if titles else ""

def fetch_cpe_catalog(
    target_count: int = 500,
    deduplicate_products: bool = True,
    output_prefix: str = "enterprise_software_catalog",
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    """Paginates the NVD API, extracts software/OS records, and saves to disk."""
    effective_api_key = api_key or API_KEY
    headers = {"User-Agent": "CPE-Catalog-Extractor/1.0"}
    if effective_api_key:
        headers["apiKey"] = effective_api_key

    # NIST allows up to 2,000 records per request
    page_size = min(target_count, 2000)
    start_index = 0
    records: list[dict[str, Any]] = []
    seen_products = set()

    # Rate pacing: 0.6s with key, 1.0s without key
    sleep_interval = 0.6 if effective_api_key else 1.0

    logger.info(f"Starting NVD CPE extraction. Target: {target_count} software/OS records...")

    while len(records) < target_count:
        params = {"resultsPerPage": page_size, "startIndex": start_index}

        try:
            response = requests.get(
                BASE_URL, headers=headers, params=params, timeout=30
            )

            if response.status_code == 429:
                logger.warning("Rate limit reached. Backing off for 15 seconds...")
                time.sleep(15)
                continue

            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"Network error at index {start_index}: {e}")
            break

        products = data.get("products", [])
        if not products:
            logger.info("No further records available from endpoint.")
            break

        for item in products:
            cpe_data = item.get("cpe", {})
            if cpe_data.get("deprecated", False):
                continue

            cpe_uri = cpe_data.get("cpeName", "")
            parsed = parse_cpe_23(cpe_uri)
            if not parsed:
                continue

            # Deduplication logic: collapse identical vendor+product pairs
            if deduplicate_products:
                prod_key = (
                    parsed["type"],
                    parsed["vendor"].lower(),
                    parsed["product"].lower(),
                )
                if prod_key in seen_products:
                    continue
                seen_products.add(prod_key)

            parsed["title"] = extract_english_title(cpe_data.get("titles", []))
            parsed["cpe_id"] = cpe_data.get("cpeNameId", "")
            parsed["last_modified"] = cpe_data.get("lastModified", "")

            records.append(parsed)
            if len(records) >= target_count:
                break

        logger.info(
            f"Retrieved {len(records)}/{target_count} items (Scanned index: {start_index + len(products)})"
        )
        start_index += page_size
        time.sleep(sleep_interval)

    # Export to CSV
    csv_file = f"{output_prefix}.csv"
    fieldnames = [
        "title",
        "type",
        "vendor",
        "product",
        "version",
        "update",
        "raw_cpe",
        "cpe_id",
        "last_modified",
    ]
    try:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        # Export to JSON
        json_file = f"{output_prefix}.json"
        with open(json_file, mode="w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        logger.info(
            f"Export complete: {len(records)} entries saved to '{csv_file}' and '{json_file}'."
        )
    except Exception as e:  # noqa: BLE001
        logger.warning(f"File save warning: {e}")

    return records

def ingest_nvd_cpe_into_db(db: Database | None = None, records: list[dict[str, Any]] | None = None) -> int:
    """
    Ingests NVD CPE software records into the SQLite database with provenance links.
    """
    db = db or Database()
    if not records:
        records = fetch_cpe_catalog(target_count=300, deduplicate_products=True)

    ds = db.get_data_source_by_name("NIST National Vulnerability Database (NVD) CPE API")
    ds_id = ds["id"] if ds else None
    conf = ds["confidence_score"] if ds else 0.95

    count = 0
    for r in records:
        slug = f"{r['vendor'].lower().replace(' ', '-')}-{r['product'].lower().replace(' ', '-')}"
        category = "os" if r["type"] == "Operating System" else "server-app"
        
        pid = db.upsert_product(
            slug=slug,
            name=r["product"],
            label=r["title"] or f"{r['vendor']} {r['product']}",
            category=category,
            vendor=r["vendor"],
            tags=["nist", "cpe", r["type"].lower().replace(" ", "-")]
        )

        db.add_provenance(
            entity_type="product",
            entity_id=pid,
            data_source_id=ds_id,
            source_name="NIST NVD CPE 2.0 API",
            source_url=r["raw_cpe"],
            license="NIST Public Domain",
            confidence_score=conf,
            notes=f"CPE Name ID: {r['cpe_id']} | Raw CPE: {r['raw_cpe']}"
        )
        count += 1

    return count

if __name__ == "__main__":
    records = fetch_cpe_catalog(target_count=200, deduplicate_products=True)
    db = Database()
    count = ingest_nvd_cpe_into_db(db=db, records=records)
    print(f"Successfully ingested {count} NVD CPE records into database.")
