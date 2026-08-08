"""Pricing engine read contract — GET /pricing/quote."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PricingQuoteResponse(BaseModel):
    base_fare: float = Field(..., ge=0, description="Flat base component of the fare.")
    distance_cost: float = Field(..., ge=0, description="distance_km × rate_per_km component.")
    surcharge: float = Field(..., ge=0, description="Sum of weight/type surcharges (e.g. hazardous, refrigerated).")
    total: float = Field(
        ..., ge=0, description="Total quoted fare (base_fare + distance_cost + surcharge, demand-adjusted)."
    )
