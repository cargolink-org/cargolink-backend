"""InMemoryVehicleRepository (Task A.3)."""

from __future__ import annotations

import math
from datetime import datetime
from typing import Dict, List, Optional

from app.core.enums import VehicleType
from app.repositories.exceptions import NotFoundError
from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import GeoPoint, Vehicle, new_id


def _haversine_km(a: GeoPoint, b: GeoPoint) -> float:
    """Straight-line distance, used ONLY as the mock's stand-in for the
    real implementation's PostGIS ST_DWithin/GIST-indexed query — this is
    exactly the C.1 'Haversine fallback' logic pattern, reused here
    because the mock has no real geospatial engine, not because the mock
    is trying to be road-accurate."""
    r_km = 6371.0
    lat1, lng1, lat2, lng2 = map(math.radians, (a.lat, a.lng, b.lat, b.lng))
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * r_km * math.asin(math.sqrt(h))


class InMemoryVehicleRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, Vehicle] = {}
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("vehicles.json")
        if not records:
            return
        for row in records:
            try:
                location = None
                if row.get("current_location"):
                    loc = row["current_location"]
                    location = GeoPoint(lat=loc["lat"], lng=loc["lng"])
                vehicle = Vehicle(
                    id=row.get("id") or new_id(),
                    transporter_id=row["transporter_id"],
                    type=VehicleType(row["type"]),
                    capacity_kg=float(row["capacity_kg"]),
                    capacity_volume=row.get("capacity_volume"),
                    route_pref=row.get("route_pref"),
                    current_location=location,
                    is_available=row.get("is_available", True),
                )
            except (KeyError, ValueError):
                continue
            self._by_id[vehicle.id] = vehicle

    async def create(
        self,
        transporter_id: str,
        type: VehicleType,
        capacity_kg: float,
        capacity_volume: Optional[float],
        route_pref: Optional[str],
    ) -> Vehicle:
        vehicle = Vehicle(
            id=new_id(),
            transporter_id=transporter_id,
            type=type,
            capacity_kg=capacity_kg,
            capacity_volume=capacity_volume,
            route_pref=route_pref,
        )
        self._by_id[vehicle.id] = vehicle
        return vehicle

    async def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        return self._by_id.get(vehicle_id)

    async def list_by_transporter(self, transporter_id: str) -> List[Vehicle]:
        return [v for v in self._by_id.values() if v.transporter_id == transporter_id]

    async def find_within_radius(
        self, point: GeoPoint, radius_km: float, min_capacity_kg: float
    ) -> List[Vehicle]:
        results = []
        for vehicle in self._by_id.values():
            if vehicle.current_location is None:
                continue
            if vehicle.capacity_kg < min_capacity_kg:
                continue
            distance = _haversine_km(point, vehicle.current_location)
            if distance <= radius_km:  # inclusive boundary, per C.2's documented choice
                results.append(vehicle)
        return results

    async def update_location(self, vehicle_id: str, lat: float, lng: float, ts: datetime) -> None:
        vehicle = self._by_id.get(vehicle_id)
        if vehicle is None:
            raise NotFoundError(f"No vehicle with id={vehicle_id!r}")
        vehicle.current_location = GeoPoint(lat=lat, lng=lng)
        vehicle.last_ping_at = ts

    async def is_available(self, vehicle_id: str) -> bool:
        vehicle = self._by_id.get(vehicle_id)
        if vehicle is None:
            raise NotFoundError(f"No vehicle with id={vehicle_id!r}")
        return vehicle.is_available
