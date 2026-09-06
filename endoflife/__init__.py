"""
Endoflife API Client Library
Official API documentation: https://endoflife.date/docs/api/v1/
"""

from .client import (
    EndoflifeAPIError,
    EndoflifeClient,
    RateLimitError,
    ResourceNotFoundError,
)
from .models import (
    ProductDetails,
    ProductSummary,
    ProductVersion,
    ReleaseCycle,
    ResourceLink,
)

__version__ = "0.1.0"
__all__ = [
    "EndoflifeAPIError",
    "EndoflifeClient",
    "ProductDetails",
    "ProductSummary",
    "ProductVersion",
    "RateLimitError",
    "ReleaseCycle",
    "ResourceLink",
    "ResourceNotFoundError",
]
