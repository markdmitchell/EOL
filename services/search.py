from typing import Any

from db.database import Database


class SearchService:
    def __init__(self, db: Database | None = None):
        self.db = db or Database()

    def search_catalog(
        self,
        query: str = "",
        category: str = "",
        vendor: str = "",
        tag: str = "",
        eol_only: bool = False,
        lts_only: bool = False,
        limit: int | None = None,
        offset: int = 0
    ) -> list[dict[str, Any]]:
        """
        Search products and retrieve their release cycles, multi-source provenance, and collision flags.
        """
        products = self.db.search_products(
            query=query,
            category=category,
            vendor=vendor,
            tag=tag,
            limit=limit,
            offset=offset
        )
        results = []

        for p in products:
            cycles = self.db.get_release_cycles_for_product(p["id"])

            filtered_cycles = []
            for c in cycles:
                if eol_only and not c["is_eol"]:
                    continue
                if lts_only and not c["is_lts"]:
                    continue

                # Fetch all provenance records for this cycle to check for date collisions
                cycle_prov = self.db.get_provenance("release_cycle", c["id"])
                c["provenance_claims"] = cycle_prov
                c["has_collision"] = self._detect_date_collisions(cycle_prov)
                filtered_cycles.append(c)

            if eol_only and not filtered_cycles:
                continue

            p_prov = self.db.get_provenance("product", p["id"])

            results.append({
                "product": p,
                "release_cycles": filtered_cycles,
                "provenance": p_prov
            })

        return results

    def get_distinct_vendors(self) -> list[str]:
        return self.db.get_distinct_vendors()

    def get_distinct_categories(self) -> list[str]:
        return self.db.get_distinct_categories()

    def _detect_date_collisions(self, prov_records: list[dict[str, Any]]) -> bool:
        """
        Detects if multiple provenance records for the same entity report conflicting EOL dates.
        """
        if len(prov_records) < 2:
            return False

        # Collect distinct source notes / dates if present
        dates = set()
        for r in prov_records:
            notes = r.get("notes", "")
            if "EOL:" in notes or "eol_date" in notes:
                dates.add(notes)

        return len(dates) > 1

    def get_product_details_with_provenance(self, slug: str) -> dict[str, Any] | None:
        product = self.db.get_product_by_slug(slug)
        if not product:
            return None
        cycles = self.db.get_release_cycles_for_product(product["id"])
        product_prov = self.db.get_provenance("product", product["id"])

        cycles_with_prov = []
        for c in cycles:
            c_prov = self.db.get_provenance("release_cycle", c["id"])
            cycles_with_prov.append({
                "cycle": c,
                "provenance": c_prov,
                "has_collision": self._detect_date_collisions(c_prov)
            })

        return {
            "product": product,
            "release_cycles": cycles_with_prov,
            "provenance": product_prov
        }

    def get_inventory_risk_summary(self) -> dict[str, Any]:
        items = self.db.get_all_inventory_items()
        critical_count = sum(1 for i in items if i["risk_level"] == "CRITICAL (EOL)")
        high_count = sum(1 for i in items if i["risk_level"] == "HIGH")
        low_count = sum(1 for i in items if i["risk_level"] == "LOW")

        return {
            "total_items": len(items),
            "critical_eol_count": critical_count,
            "high_risk_count": high_count,
            "low_risk_count": low_count,
            "items": items
        }
