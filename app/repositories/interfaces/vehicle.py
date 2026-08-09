"""VehicleRepository interface (Task A.3)."""

from datetime import datetime
from typing import List, Optional, Protocol

from app.core.enums import VehicleType
from app.repositories.models import GeoPoint, Vehicle


class VehicleRepository(Protocol):
    async def create(
        self,
        transporter_id: str,
        type: VehicleType,
        capacity_kg: float,
        capacity_volume: Optional[float],
        route_pref: Optional[str],
    ) -> Vehicle:
        """Register a new vehicle for a transporter."""
        ...

    async def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        """Fetch a vehicle by id, or None if it doesn't exist. (Note:
        several other VehicleRepository operations below raise
        NotFoundError instead of returning None for an unknown vehicle_id
        — get_by_id is the one read-only lookup that stays Optional so
        callers can do existence checks without a try/except.)"""
        ...

    async def list_by_transporter(self, transporter_id: str) -> List[Vehicle]:
        """List every vehicle owned by a transporter."""
        ...

    async def find_within_radius(
        self, point: GeoPoint, radius_km: float, min_capacity_kg: float
    ) -> List[Vehicle]:
        """C.2's core query: vehicles within radius_km of `point` whose
        capacity_kg >= min_capacity_kg.

        CRITICAL — real-implementation note for Kishor (mirrored in
        shared/contracts/repository-interfaces.md): once backed by
        PostgreSQL+PostGIS, this needs a GIST index on
        vehicles.current_location (per the technical spec's
        `CREATE INDEX ON vehicles USING GIST (current_location);`) or this
        query becomes a full table scan at any meaningful vehicle count.
        This is the exact note C.2 (Sprint 3) depends on existing before
        Kishor's real implementation lands.
        """
        ...

    async def update_location(
        self, vehicle_id: str, lat: float, lng: float, ts: datetime
    ) -> None:
        """E.1 write path: update a vehicle's current_location and
        last_ping_at from a `location_update` socket event. Raises
        NotFoundError for an unknown vehicle_id."""
        ...

    async def is_available(self, vehicle_id: str) -> bool:
        """C.5 re-validation: is this vehicle still available for
        assignment at commit time (Hungarian batch's 'vehicle becomes
        unavailable mid-computation' edge case)? Raises NotFoundError for
        an unknown vehicle_id."""
        ...
