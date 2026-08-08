"""Load posting & acceptance contract.

Module-boundary decision (A.2 task instructions ask us to choose): `loads`
is its own app/ module, owning load *lifecycle* endpoints (POST /loads,
POST /loads/{id}/accept). `GET /loads/{id}/matches` stays in
app/matching/ — per the implementation guide's own framing ("GET
/loads/{id}/matches is explicitly matching-engine territory"), that
endpoint's query logic belongs with the matching engine (Cluster C), not
load CRUD. This keeps `loads/` about the load *resource* and `matching/`
about the *algorithm*, mirroring how Cluster C's own files (engine.py,
hungarian.py, graph.py) are organized in the backend guide.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from app.vehicles.schemas import GeoPoint


class CargoType(str, Enum):
    GENERAL = "general"
    FRAGILE = "fragile"
    HAZARDOUS = "hazardous"
    REFRIGERATED = "refrigerated"


class LoadStatus(str, Enum):
    OPEN = "open"
    MATCHED = "matched"
    ACCEPTED = "accepted"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class LoadCreateRequest(BaseModel):
    weight: float = Field(..., gt=0, description="Cargo weight in kilograms.")
    cargo_type: CargoType = Field(..., description="Category of cargo being shipped.")
    source: GeoPoint = Field(..., description="Pickup location.")
    destination: GeoPoint = Field(..., description="Drop-off location.")
    deadline: datetime = Field(..., description="Latest acceptable pickup deadline.")


class LoadCreateResponse(BaseModel):
    load_id: UUID = Field(..., description="Unique identifier for the newly posted load.")
    status: LoadStatus = Field(..., description="Initial load status (always 'open' on creation).")


class LoadAcceptRequest(BaseModel):
    vehicle_id: UUID = Field(..., description="The vehicle being assigned to fulfil this load.")


class LoadAcceptResponse(BaseModel):
    match_id: UUID = Field(..., description="Identifier of the created load_matches record.")
    status: LoadStatus = Field(..., description="Load status after acceptance (typically 'accepted').")
