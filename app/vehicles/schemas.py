"""Vehicle registration & read contract.

Inference note: not explicitly enumerated in the technical spec's §5
endpoint list; routes below are inferred from the `vehicles` table (§4)
and the Frontend "vehicle registration + document upload UI" task, using
the smallest reasonable REST shape:

    POST /vehicles           register a vehicle owned by the calling transporter
    GET  /vehicles/{id}      read a single vehicle
    GET  /vehicles           list the calling transporter's own vehicles

`GeoPoint` is defined here (not duplicated per-domain) because it is
reused by loads/schemas.py (source/destination) and tracking/schemas.py's
LocationPoint follows the same lat/lng bounds.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class VehicleType(str, Enum):
    MINI_TRUCK = "mini_truck"
    CONTAINER_TRUCK = "container_truck"
    TRAILER = "trailer"
    OTHER = "other"


class GeoPoint(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees (WGS84).")
    lng: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees (WGS84).")


class VehicleCreateRequest(BaseModel):
    type: VehicleType = Field(..., description="Vehicle category.")
    capacity_kg: float = Field(..., gt=0, description="Maximum cargo weight capacity, in kilograms.")
    capacity_volume: float = Field(..., gt=0, description="Maximum cargo volume capacity, in cubic meters.")
    route_pref: str | None = Field(
        None, max_length=200, description="Free-text preferred route/operating corridor, e.g. 'Mumbai-Pune'."
    )


class VehicleResponse(BaseModel):
    id: UUID = Field(..., description="Unique vehicle identifier.")
    transporter_id: UUID = Field(..., description="Owning transporter's user id.")
    type: VehicleType = Field(..., description="Vehicle category.")
    capacity_kg: float = Field(..., description="Maximum cargo weight capacity, in kilograms.")
    capacity_volume: float = Field(..., description="Maximum cargo volume capacity, in cubic meters.")
    route_pref: str | None = Field(None, description="Free-text preferred route/operating corridor.")
    current_location: GeoPoint | None = Field(
        None, description="Last known GPS location, if the vehicle has reported one."
    )
    last_ping_at: datetime | None = Field(None, description="Timestamp of the last location ping received.")


class VehicleListResponse(BaseModel):
    vehicles: list[VehicleResponse] = Field(..., description="The calling transporter's registered vehicles.")
