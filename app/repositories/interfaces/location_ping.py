"""LocationPingRepository interface (Task A.3)."""

from datetime import datetime
from typing import List, Optional, Protocol

from app.repositories.models import LocationPing


class LocationPingRepository(Protocol):
    async def create(
        self, vehicle_id: str, lat: float, lng: float, ts: datetime
    ) -> LocationPing:
        """E.1 write path: persist a single location ping before
        broadcasting to the load's socket room."""
        ...

    async def list_for_vehicle(
        self,
        vehicle_id: str,
        from_ts: Optional[datetime] = None,
        to_ts: Optional[datetime] = None,
    ) -> List[LocationPing]:
        """GET /tracking/{vehicleId}?from=&to= — historical location
        read path. Both bounds optional; omitting both returns full
        history (callers should paginate/limit above this layer for a
        long-running trip)."""
        ...

    async def get_latest(self, vehicle_id: str) -> Optional[LocationPing]:
        """Most recent ping for a vehicle, or None if it has never
        reported a location."""
        ...
