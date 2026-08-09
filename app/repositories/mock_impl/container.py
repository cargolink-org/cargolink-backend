"""InMemoryContainerRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, Optional

from app.repositories.models import Container


class InMemoryContainerRepository:
    def __init__(self) -> None:
        self._by_load: Dict[str, Container] = {}
        # No seed file — container data is entered per-load by F.3's
        # upload flow, not fixture data; a missing entry correctly means
        # "purely road freight" (see get_by_load below).

    async def get_by_load(self, load_id: str) -> Optional[Container]:
        # Returns None (not NotFoundError) for a load with no container
        # data — F.3's edge case: purely road freight must not error.
        return self._by_load.get(load_id)

    async def upsert(
        self,
        load_id: str,
        container_no: Optional[str],
        vessel_or_flight: Optional[str],
        port_of_loading: Optional[str],
        port_of_discharge: Optional[str],
    ) -> Container:
        container = Container(
            load_id=load_id,
            container_no=container_no,
            vessel_or_flight=vessel_or_flight,
            port_of_loading=port_of_loading,
            port_of_discharge=port_of_discharge,
        )
        self._by_load[load_id] = container
        return container
