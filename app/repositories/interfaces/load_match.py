"""LoadMatchRepository interface (Task A.3)."""

from typing import List, Optional, Protocol

from app.core.enums import LoadMatchStatus
from app.repositories.models import LoadMatch


class LoadMatchRepository(Protocol):
    async def create(
        self,
        load_id: str,
        vehicle_id: str,
        status: LoadMatchStatus,
        match_score: Optional[float],
    ) -> LoadMatch:
        """Record a proposed/accepted match between a load and a vehicle.

        Raises ConflictError if the vehicle already has an active match
        (status PROPOSED or ACCEPTED — i.e. not REJECTED/EXPIRED/CANCELLED)
        for a *different* load. This is the 'match no longer available'
        race Keval's Frontend UI has a defined state for; the
        implementation must be strict here, or Frontend testing against
        the mock won't catch bugs the real DB's constraints would later
        catch (per A.3 requirement 5)."""
        ...

    async def get_by_load_and_vehicle(
        self, load_id: str, vehicle_id: str
    ) -> Optional[LoadMatch]:
        """Fetch a specific load/vehicle match pairing, or None."""
        ...

    async def update_status(self, match_id: str, status: LoadMatchStatus) -> None:
        """Transition a match's status (e.g. PROPOSED -> ACCEPTED on
        POST /loads/{id}/accept). Raises NotFoundError for an unknown
        match_id."""
        ...

    async def list_by_load(self, load_id: str) -> List[LoadMatch]:
        """List every match (any status) proposed for a given load."""
        ...
