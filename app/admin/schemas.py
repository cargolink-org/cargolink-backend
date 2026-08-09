"""
admin — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Admin stats aggregation.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /admin/stats/overview
"""

from typing import List

from pydantic import BaseModel, Field, field_validator


class RouteStat(BaseModel):
    route: str
    shipment_count: int

    @field_validator("shipment_count")
    def shipment_count_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("shipment_count must be non-negative")
        return value


class AdminStatsOverviewResponse(BaseModel):
    active: int
    completed: int
    delayed: int
    revenue: int
    top_routes: List[RouteStat] = Field(default_factory=list)

    @field_validator("active", "completed", "delayed", "revenue")
    def non_negative_counts(cls, value: int) -> int:
        if value < 0:
            raise ValueError("counts must be non-negative")
        return value
