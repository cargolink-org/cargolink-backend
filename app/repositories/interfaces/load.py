"""LoadRepository interface (Task A.3)."""

from datetime import datetime
from typing import List, Optional, Protocol

from app.core.enums import CargoType, LoadStatus
from app.repositories.models import GeoPoint, Load


class LoadRepository(Protocol):
    async def create(
        self,
        shipper_id: str,
        weight: float,
        cargo_type: CargoType,
        source: GeoPoint,
        destination: GeoPoint,
        deadline: datetime,
    ) -> Load:
        """Post a new cargo requirement, status POSTED."""
        ...

    async def get_by_id(self, load_id: str) -> Optional[Load]:
        """Fetch a load by id, or None if it doesn't exist."""
        ...

    async def get_owner_id(self, load_id: str) -> str:
        """Ownership-check helper (used across F.1/F.2/F.3/D.1's 'shipper
        can only act on their own loads' checks). Raises NotFoundError if
        load_id doesn't exist."""
        ...

    async def update_status(self, load_id: str, status: LoadStatus) -> None:
        """Transition a load's lifecycle status. Raises NotFoundError for
        an unknown load_id."""
        ...

    async def list_open(self) -> List[Load]:
        """C.5 Hungarian batch input: every load still open for matching
        (status POSTED, not yet ACCEPTED/CANCELLED/DELIVERED)."""
        ...
