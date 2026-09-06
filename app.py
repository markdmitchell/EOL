
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
    page_title="Software EOL/EOS Database & Enterprise Intelligence",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_resource
def get_services():
    db = Database()
    search_svc = SearchService(db=db)
    sync_svc = SyncService(db=db)
    csv_imp = CSVImporter(db=db)
    ms_svc = MultiSourceService(db=db)
    ent_svc = EnterpriseVendorService(db=db)
    return db, search_svc, sync_svc, csv_imp, ms_svc, ent_svc

db, search_svc, sync_svc, csv_imp, ms_svc, ent_svc = get_services()

# --- Sidebar Header & Navigation ---
st.sidebar.image("https://img.icons8.com/color/96/shield.png", width=64)
st.sidebar.title("EOL/EOS Intelligence")
st.sidebar.caption("Enterprise Software Lifecycle Reference Portal")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🔍 Searchable Product Catalog",
        "🛡️ Runtime Environment Risk Dashboard",
        "📚 24 Data Sources Registry",
        "📜 Data Provenance & Audit Inspector",
        "⚙️ Data Ingestion & Management"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "**Enterprise Software & Provenance Guaranteed**\n"
    "Includes Atlassian (Jira, Confluence), OpenText / Micro Focus (ALM, Content Suite, Vertica), IBM, SAP, Cisco, ServiceNow, Splunk, Microsoft, Canonical, Red Hat, Oracle."
)


# ==========================================
# TAB 1: Searchable Product Catalog
# ==========================================
if nav_choice == "🔍 Searchable Product Catalog":
    st.title("🔍 Searchable Enterprise Software EOL/EOS Catalog")
    st.markdown("Search support lifecycles, EOL/EOS dates, and release cycles across **Jira, OpenText, Micro Focus, IBM DB2, SAP S/4HANA, Cisco, ServiceNow, Splunk**, OSs, Languages, and Databases.")

    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1.5])
    with col1:
        query_input = st.text_input("Search Product (e.g. Jira, OpenText, ALM, Vertica, WebSphere, SAP, Cisco, Python)", "")
    with col2:
        category_filter = st.selectbox("Category Filter", ["All Categories", "lang", "os", "framework", "database", "server-app"])
    with col3:
        vendor_filter = st.selectbox("Vendor Filter", ["All Vendors", "Atlassian", "OpenText / Micro Focus", "IBM Corporation", "SAP SE", "Cisco Systems", "ServiceNow, Inc.", "Splunk / Cisco", "Microsoft Corporation", "Red Hat, Inc.", "Canonical", "Oracle Corporation", "Google"])
    with col4:
        eol_only = st.checkbox("Only Show EOL Products/Cycles", value=False)

    cat_val = "" if category_filter == "All Categories" else category_filter
    results = search_svc.search_catalog(query=query_input, category=cat_val, eol_only=eol_only)

    if vendor_filter != "All Vendors":
        results = [r for r in results if r["product"].get("vendor") == vendor_filter]

    st.write(f"Showing **{len(results)}** matching enterprise products from database:")

    if not results:
        st.warning("No products found matching your search criteria. Try syncing more products from the 'Data Ingestion & Management' tab.")
    else:
        for item in results:
            product = item["product"]
            cycles = item["release_cycles"]
            provenance = item["provenance"]

            with st.expander(f"📦 **{product['label']}** ({product['slug']}) — Vendor: `{product.get('vendor') or 'N/A'}` | Category: `{product['category'] or 'N/A'}`", expanded=(len(results) == 1)):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**Vendor:** {product.get('vendor') or 'N/A'}")
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
# TAB 3: 24 Data Sources Registry
# ==========================================
elif nav_choice == "📚 24 Data Sources Registry":
    st.title("📚 Software EOL Data Sources Registry (24 Integrated Feeds)")
    st.markdown("Comprehensive directory of all primary APIs, vendor portals, standards (TEA / ECMA-428 CLE), and aggregators powering the database.")

    sources = db.get_all_data_sources()
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
        target_count = st.number_input("Target Records Count", min_value=10, max_value=5000, value=300, step=50)
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
