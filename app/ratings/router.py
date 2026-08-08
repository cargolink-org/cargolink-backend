"""Ratings domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.ratings.schemas import RatingCreateRequest, RatingCreateResponse

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post(
    "",
    response_model=RatingCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Submit a post-trip rating",
)
async def create_rating(payload: RatingCreateRequest) -> RatingCreateResponse:
    """Stub — real logic (duplicate/ownership checks, rating_avg update) lands in Cluster H.2 (Sprint 6)."""
    raise NotImplementedError("Implemented in Task H.2 (Sprint 6)")
