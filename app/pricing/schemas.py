"""
pricing — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Rule-based (then regression) fare quoting.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /pricing/quote
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator


class PricingQuoteResponse(BaseModel):
    base_fare: float
    distance_cost: float
    surcharge: float
    total: float

    @field_validator("base_fare", "distance_cost", "surcharge")
    def non_negative_components(cls, value: float) -> float:
        if value < 0:
            raise ValueError("fare components must be non-negative")
        return value

    @model_validator(mode="after")
    def total_must_match_components(cls, values):
        if values.total != values.base_fare + values.distance_cost + values.surcharge:
            raise ValueError("total must equal base_fare + distance_cost + surcharge")
        return values


class PricingPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class PricingPlaceholderResponse(BaseModel):
    """Placeholder response model — see PricingPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
