import logging

from db.database import Database
from endoflife import EndoflifeClient

logger = logging.getLogger(__name__)

class SyncService:
    def __init__(self, db: Database | None = None, client: EndoflifeClient | None = None):
        self.db = db or Database()
        self.client = client or EndoflifeClient()

    def sync_product(self, product_slug: str) -> bool:
        """
        Sync a single product and its release cycles from endoflife.date API into the DB.
        Attaches provenance records for the product and each release cycle.
        """
        try:
            details = self.client.get_product(product_slug)

            # Upsert product record
            product_id = self.db.upsert_product(
                slug=details.name,
                name=details.label,
                label=details.label,
                category=details.category,
                tags=details.tags,
                version_command=details.version_command
            )

            # Record provenance for Product
            source_url = f"https://endoflife.date/api/v1/products/{details.name}"
            self.db.add_provenance(
                entity_type="product",
                entity_id=product_id,
                source_name="endoflife.date API v1",
                source_url=source_url,
                license="CC0 1.0 Universal",
                confidence_score=1.0,
                notes=f"Fetched product summary for {details.label}"
            )

            # Upsert each Release Cycle
            for rel in details.releases:
                latest_ver = rel.latest.name if rel.latest else None
                latest_date = rel.latest.date if rel.latest else None

                cycle_id = self.db.upsert_release_cycle(
                    product_id=product_id,
                    cycle=rel.name,
                    label=rel.label,
                    codename=rel.codename,
                    release_date=rel.release_date,
                    eoas_date=rel.eoas_from,
                    eol_date=rel.eol_from,
                    eoes_date=rel.eoes_from,
                    is_lts=rel.is_lts,
                    is_eol=rel.is_eol,
                    is_maintained=rel.is_maintained,
                    latest_version=latest_ver,
                    latest_release_date=latest_date,
                    custom_metadata=rel.custom
                )

                # Record provenance for Release Cycle
                release_url = f"https://endoflife.date/api/v1/products/{details.name}/releases/{rel.name}"
                self.db.add_provenance(
                    entity_type="release_cycle",
                    entity_id=cycle_id,
                    source_name="endoflife.date API v1",
                    source_url=release_url,
                    license="CC0 1.0 Universal",
                    confidence_score=1.0,
                    notes=f"Release cycle {rel.name} data for {details.label}"
                )

            return True

        except Exception as e:  # noqa: BLE001
            logger.error(f"Error syncing product {product_slug}: {e}")
            return False

    def sync_popular_products(self, limit: int = 50) -> int:
        """
        Sync a batch of products from endoflife.date API.
        """
        products = self.client.get_products()
        synced_count = 0
        for p in products[:limit]:
            if self.sync_product(p.name):
                synced_count += 1
        return synced_count

    def sync_all_products(self) -> int:
        """
        Sync all available products from endoflife.date API.
        """
        products = self.client.get_products()
        synced_count = 0
        for p in products:
            if self.sync_product(p.name):
                synced_count += 1
        return synced_count

    def sync_all_products_bulk(self) -> tuple[int, int]:
        """
        Fast batch sync for all 473+ products and 8,600+ release cycles from endoflife.date API / GitHub release data.
        Returns (products_synced, cycles_synced).
        """
        logger.info("Starting bulk sync of all products from endoflife.date API...")
        full_products = self.client.get_products_full()

        prod_count = 0
        cycle_count = 0

        for details in full_products:
            try:
                # Upsert product record
                product_id = self.db.upsert_product(
                    slug=details.name,
                    name=details.label,
                    label=details.label,
                    category=details.category,
                    tags=details.tags,
                    version_command=details.version_command,
                )

                # Record provenance for Product
                source_url = f"https://endoflife.date/api/v1/products/{details.name}"
                self.db.add_provenance(
                    entity_type="product",
                    entity_id=product_id,
                    source_name="endoflife.date API v1 (Bulk GitHub Data)",
                    source_url=source_url,
                    license="CC0 1.0 Universal",
                    confidence_score=1.0,
                    notes=f"Full bulk sync for {details.label}",
                )
                prod_count += 1

                # Upsert each Release Cycle
                for rel in details.releases:
                    latest_ver = rel.latest.name if rel.latest else None
                    latest_date = rel.latest.date if rel.latest else None

                    cycle_id = self.db.upsert_release_cycle(
                        product_id=product_id,
                        cycle=rel.name,
                        label=rel.label,
                        codename=rel.codename,
                        release_date=rel.release_date,
                        eoas_date=rel.eoas_from,
                        eol_date=rel.eol_from,
                        eoes_date=rel.eoes_from,
                        is_lts=rel.is_lts,
                        is_eol=rel.is_eol,
                        is_maintained=rel.is_maintained,
                        latest_version=latest_ver,
                        latest_release_date=latest_date,
                        custom_metadata=rel.custom,
                    )

                    # Record provenance for Release Cycle
                    release_url = f"https://endoflife.date/api/v1/products/{details.name}/releases/{rel.name}"
                    self.db.add_provenance(
                        entity_type="release_cycle",
                        entity_id=cycle_id,
                        source_name="endoflife.date API v1 (Bulk GitHub Data)",
                        source_url=release_url,
                        license="CC0 1.0 Universal",
                        confidence_score=1.0,
                        notes=f"Release cycle {rel.name} data for {details.label}",
                    )
                    cycle_count += 1
            except Exception as e:  # noqa: BLE001
                logger.error(
                    f"Error syncing product {details.name} in bulk sync: {e}"
                )

        logger.info(
            f"Bulk sync completed: {prod_count} products and {cycle_count} release cycles ingested."
        )
        return prod_count, cycle_count
