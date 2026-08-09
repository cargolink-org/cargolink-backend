"""ShipperProfileRepository interface (Task A.3)."""

from typing import Optional, Protocol

from app.repositories.models import ShipperProfile


class ShipperProfileRepository(Protocol):
    async def get_by_user_id(self, user_id: str) -> Optional[ShipperProfile]:
        """Fetch a shipper's profile, or None if they haven't completed
        profile setup yet."""
        ...

    async def upsert(
        self, user_id: str, company_name: Optional[str], gstin: Optional[str]
    ) -> ShipperProfile:
        """Create or update a shipper's profile. gstin is optional per the
        technical spec's schema (nullable business-registration field)."""
        ...
