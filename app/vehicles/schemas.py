"""
vehicles — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Vehicle registration and compliance document upload.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - POST /vehicles
  - GET /vehicles/{id}
  - GET /vehicles
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class GeoPoint(BaseModel):
    lat: float
    lng: float

    @field_validator("lat")
    def lat_in_range(cls, value: float) -> float:
        if value < -90 or value > 90:
            raise ValueError("lat must be between -90 and 90")
        return value

    @field_validator("lng")
    def lng_in_range(cls, value: float) -> float:
        if value < -180 or value > 180:
            raise ValueError("lng must be between -180 and 180")
        return value


class VehicleType(str, Enum):
    MINI_TRUCK = "mini_truck"
    CONTAINER_TRUCK = "container_truck"
    TRAILER = "trailer"
    OTHER = "other"


class VehicleCreateRequest(BaseModel):
    type: VehicleType
    capacity_kg: float
    capacity_volume: Optional[float] = None
    route_pref: Optional[str] = None

    @field_validator("capacity_kg")
    def validate_capacity_kg(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("capacity_kg must be positive")
        return value

    @field_validator("capacity_volume")
    def validate_capacity_volume(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and value <= 0:
            raise ValueError("capacity_volume must be positive")
        return value


class VehiclesPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class VehiclesPlaceholderResponse(BaseModel):
    """Placeholder response model — see VehiclesPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
