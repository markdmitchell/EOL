"""
Endoflife API Client Library
Official API documentation: https://endoflife.date/docs/api/v1/
"""

from .client import (
    EndoflifeClient,
    EndoflifeAPIError,
    ResourceNotFoundError,
    RateLimitError,
)
from .models import ProductSummary, ProductDetails, ReleaseCycle, ResourceLink, ProductVersion

__version__ = "0.1.0"
__all__ = [
    "EndoflifeClient",
    "EndoflifeAPIError",
    "ResourceNotFoundError",
    "RateLimitError",
    "ProductSummary",
    "ProductDetails",
    "ReleaseCycle",
    "ResourceLink",
    "ProductVersion",
]
