"""
loads — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Load posting and lifecycle.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - POST /loads
  - GET /loads/{id}
  - POST /loads/{id}/accept
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from app.vehicles.schemas import GeoPoint
from pydantic import BaseModel, Field, field_validator


class CargoType(str, Enum):
    GENERAL = "general"
    FRAGILE = "fragile"
    HAZARDOUS = "hazardous"
    REFRIGERATED = "refrigerated"


class LoadCreateRequest(BaseModel):
    weight: float
    cargo_type: CargoType
    source: GeoPoint
    destination: GeoPoint
    deadline: datetime

    @field_validator("weight")
    def weight_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("weight must be positive")
        return value

    @field_validator("deadline")
    def deadline_required(cls, value: datetime) -> datetime:
        if value is None:
            raise ValueError("deadline is required")
        return value


class LoadsPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class LoadsPlaceholderResponse(BaseModel):
    """Placeholder response model — see LoadsPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
