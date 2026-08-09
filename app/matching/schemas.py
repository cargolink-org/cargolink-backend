"""
matching — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Matching engine — OSRM filter, graph, Hungarian, ML stretch.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /loads/{id}/matches
"""

from __future__ import annotations

from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class MatchCandidate(BaseModel):
    vehicle_id: UUID
    distance_km: float
    capacity_fit: bool
    eta: int
    score: float


class LoadMatchesResponse(BaseModel):
    matches: List[MatchCandidate]


class MatchingPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class MatchingPlaceholderResponse(BaseModel):
    """Placeholder response model — see MatchingPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
