"""Ratings contract — POST /ratings."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class RatingCreateRequest(BaseModel):
    load_id: UUID = Field(..., description="The completed load this rating is for.")
    ratee_id: UUID = Field(
        ...,
        description="The counterparty being rated. Verified server-side against the load's actual participants, never trusted blindly (Cluster H.2).",
    )
    score: int = Field(..., ge=1, le=5, description="Star rating, 1 (worst) to 5 (best).")
    comment: str | None = Field(None, max_length=1000, description="Optional free-text comment.")


class RatingCreateResponse(BaseModel):
    rating_id: UUID = Field(..., description="Identifier of the created rating record.")
