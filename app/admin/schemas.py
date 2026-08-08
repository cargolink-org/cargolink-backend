"""Admin analytics contract — GET /admin/stats/overview."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RouteStat(BaseModel):
    route: str = Field(..., description="Corridor label, e.g. 'Mumbai -> Delhi'.")
    shipment_count: int = Field(..., ge=0, description="Number of shipments on this route in the reporting window.")


class AdminStatsOverviewResponse(BaseModel):
    active: int = Field(..., ge=0, description="Count of currently active (in-progress) shipments.")
    completed: int = Field(..., ge=0, description="Count of completed shipments.")
    delayed: int = Field(..., ge=0, description="Count of shipments currently flagged delayed.")
    revenue: float = Field(..., ge=0, description="Gross revenue for the reporting window.")
    top_routes: list[RouteStat] = Field(..., description="Most popular corridors, ranked by shipment count.")
