# endoflife.date API Python Client

A clean Python library and CLI tool for interacting with the [endoflife.date](https://endoflife.date) v1 REST API.

## Features

- **No Third-Party Dependencies Required**: Built using Python 3 standard libraries (`urllib`, `json`, `dataclasses`).
- **Complete Endpoint Coverage**: Supports products, release cycles, categories, tags, and product identifiers.
- **Type-Safe Data Models**: Clean dataclasses (`ProductSummary`, `ProductDetails`, `ReleaseCycle`, `ProductVersion`).
- **CLI Utility Included**: Run `python -m endoflife.cli` to query end-of-life status directly from the command line.

## Quick Start

### Python Usage

```python
from endoflife import EndoflifeClient

client = EndoflifeClient()

# Get details and release cycles for a product
python_info = client.get_product("python")
print(f"Product: {python_info.label}")

for release in python_info.releases:
    print(f"Cycle {release.name}: EOL={release.is_eol}, Date={release.eol_from}")

# Get latest release cycle
latest = client.get_latest_release("ubuntu")
print(f"Latest Ubuntu Cycle: {latest.name}, EOL={latest.eol_from}")
```

### CLI Usage

```powershell
# List products matching a search query
python -m endoflife.cli products -q python

# Display product details & release cycles table
python -m endoflife.cli product nodejs

# Get specific release info
python -m endoflife.cli release ubuntu 24.04

# List categories
python -m endoflife.cli categories
```

## Running Tests

Execute the unit test suite:

```powershell
python -m unittest discover -s tests
```
