"""InMemoryLocationPingRepository (Task A.3)."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from app.repositories.models import LocationPing, new_id


class InMemoryLocationPingRepository:
    def __init__(self) -> None:
        self._by_vehicle: Dict[str, List[LocationPing]] = {}
        # No seed file — pings are a high-volume, time-series write path
        # generated at runtime by E.1's socket handler, not fixture data.

    async def create(self, vehicle_id: str, lat: float, lng: float, ts: datetime) -> LocationPing:
        ping = LocationPing(id=new_id(), vehicle_id=vehicle_id, lat=lat, lng=lng, ts=ts)
        self._by_vehicle.setdefault(vehicle_id, []).append(ping)
        return ping

    async def list_for_vehicle(
        self,
        vehicle_id: str,
        from_ts: Optional[datetime] = None,
        to_ts: Optional[datetime] = None,
    ) -> List[LocationPing]:
        pings = self._by_vehicle.get(vehicle_id, [])
        if from_ts is not None:
            pings = [p for p in pings if p.ts >= from_ts]
        if to_ts is not None:
            pings = [p for p in pings if p.ts <= to_ts]
        return list(pings)

    async def get_latest(self, vehicle_id: str) -> Optional[LocationPing]:
        pings = self._by_vehicle.get(vehicle_id)
        if not pings:
            return None
        return max(pings, key=lambda p: p.ts)
