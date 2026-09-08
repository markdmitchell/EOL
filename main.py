"""
Example script demonstrating how to connect to and query the endoflife.date API.
"""

from endoflife import EndoflifeClient, ResourceNotFoundError


def main():
    client = EndoflifeClient()

    print("=== endoflife.date API Demo ===\n")

    # 1. Fetch products summary
    print("1. Fetching all available products...")
    products = client.get_products()
    print(f"Total products available: {len(products)}")
    sample_names = [p.name for p in products[:8]]
    print(f"Sample products: {', '.join(sample_names)}\n")

    # 2. Fetch specific product details (e.g. Python)
    print("2. Fetching details for 'python'...")
    python_info = client.get_product("python")
    print(f"Product: {python_info.label}")
    print(f"Category: {python_info.category}")
    print(f"Tags: {', '.join(python_info.tags)}")
    print(f"Version check command: {python_info.version_command.strip() if python_info.version_command else 'N/A'}")

    print("\nRecent Python releases:")
    for rel in python_info.releases[:5]:
        eol_str = f"EOL since {rel.eol_from}" if rel.is_eol else f"Supported until {rel.eol_from or 'TBD'}"
        latest = rel.latest.name if rel.latest else "N/A"
        print(f"  Cycle {rel.name:<6}: Released {rel.release_date} | {eol_str:<30} | Latest: {latest}")

    # 3. Fetch specific product details (e.g. Ubuntu)
    print("\n3. Fetching latest release cycle for 'ubuntu'...")
    ubuntu_latest = client.get_latest_release("ubuntu")
    print(f"Ubuntu latest cycle: {ubuntu_latest.name} ({ubuntu_latest.label})")
    print(f"Is LTS: {ubuntu_latest.is_lts}")
    print(f"EOL date: {ubuntu_latest.eol_from}")

    # 4. Error handling demonstration
    print("\n4. Handling missing product lookup...")
    try:
        client.get_product("fake-product-name")
    except ResourceNotFoundError as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    main()
