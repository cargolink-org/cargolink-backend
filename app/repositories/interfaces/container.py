"""ContainerRepository interface (Task A.3)."""

from typing import Optional, Protocol

from app.repositories.models import Container


class ContainerRepository(Protocol):
    async def get_by_load(self, load_id: str) -> Optional[Container]:
        """Fetch container data for a load, or None for purely road
        freight (F.3's 'cleanly absent' edge case — must not raise)."""
        ...

    async def upsert(
        self,
        load_id: str,
        container_no: Optional[str],
        vessel_or_flight: Optional[str],
        port_of_loading: Optional[str],
        port_of_discharge: Optional[str],
    ) -> Container:
        """Create or update the single container record for a load."""
        ...
