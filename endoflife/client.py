import json
import urllib.error
import urllib.request
from typing import Any

from .models import (
    ProductDetails,
    ProductSummary,
    ReleaseCycle,
    ResourceLink,
)

BASE_URL = "https://endoflife.date/api/v1"

class EndoflifeAPIError(Exception):
    """Base exception for Endoflife API errors."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code

class ResourceNotFoundError(EndoflifeAPIError):
    """Raised when a product, release, category, tag, or identifier is not found (404)."""

class RateLimitError(EndoflifeAPIError):
    """Raised when rate limit is exceeded (429)."""

class EndoflifeClient:
    """
    Client for interacting with the endoflife.date v1 REST API.
    """

    def __init__(self, base_url: str = BASE_URL, timeout: int = 15, user_agent: str = "endoflife-python-sdk/0.1.0"):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent

    def _request(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"
        if not url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL protocol scheme in '{url}'. Only HTTP/HTTPS permitted.")
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
                if isinstance(payload, dict) and "result" in payload:
                    return payload["result"]
                return payload
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ResourceNotFoundError(f"Resource at '{endpoint}' not found.", status_code=404) from e
            elif e.code == 429:
                raise RateLimitError("Rate limit exceeded. Please retry later.", status_code=429) from e
            else:
                raise EndoflifeAPIError(f"HTTP {e.code}: {e.reason}", status_code=e.code) from e
        except urllib.error.URLError as e:
            raise EndoflifeAPIError(f"Connection failed: {e.reason}") from e

    def get_index(self) -> list[ResourceLink]:
        """List main API endpoints."""
        data = self._request("/")
        return [ResourceLink.from_dict(item) for item in data]

    def get_products(self) -> list[ProductSummary]:
        """List all tracked products summary."""
        data = self._request("/products")
        return [ProductSummary.from_dict(item) for item in data]

    def get_products_full(self) -> list[ProductDetails]:
        """List all products with complete release and identifier details."""
        data = self._request("/products/full")
        return [ProductDetails.from_dict(item) for item in data]

    def get_product(self, product: str) -> ProductDetails:
        """Get full details and release history for a specific product."""
        data = self._request(f"/products/{product}")
        return ProductDetails.from_dict(data)

    def get_release(self, product: str, release: str) -> ReleaseCycle:
        """Get information for a specific product release cycle."""
        data = self._request(f"/products/{product}/releases/{release}")
        return ReleaseCycle.from_dict(data)

    def get_latest_release(self, product: str) -> ReleaseCycle:
        """Get the latest release cycle information for a product."""
        data = self._request(f"/products/{product}/releases/latest")
        return ReleaseCycle.from_dict(data)

    def get_categories(self) -> list[ResourceLink]:
        """List all categories."""
        data = self._request("/categories")
        return [ResourceLink.from_dict(item) for item in data]

    def get_category_products(self, category: str) -> list[ProductSummary]:
        """List all products within a specific category."""
        data = self._request(f"/categories/{category}")
        return [ProductSummary.from_dict(item) for item in data]

    def get_tags(self) -> list[ResourceLink]:
        """List all tags."""
        data = self._request("/tags")
        return [ResourceLink.from_dict(item) for item in data]

    def get_tagged_products(self, tag: str) -> list[ProductSummary]:
        """List all products matching a specific tag."""
        data = self._request(f"/tags/{tag}")
        return [ProductSummary.from_dict(item) for item in data]

    def get_identifier_types(self) -> list[ResourceLink]:
        """List all identifier types (e.g. purl, cpe)."""
        data = self._request("/identifiers")
        return [ResourceLink.from_dict(item) for item in data]

    def get_identifiers(self, identifier_type: str) -> list[dict[str, Any]]:
        """List all identifiers for a given type."""
        return self._request(f"/identifiers/{identifier_type}")
