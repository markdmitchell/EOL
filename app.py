
import pandas as pd
import streamlit as st

from db.database import Database
from services.csv_importer import CSVImporter
from services.enterprise_vendors import EnterpriseVendorService
from services.multi_source import MultiSourceService
from services.nvd_cpe import fetch_cpe_catalog, ingest_nvd_cpe_into_db
from services.search import SearchService
from services.sync import SyncService

# Page Configuration
st.set_page_config(
    page_title="endoflife.tech | Enterprise Software EOL/EOS Intelligence (v0.9.0-beta)",
    page_icon="🛡️",
    layout="wide"
)

# --- Bento Box UI Custom CSS Styling ---
st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Bento Grid Stat Tile */
    .bento-tile {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        text-align: center;
        margin-bottom: 12px;
    }
    .bento-tile-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }
    .bento-tile-lbl {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Bento Pill Badges */
    .pill-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.76rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .pill-blue {
        background-color: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }
    .pill-green {
        background-color: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
    }
    .pill-amber {
        background-color: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }
    .pill-slate {
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
    }

    /* Streamlit Expander Overrides for Bento Cards */
    div[data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.15s ease-in-out;
    }
    div[data-testid="stExpander"]:hover {
        border-color: #cbd5e1 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02) !important;
    }
    div[data-testid="stExpander"] > summary {
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_resource(ttl=3600)
def get_services(cache_version: str = "v3_tracked_db"):
    db = Database()
    search_svc = SearchService(db=db)
    sync_svc = SyncService(db=db)
    csv_imp = CSVImporter(db=db)
    ms_svc = MultiSourceService(db=db)
    ent_svc = EnterpriseVendorService(db=db)

    # Auto-seed database if empty on initial environment startup
    if len(db.search_products()) == 0:
        ent_svc.ingest_all_enterprise_suites()
        sync_svc.sync_all_products_bulk()

    return db, search_svc, sync_svc, csv_imp, ms_svc, ent_svc

db, search_svc, sync_svc, csv_imp, ms_svc, ent_svc = get_services()

def fetch_distinct_categories(db_inst, search_inst):
    if hasattr(search_inst, "get_distinct_categories"):
        return search_inst.get_distinct_categories()
    if hasattr(db_inst, "get_distinct_categories"):
        return db_inst.get_distinct_categories()
    with db_inst.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != '' ORDER BY category ASC;")
        return [row["category"] for row in cursor.fetchall()]

def fetch_distinct_vendors(db_inst, search_inst):
    if hasattr(search_inst, "get_distinct_vendors"):
        return search_inst.get_distinct_vendors()
    if hasattr(db_inst, "get_distinct_vendors"):
        return db_inst.get_distinct_vendors()
    with db_inst.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT vendor FROM products WHERE vendor IS NOT NULL AND vendor != '' ORDER BY vendor ASC;")
        return [row["vendor"] for row in cursor.fetchall()]

def execute_catalog_search(search_inst, query, category, vendor, eol_only):
    try:
        return search_inst.search_catalog(query=query, category=category, vendor=vendor, eol_only=eol_only)
    except TypeError:
        results = search_inst.search_catalog(query=query, category=category, eol_only=eol_only)
        if vendor:
            results = [r for r in results if r["product"].get("vendor") == vendor]
        return results

# --- Sidebar Header & Navigation ---
st.sidebar.image("https://img.icons8.com/color/96/shield.png", width=64)
st.sidebar.title("endoflife.tech")
st.sidebar.caption("Enterprise Software Lifecycle Reference Portal")
st.sidebar.markdown(
    """
    <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 10px 12px; margin-bottom: 14px; font-size: 0.82rem; color: #1e40af;">
        🌐 <strong>Live Site:</strong> <a href="https://endoflife.tech" target="_blank" style="color: #2563eb; font-weight: bold; text-decoration: underline;">endoflife.tech</a><br/>
        🏷️ <strong>Version:</strong> <code>v0.9.0-beta</code> <span style="background-color: #fef08a; color: #854d0e; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">EARLY BETA</span>
    </div>
    """,
    unsafe_allow_html=True
)

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🔍 Searchable Product Catalog",
        "🛡️ Runtime Environment Risk Dashboard",
        "📚 Integrated Data Sources Registry",
        "📜 Data Provenance & Audit Inspector",
        "⚙️ Data Ingestion & Management"
    ]
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 14px; margin-top: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div style="font-size: 0.85rem; font-weight: 700; color: #0f172a; margin-bottom: 10px;">
            👤 Authors & Contributors
        </div>
        <div style="font-size: 0.84rem; color: #334155;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span><strong>Mark D. Mitchell</strong></span>
                <a href="https://www.linkedin.com/in/markdmitchell/" target="_blank" title="Mark D. Mitchell on LinkedIn" style="display: inline-flex; align-items: center; text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="18" height="18" alt="LinkedIn"/>
                </a>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span><strong>James Shenberger</strong></span>
                <a href="https://www.linkedin.com/in/jamesshenberger/" target="_blank" title="James Shenberger on LinkedIn" style="display: inline-flex; align-items: center; text-decoration: none;">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="18" height="18" alt="LinkedIn"/>
                </a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# TAB 1: Searchable Product Catalog
# ==========================================
if nav_choice == "🔍 Searchable Product Catalog":
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("🔍 Searchable Enterprise Software EOL/EOS Catalog")
    with col_t2:
        st.markdown(
            """
            <div style="text-align: right; padding-top: 15px;">
                <span style="background-color: #fef08a; color: #854d0e; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: bold; border: 1px solid #fde047;">⚡ EARLY BETA v0.9.0-beta</span><br/>
                <span style="font-size: 0.8rem; color: #64748b;">Domain: <a href="https://endoflife.tech" target="_blank" style="color: #2563eb; font-weight: 600;">endoflife.tech</a></span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("Search support lifecycles, EOL/EOS dates, and release cycles across **3,000+ software products**, enterprise suites, utilities, OSs, languages, and databases.")

    # --- Bento Box Top Hero Stat Tiles ---
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown(
            """
            <div class="bento-tile">
                <div class="bento-tile-val">3,054</div>
                <div class="bento-tile-lbl">📦 Enterprise Products</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with b_col2:
        st.markdown(
            """
            <div class="bento-tile">
                <div class="bento-tile-val">8,841</div>
                <div class="bento-tile-lbl">📅 Release Cycles Tracked</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with b_col3:
        st.markdown(
            """
            <div class="bento-tile">
                <div class="bento-tile-val">30,300</div>
                <div class="bento-tile-lbl">🛡️ Verified Provenance Records</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    available_categories = ["All Categories"] + fetch_distinct_categories(db, search_svc)
    available_vendors = ["All Vendors"] + fetch_distinct_vendors(db, search_svc)

    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        query_input = st.text_input(
            "Search Product (e.g. 7-Zip, WinRAR, Jira, OpenText, Python, Cisco, Windows)",
            key="catalog_query_input"
        )
    with col2:
        category_filter = st.selectbox("Category Filter", available_categories)
    with col3:
        vendor_filter = st.selectbox("Vendor Filter", available_vendors)
    with col4:
        eol_only = st.checkbox("Only Show EOL Products/Cycles", value=False)

    has_search_term = bool(query_input.strip())
    has_category = category_filter != "All Categories"
    has_vendor = vendor_filter != "All Vendors"
    is_active_search = has_search_term or has_category or has_vendor or eol_only

    if not is_active_search:
        st.markdown(
            """
            <div style="display: inline-block; width: fit-content; background-color: #f0f7ff; color: #1e40af; border: 1px solid #bfdbfe; border-left: 4px solid #3b82f6; padding: 10px 16px; border-radius: 6px; margin: 8px 0 12px 0; font-size: 0.95rem;">
                💡 <strong>Type a software or OS product name above to search EOL/EOS dates.</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        cat_val = "" if category_filter == "All Categories" else category_filter
        ven_val = "" if vendor_filter == "All Vendors" else vendor_filter

        all_results = execute_catalog_search(
            search_inst=search_svc,
            query=query_input.strip(),
            category=cat_val,
            vendor=ven_val,
            eol_only=eol_only
        )

        total_results = len(all_results)

        # UI Pagination controls for ultra-fast rendering
        p_col1, p_col2 = st.columns([2, 2])
        with p_col1:
            page_size = st.selectbox("Products per page", [10, 25, 50, 100], index=1)
        with p_col2:
            total_pages = max(1, (total_results + page_size - 1) // page_size)

            # Reset page state if query or filters changed
            filter_state_key = f"{query_input}_{cat_val}_{ven_val}_{eol_only}_{page_size}"
            if st.session_state.get("active_filter_key") != filter_state_key:
                st.session_state["active_filter_key"] = filter_state_key
                st.session_state["page_num"] = 1

            selected_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=min(st.session_state.get("page_num", 1), total_pages),
                step=1
            )
            st.session_state["page_num"] = selected_page

        current_page = st.session_state.get("page_num", 1)
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_results)
        page_results = all_results[start_idx:end_idx]

        if total_results == 0:
            st.warning("No products found matching your search criteria.")
            st.info("💡 **Tips**: Try broadening your search query, selecting 'All Vendors' / 'All Categories', or sync missing products in the 'Data Ingestion & Management' tab.")
        else:
            st.success(f"Found **{total_results}** matching enterprise products. Showing items **{start_idx + 1} - {end_idx}** (Page {current_page} of {total_pages}):")

            for item in page_results:
                product = item["product"]
                cycles = item["release_cycles"]
                provenance = item["provenance"]

                ven_name = product.get('vendor') or 'N/A'
                cat_name = product.get('category') or 'N/A'
                card_title = f"📦 **{product['label']}** ({product['slug']}) — Vendor: `{ven_name}` | Category: `{cat_name}`"

                with st.expander(card_title, expanded=(total_results == 1)):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"**Vendor:** {ven_name}")
                        st.write(f"**Tags:** {', '.join(product['tags']) if product['tags'] else 'N/A'}")
                        if product.get("version_command"):
                            st.code(f"# Version Verification Command\n{product['version_command']}", language="bash")
                    with col_b:
                        if provenance:
                            prov_info = provenance[0]
                            source_url = prov_info.get("source_url") or prov_info.get("ds_url") or "#"
                            conf = prov_info.get("ds_confidence") or prov_info.get("confidence_score") or 1.0
                            st.caption(f"**Source:** [{prov_info['source_name']}]({source_url})")
                            st.caption(f"**License:** {prov_info.get('license', 'N/A')}")
                            st.caption(f"**Provenance Score:** {int(conf * 100)}%")

                    st.subheader(f"Release Cycles ({len(cycles)})")
                    if cycles:
                        df_data = []
                        for c in cycles:
                            status = "🔴 End of Life (EOL)" if c["is_eol"] else ("🟢 Supported" if c["is_maintained"] else "🟡 Security Support")
                            lts_badge = "✅ LTS" if c["is_lts"] else "Standard"
                            latest_ver = c["latest_version"] or "N/A"
                            df_data.append({
                                "Release Cycle": c["cycle"],
                                "Release Date": c["release_date"] or "N/A",
                                "End of Active Support": c["eoas_date"] or "N/A",
                                "End of Life (EOL) Date": c["eol_date"] or "N/A",
                                "LTS Status": lts_badge,
                                "Status": status,
                                "Latest Version": latest_ver
                            })
                        st.dataframe(pd.DataFrame(df_data), use_container_width=True)
                    else:
                        st.write("No release cycles recorded for this product.")


# ==========================================
# TAB 2: Runtime Environment Risk Dashboard
# ==========================================
elif nav_choice == "🛡️ Runtime Environment Risk Dashboard":
    st.title("🛡️ Enterprise Runtime Environment Risk Dashboard")
    st.markdown("Track and monitor active runtime environments against EOL schedules, dynamically calculated based on current system date.")

    risk_data = search_svc.get_inventory_risk_summary()
    items = risk_data["items"]

    # Key Performance Indicators
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tracked Environments", risk_data["total_items"])
    m2.metric("Critical (EOL)", risk_data["critical_eol_count"], delta="-Immediate Action", delta_color="inverse")
    m3.metric("High Risk (EOL < 6 Mo)", risk_data["high_risk_count"], delta="Migration Needed", delta_color="off")
    m4.metric("Low Risk (Active)", risk_data["low_risk_count"], delta="Healthy", delta_color="normal")

    st.divider()

    if items:
        df_inv = pd.DataFrame(items)

        # Display controls
        c1, c2 = st.columns([2, 2])
        with c1:
            risk_filter = st.multiselect("Filter by Risk Level", options=["CRITICAL (EOL)", "HIGH", "LOW"], default=["CRITICAL (EOL)", "HIGH", "LOW"])
        with c2:
            status_filter = st.multiselect("Filter by Migration Status", options=list(set(df_inv["migration_status"])), default=list(set(df_inv["migration_status"])))

        filtered_df = df_inv[
            (df_inv["risk_level"].isin(risk_filter)) &
            (df_inv["migration_status"].isin(status_filter))
        ]

        display_cols = [
            "platform", "version", "release_type", "deployment_env", "release_date",
            "eoas_date", "eol_date", "lifecycle_phase", "days_to_eol", "risk_level",
            "target_upgrade_path", "migration_status"
        ]

        renamed_df = filtered_df[display_cols].rename(columns={
            "platform": "Runtime / Platform",
            "version": "Version",
            "release_type": "Release Type",
            "deployment_env": "Deployment Environment",
            "release_date": "Release Date",
            "eoas_date": "End of Active Support",
            "eol_date": "End of Life (EOL) Date",
            "lifecycle_phase": "Lifecycle Phase",
            "days_to_eol": "Days to EOL",
            "risk_level": "Risk Level",
            "target_upgrade_path": "Target Upgrade Path",
            "migration_status": "Migration Action Status"
        })

        st.dataframe(
            renamed_df.style.map(
                lambda val: 'background-color: #ffcccc; color: #990000; font-weight: bold;' if 'CRITICAL' in str(val) else ('background-color: #fff0c2; color: #664d00;' if 'HIGH' in str(val) else ''),
                subset=['Risk Level']
            ),
            use_container_width=True
        )

        st.download_button(
            label="📥 Export Risk Report (CSV)",
            data=renamed_df.to_csv(index=False).encode('utf-8'),
            file_name="Active_Runtime_Environment_Risk_Report.csv",
            mime="text/csv"
        )
    else:
        st.info("No runtime inventory items found. Upload an inventory CSV in the Data Ingestion tab.")


# ==========================================
# TAB 3: Integrated Data Sources Registry
# ==========================================
elif nav_choice == "📚 Integrated Data Sources Registry":
    sources = db.get_all_data_sources()
    st.title(f"📚 Software EOL Data Sources Registry ({len(sources)} Integrated Feeds)")
    st.markdown("Comprehensive directory of all primary APIs, vendor portals, standards (TEA / ECMA-428 CLE), and aggregators powering the database.")

    st.write(f"Total Registered Sources: **{len(sources)}**")

    # Filters
    f1, f2 = st.columns(2)
    with f1:
        cat_select = st.selectbox("Filter Source Category", ["All Categories"] + sorted({s["category"] for s in sources}))
    with f2:
        search_src = st.text_input("Search Source Name / Keyword", "")

    filtered_sources = sources
    if cat_select != "All Categories":
        filtered_sources = [s for s in filtered_sources if s["category"] == cat_select]
    if search_src:
        q = search_src.lower()
        filtered_sources = [s for s in filtered_sources if q in s["name"].lower() or q in s["description"].lower()]

    src_df = pd.DataFrame(filtered_sources)
    if not src_df.empty:
        st.dataframe(
            src_df[["name", "category", "format", "api_available", "confidence_score", "url", "description"]].rename(columns={
                "name": "Source Name",
                "category": "Platform Category",
                "format": "Data Format",
                "api_available": "API Availability",
                "confidence_score": "Confidence Rating",
                "url": "Access URL",
                "description": "Description"
            }),
            use_container_width=True
        )
    else:
        st.warning("No data sources matching search filter.")


# ==========================================
# TAB 4: Data Provenance & Audit Inspector
# ==========================================
elif nav_choice == "📜 Data Provenance & Audit Inspector":
    st.title("📜 Data Provenance & Audit Trail Inspector")
    st.markdown("Inspect cryptographic hashes, original source URLs, verification timestamps, and licenses for all database records.")

    entity_type = st.selectbox("Entity Type", ["product", "release_cycle", "inventory"])

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.entity_type, p.entity_id, p.source_name, p.source_url, p.license, p.confidence_score, p.fetched_at, p.notes, d.name as registry_source
            FROM provenance_records p
            LEFT JOIN data_sources d ON p.data_source_id = d.id
            WHERE p.entity_type = ?
            ORDER BY p.fetched_at DESC;
        """, (entity_type,))
        prov_rows = [dict(r) for r in cursor.fetchall()]

    st.write(f"Total Audit Provenance Records for `{entity_type}`: **{len(prov_rows)}**")
    if prov_rows:
        prov_df = pd.DataFrame(prov_rows)
        st.dataframe(prov_df[["id", "entity_id", "source_name", "source_url", "license", "confidence_score", "fetched_at", "notes"]], use_container_width=True)
    else:
        st.write("No provenance records found for this entity type.")


# ==========================================
# TAB 5: Data Ingestion & Management
# ==========================================
elif nav_choice == "⚙️ Data Ingestion & Management":
    st.title("⚙️ Data Ingestion & Database Management")
    st.markdown("Synchronize data from primary EOL APIs, enterprise software suites (Jira, OpenText, IBM, SAP, Cisco), or upload CSV inventories.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌐 Sync Enterprise Suites & Vendor Catalogs")
        st.write("Ingest Atlassian (Jira, Confluence), OpenText / Micro Focus (ALM, Content Suite, Vertica), IBM, SAP, Cisco, ServiceNow, and Splunk.")

        if st.button("Ingest All Enterprise Software Suites (Jira, OpenText, IBM, SAP, Cisco, etc.)"):
            with st.spinner("Ingesting Enterprise Vendor Suites..."):
                cnt = ent_svc.ingest_all_enterprise_suites()
                st.success(f"Successfully ingested {cnt} enterprise software product suites!")

        st.divider()
        if st.button("⚡ Full GitHub & REST API Bulk Sync (473+ Products & 8,600+ Cycles)"):
            with st.spinner("Executing full bulk batch sync across all 473+ products and 8,600+ release cycles..."):
                prods, cycles = sync_svc.sync_all_products_bulk()
                st.success(f"Successfully bulk synced {prods} products and {cycles} release cycles with full provenance tracking!")

        st.divider()
        sync_single = st.text_input("Sync Specific Product Slug (e.g. 'python', 'ubuntu', 'kubernetes')", "kubernetes")
        if st.button("Sync Single Product from REST API"):
            with st.spinner(f"Fetching '{sync_single}'..."):
                ok = sync_svc.sync_product(sync_single)
                if ok:
                    st.success(f"Successfully synced '{sync_single}' with full provenance!")
                else:
                    st.error(f"Failed to sync product '{sync_single}'. Check if slug exists.")

    with col2:
        st.subheader("📄 Import Active Runtime Inventory CSV")
        st.write("Upload a CSV file with enterprise runtime environment inventory records.")

        uploaded_csv = st.file_uploader("Choose Inventory CSV", type=["csv"])
        if uploaded_csv is not None and st.button("Process & Import CSV"):
            with st.spinner("Processing CSV and calculating dynamic EOL risk metrics..."):
                count = csv_imp.import_inventory_csv(uploaded_csv, source_name="Uploaded Enterprise CSV")
                st.success(f"Successfully imported {count} inventory records!")

    st.divider()
    st.subheader("🛡️ NIST NVD CPE 2.0 API Extractor & Database Ingestion")
    st.markdown("Extract and parse enterprise software and OS catalog entries directly from the **NIST National Vulnerability Database (NVD) CPE 2.0 API** with full CPE 2.3 URI decomposition.")

    cpe_col1, cpe_col2, cpe_col3 = st.columns([2, 2, 2])
    with cpe_col1:
        target_count = st.number_input("Target Records Count", min_value=10, max_value=50000, value=1000, step=250)
    with cpe_col2:
        dedup_products = st.checkbox("Deduplicate (Vendor + Product)", value=True)
    with cpe_col3:
        api_key_input = st.text_input("NVD API Key (Optional)", type="password", help="Increases rate limit threshold from 5 to 50 req/30s")

    if st.button("Extract & Ingest NVD CPE Catalog"):
        with st.spinner(f"Paginating NIST NVD CPE 2.0 API for {target_count} records..."):
            key_val = api_key_input.strip() if api_key_input else None
            records = fetch_cpe_catalog(
                target_count=int(target_count),
                deduplicate_products=dedup_products,
                api_key=key_val
            )
            count = ingest_nvd_cpe_into_db(db=db, records=records)
            st.success(f"Successfully extracted {len(records)} CPE records and ingested {count} products into database with NIST provenance links!")

    st.divider()
    st.subheader("➕ Register Custom Niche Software EOL Record")
    with st.form("custom_software_form"):
        st.caption("Manually register software EOL dates for niche or proprietary enterprise software with provenance tracking.")
        c_slug = st.text_input("Product Slug", "my-custom-niche-app")
        c_name = st.text_input("Product Label", "My Custom Niche App")
        c_cat = st.selectbox("Category", ["os", "lang", "framework", "database", "server-app", "niche-app", "service"])
        c_cycle = st.text_input("Release Cycle", "1.0")
        c_eol = st.text_input("EOL Date (YYYY-MM-DD)", "2027-12-31")
        c_source = st.text_input("Provenance Source Name", "Internal Vendor Contract / SLA")
        c_url = st.text_input("Provenance Source Document / URL", "https://internal.company.com/sla/app-1.0")

        submitted = st.form_submit_button("Register Custom Software")
        if submitted:
            pid = db.upsert_product(slug=c_slug.lower(), name=c_name, label=c_name, category=c_cat)
            cid = db.upsert_release_cycle(product_id=pid, cycle=c_cycle, eol_date=c_eol, is_eol=False)
            db.add_provenance("product", pid, source_name=c_source, source_url=c_url, confidence_score=0.9, notes="Manual entry for niche app")
            st.success(f"Custom niche software '{c_name}' cycle {c_cycle} registered with provenance!")
