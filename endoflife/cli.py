import argparse
import sys
from typing import Optional

from .client import EndoflifeClient, ResourceNotFoundError, EndoflifeAPIError

def main(args: Optional[list] = None) -> None:
    parser = argparse.ArgumentParser(
        prog="endoflife",
        description="CLI tool to query EOL (End-of-Life) dates and product lifecycles via endoflife.date"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: products
    products_parser = subparsers.add_parser("products", help="List products")
    products_parser.add_argument("-c", "--category", help="Filter by category")
    products_parser.add_argument("-t", "--tag", help="Filter by tag")
    products_parser.add_argument("-q", "--query", help="Filter by product name search")

    # Command: product
    product_parser = subparsers.add_parser("product", help="Get product details")
    product_parser.add_argument("name", help="Product name (e.g. python, ubuntu, nodejs)")

    # Command: release
    release_parser = subparsers.add_parser("release", help="Get specific release cycle info")
    release_parser.add_argument("name", help="Product name")
    release_parser.add_argument("cycle", help="Release cycle (e.g. 3.14, 22.04)")

    # Command: categories
    subparsers.add_parser("categories", help="List all categories")

    # Command: tags
    subparsers.add_parser("tags", help="List all tags")

    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    client = EndoflifeClient()

    try:
        if parsed.command == "products":
            if parsed.category:
                prods = client.get_category_products(parsed.category)
            elif parsed.tag:
                prods = client.get_tagged_products(parsed.tag)
            else:
                prods = client.get_products()

            if parsed.query:
                q = parsed.query.lower()
                prods = [p for p in prods if q in p.name.lower() or q in p.label.lower()]

            print(f"Found {len(prods)} product(s):")
            for p in prods:
                aliases_str = f" (aliases: {', '.join(p.aliases)})" if p.aliases else ""
                print(f"  - {p.label} [{p.name}]{aliases_str} - Category: {p.category or 'N/A'}")

        elif parsed.command == "product":
            details = client.get_product(parsed.name)
            print(f"=== {details.label} ({details.name}) ===")
            print(f"Category: {details.category or 'N/A'}")
            print(f"Tags: {', '.join(details.tags) if details.tags else 'N/A'}")
            if details.version_command:
                print(f"Version Command: {details.version_command.strip()}")
            print(f"\nReleases ({len(details.releases)} total):")
            print(f"{'Cycle':<12} {'Release Date':<15} {'EOL Status':<20} {'Latest Version'}")
            print("-" * 65)
            for r in details.releases:
                if r.is_eol:
                    eol_status = f"EOL ({r.eol_from or 'Yes'})"
                else:
                    eol_status = f"Supported (EOL: {r.eol_from or 'TBD'})"
                latest_str = r.latest.name if r.latest else "N/A"
                print(f"{r.name:<12} {r.release_date or 'N/A':<15} {eol_status:<20} {latest_str}")

        elif parsed.command == "release":
            rel = client.get_release(parsed.name, parsed.cycle)
            print(f"=== {parsed.name} Cycle: {rel.name} ===")
            print(f"Label: {rel.label or rel.name}")
            print(f"Release Date: {rel.release_date or 'N/A'}")
            print(f"Is LTS: {rel.is_lts} (From: {rel.lts_from or 'N/A'})")
            print(f"Is EOL: {rel.is_eol} (From: {rel.eol_from or 'N/A'})")
            print(f"Is Maintained: {rel.is_maintained}")
            if rel.latest:
                print(f"Latest Version: {rel.latest.name} (Released: {rel.latest.date or 'N/A'})")
                if rel.latest.link:
                    print(f"Changelog: {rel.latest.link}")

        elif parsed.command == "categories":
            cats = client.get_categories()
            print(f"Categories ({len(cats)}):")
            for c in cats:
                print(f"  - {c.name}")

        elif parsed.command == "tags":
            tags = client.get_tags()
            print(f"Tags ({len(tags)}):")
            for t in tags:
                print(f"  - {t.name}")

    except ResourceNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    except EndoflifeAPIError as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
