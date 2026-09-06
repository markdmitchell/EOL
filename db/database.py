import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "eol_database.db")

class Database:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 0. Data Sources Registry table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    format TEXT,
                    url TEXT,
                    api_available TEXT,
                    confidence_score REAL DEFAULT 1.0,
                    description TEXT,
                    last_synced_at TEXT DEFAULT (datetime('now'))
                );
            """)

            # 1. Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    label TEXT NOT NULL,
                    category TEXT,
                    vendor TEXT,
                    tags TEXT,
                    version_command TEXT,
                    created_at TEXT DEFAULT (datetime('now')),
                    updated_at TEXT DEFAULT (datetime('now'))
                );
            """)

            # 2. Release Cycles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS release_cycles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    cycle TEXT NOT NULL,
                    label TEXT,
                    codename TEXT,
                    release_date TEXT,
                    eoas_date TEXT,
                    eol_date TEXT,
                    eoes_date TEXT,
                    is_lts INTEGER DEFAULT 0,
                    is_eol INTEGER DEFAULT 0,
                    is_maintained INTEGER DEFAULT 0,
                    latest_version TEXT,
                    latest_release_date TEXT,
                    custom_metadata TEXT,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE(product_id, cycle)
                );
            """)

            # 3. Provenance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS provenance_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT NOT NULL,
                    entity_id INTEGER NOT NULL,
                    data_source_id INTEGER,
                    source_name TEXT NOT NULL,
                    source_url TEXT,
                    license TEXT,
                    fetched_at TEXT DEFAULT (datetime('now')),
                    verified_at TEXT,
                    confidence_score REAL DEFAULT 1.0,
                    notes TEXT,
                    FOREIGN KEY (data_source_id) REFERENCES data_sources(id) ON DELETE SET NULL
                );
            """)

            # 4. Environment Inventories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS environment_inventories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    version TEXT NOT NULL,
                    release_type TEXT,
                    deployment_env TEXT NOT NULL,
                    release_date TEXT,
                    eoas_date TEXT,
                    eol_date TEXT,
                    lifecycle_phase TEXT,
                    days_to_eol INTEGER,
                    risk_level TEXT,
                    target_upgrade_path TEXT,
                    migration_status TEXT,
                    updated_at TEXT DEFAULT (datetime('now'))
                );
            """)

            # Create Indexes for fast searching
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_release_cycles_product ON release_cycles(product_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_provenance_entity ON provenance_records(entity_type, entity_id);")

            conn.commit()

    # --- Data Source Operations ---
    def upsert_data_source(
        self,
        name: str,
        category: str,
        format: str,
        url: str,
        api_available: str,
        confidence_score: float = 1.0,
        description: str = ""
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO data_sources (name, category, format, url, api_available, confidence_score, description, last_synced_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    category=excluded.category,
                    format=excluded.format,
                    url=excluded.url,
                    api_available=excluded.api_available,
                    confidence_score=excluded.confidence_score,
                    description=excluded.description,
                    last_synced_at=excluded.last_synced_at
                RETURNING id;
            """, (name, category, format, url, api_available, confidence_score, description, now))
            row = cursor.fetchone()
            return row["id"]

    def get_all_data_sources(self) -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM data_sources ORDER BY confidence_score DESC, name ASC;")
            return [dict(row) for row in cursor.fetchall()]

    def get_data_source_by_name(self, name: str) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM data_sources WHERE name = ?;", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    # --- Product Operations ---
    def upsert_product(
        self,
        slug: str,
        name: str,
        label: str,
        category: str | None = None,
        vendor: str | None = None,
        tags: list[str] | None = None,
        version_command: str | None = None
    ) -> int:
        tags_str = json.dumps(tags or [])
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (slug, name, label, category, vendor, tags, version_command, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(slug) DO UPDATE SET
                    name=excluded.name,
                    label=excluded.label,
                    category=excluded.category,
                    vendor=COALESCE(excluded.vendor, products.vendor),
                    tags=excluded.tags,
                    version_command=COALESCE(excluded.version_command, products.version_command),
                    updated_at=excluded.updated_at
                RETURNING id;
            """, (slug, name, label, category, vendor, tags_str, version_command, now))
            row = cursor.fetchone()
            return row["id"]

    def upsert_release_cycle(
        self,
        product_id: int,
        cycle: str,
        label: str | None = None,
        codename: str | None = None,
        release_date: str | None = None,
        eoas_date: str | None = None,
        eol_date: str | None = None,
        eoes_date: str | None = None,
        is_lts: bool = False,
        is_eol: bool = False,
        is_maintained: bool = False,
        latest_version: str | None = None,
        latest_release_date: str | None = None,
        custom_metadata: dict[str, Any] | None = None
    ) -> int:
        custom_str = json.dumps(custom_metadata) if custom_metadata else None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO release_cycles (
                    product_id, cycle, label, codename, release_date, eoas_date, eol_date, eoes_date,
                    is_lts, is_eol, is_maintained, latest_version, latest_release_date, custom_metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(product_id, cycle) DO UPDATE SET
                    label=excluded.label,
                    codename=excluded.codename,
                    release_date=excluded.release_date,
                    eoas_date=excluded.eoas_date,
                    eol_date=excluded.eol_date,
                    eoes_date=excluded.eoes_date,
                    is_lts=excluded.is_lts,
                    is_eol=excluded.is_eol,
                    is_maintained=excluded.is_maintained,
                    latest_version=excluded.latest_version,
                    latest_release_date=excluded.latest_release_date,
                    custom_metadata=excluded.custom_metadata
                RETURNING id;
            """, (
                product_id, str(cycle), label, codename, release_date, eoas_date, eol_date, eoes_date,
                1 if is_lts else 0, 1 if is_eol else 0, 1 if is_maintained else 0,
                latest_version, latest_release_date, custom_str
            ))
            row = cursor.fetchone()
            return row["id"]

    def add_provenance(
        self,
        entity_type: str,
        entity_id: int,
        source_name: str,
        source_url: str | None = None,
        license: str | None = None,
        confidence_score: float = 1.0,
        notes: str | None = None,
        data_source_id: int | None = None
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        if not data_source_id:
            ds = self.get_data_source_by_name(source_name)
            if ds:
                data_source_id = ds["id"]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO provenance_records (
                    entity_type, entity_id, data_source_id, source_name, source_url, license, fetched_at, verified_at, confidence_score, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (entity_type, entity_id, data_source_id, source_name, source_url, license, now, now, confidence_score, notes))
            return cursor.lastrowid

    def get_provenance(self, entity_type: str, entity_id: int) -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*, d.url as ds_url, d.confidence_score as ds_confidence
                FROM provenance_records p
                LEFT JOIN data_sources d ON p.data_source_id = d.id
                WHERE p.entity_type = ? AND p.entity_id = ?
                ORDER BY p.fetched_at DESC;
            """, (entity_type, entity_id))
            return [dict(row) for row in cursor.fetchall()]

    def search_products(self, query: str = "", category: str = "", tag: str = "") -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM products WHERE 1=1"
            params = []

            if query:
                sql += " AND (name LIKE ? OR label LIKE ? OR slug LIKE ? OR vendor LIKE ?)"
                q_like = f"%{query}%"
                params.extend([q_like, q_like, q_like, q_like])

            if category:
                sql += " AND category = ?"
                params.append(category)

            if tag:
                sql += " AND tags LIKE ?"
                params.append(f"%{tag}%")

            sql += " ORDER BY label ASC;"
            cursor.execute(sql, params)
            products = [dict(row) for row in cursor.fetchall()]
            for p in products:
                p["tags"] = json.loads(p["tags"]) if p["tags"] else []
            return products

    def get_product_by_slug(self, slug: str) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE slug = ?;", (slug,))
            row = cursor.fetchone()
            if not row:
                return None
            p = dict(row)
            p["tags"] = json.loads(p["tags"]) if p["tags"] else []
            return p

    def get_release_cycles_for_product(self, product_id: int) -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM release_cycles
                WHERE product_id = ?
                ORDER BY release_date DESC;
            """, (product_id,))
            rows = cursor.fetchall()
            cycles = []
            for r in rows:
                c = dict(r)
                c["custom_metadata"] = json.loads(c["custom_metadata"]) if c["custom_metadata"] else None
                cycles.append(c)
            return cycles

    # --- Inventory Operations ---
    def upsert_inventory_item(
        self,
        platform: str,
        version: str,
        release_type: str,
        deployment_env: str,
        release_date: str | None,
        eoas_date: str | None,
        eol_date: str | None,
        lifecycle_phase: str,
        days_to_eol: int,
        risk_level: str,
        target_upgrade_path: str,
        migration_status: str
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM environment_inventories
                WHERE platform = ? AND version = ? AND deployment_env = ?;
            """, (platform, version, deployment_env))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("""
                    UPDATE environment_inventories SET
                        release_type=?, release_date=?, eoas_date=?, eol_date=?,
                        lifecycle_phase=?, days_to_eol=?, risk_level=?,
                        target_upgrade_path=?, migration_status=?, updated_at=?
                    WHERE id=?;
                """, (
                    release_type, release_date, eoas_date, eol_date,
                    lifecycle_phase, days_to_eol, risk_level,
                    target_upgrade_path, migration_status, now, existing["id"]
                ))
                return existing["id"]
            else:
                cursor.execute("""
                    INSERT INTO environment_inventories (
                        platform, version, release_type, deployment_env, release_date, eoas_date, eol_date,
                        lifecycle_phase, days_to_eol, risk_level, target_upgrade_path, migration_status, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    platform, version, release_type, deployment_env, release_date, eoas_date, eol_date,
                    lifecycle_phase, days_to_eol, risk_level, target_upgrade_path, migration_status, now
                ))
                return cursor.lastrowid

    def get_all_inventory_items(self) -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM environment_inventories ORDER BY days_to_eol ASC;")
            return [dict(row) for row in cursor.fetchall()]
