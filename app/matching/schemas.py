"""Matching-engine read contract — GET /loads/{id}/matches.

See app/loads/schemas.py for the module-boundary decision between
`loads` (resource CRUD) and `matching` (the algorithm).
"""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class MatchCandidate(BaseModel):
    vehicle_id: UUID = Field(..., description="Candidate vehicle's id.")
    distance_km: float = Field(
        ...,
        ge=0,
        description="Road distance from vehicle to pickup point, in km (OSRM; falls back to Haversine if OSRM is degraded — Cluster C.1).",
    )
    capacity_fit: bool = Field(..., description="Whether the vehicle's capacity satisfies the load's weight/volume.")
    eta: int = Field(..., ge=0, description="Estimated time to pickup, in seconds.")
    score: float = Field(..., description="Composite match score (higher is better); see Clusters C.2/H.2 for scoring inputs.")


class LoadMatchesResponse(BaseModel):
    matches: list[MatchCandidate] = Field(
        ...,
        description="Candidate vehicles for this load, sorted by score descending. Empty list (not an error) when nothing qualifies.",
    )
