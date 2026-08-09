"""
ratings — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Post-trip ratings.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - POST /ratings
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class RatingCreateRequest(BaseModel):
    load_id: UUID
    ratee_id: UUID
    score: int
    comment: Optional[str] = None

    @field_validator("score")
    def validate_score(cls, value: int) -> int:
        if value < 1 or value > 5:
            raise ValueError("score must be between 1 and 5")
        return value


class RatingsPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class RatingsPlaceholderResponse(BaseModel):
    """Placeholder response model — see RatingsPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
