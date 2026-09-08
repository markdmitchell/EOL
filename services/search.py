from typing import Any

from db.database import SYNONYM_MAP, Database


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

        deduped = self._deduplicate_results(results)
        if query:
            deduped.sort(key=lambda x: self._calculate_relevance_score(x, query), reverse=True)
        return deduped

    def _calculate_relevance_score(self, item: dict[str, Any], query: str) -> tuple[int, int, int, str]:
        q = query.lower().strip()
        expanded_q = SYNONYM_MAP.get(q, q)
        q_clean = expanded_q.replace("-", " ").replace("_", " ").replace("/", " ")
        q_norm = expanded_q.replace("-", "").replace(" ", "").replace("_", "")

        product = item["product"]
        cycles_count = len(item["release_cycles"])
        name = (product.get("name") or "").lower()
        slug = (product.get("slug") or "").lower()
        label = (product.get("label") or "").lower()
        vendor = (product.get("vendor") or "").lower()
        tags = [t.lower() for t in (product.get("tags") or [])]

        score = 0
        # 1. Exact match on slug or name
        if slug == q or name == q or q_norm == slug.replace("-", "").replace("_", "") or q_norm == name.replace("-", "").replace("_", ""):
            score += 1000
        elif slug == expanded_q or name == expanded_q:
            score += 900
        elif slug.startswith((q, q_norm)) or name.startswith(q):
            score += 600
        elif q_clean in name.replace("-", " ") or q_clean in label.replace("-", " "):
            score += 400
        elif q in slug or q in name:
            score += 300
        elif q in label or q in vendor or any(q in t for t in tags):
            score += 150

        if cycles_count > 0:
            score += 200

        return (score, cycles_count, -len(slug), label)

    def _deduplicate_results(self, results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Deduplicates search results where a canonical product is accompanied by
        a secondary duplicate entry (e.g. bare CPE stubs with 0 cycles).
        """
        seen_keys: dict[str, dict[str, Any]] = {}
        deduped: list[dict[str, Any]] = []

        for item in results:
            product = item["product"]
            cycles = item["release_cycles"]
            slug = product["slug"].lower()

            parts = slug.split("-")
            base_slug = slug
            if len(parts) >= 2 and parts[0] == parts[1]:
                base_slug = parts[0]

            # Strip common variant suffixes for deduplication keying
            for suffix in ["-enterprise", "-server", "-community", "-edition", "-express"]:
                base_slug = base_slug.removesuffix(suffix)

            key = base_slug.replace("-", "").replace(" ", "").replace("_", "")

            if key not in seen_keys:
                seen_keys[key] = item
                deduped.append(item)
            else:
                existing_item = seen_keys[key]
                existing_cycles = len(existing_item["release_cycles"])
                current_cycles = len(cycles)

                if current_cycles > existing_cycles or (
                    current_cycles == existing_cycles and len(slug) < len(existing_item["product"]["slug"])
                ):
                    idx = deduped.index(existing_item)
                    deduped[idx] = item
                    seen_keys[key] = item

        return deduped

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
