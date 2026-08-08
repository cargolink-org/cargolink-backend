"""Matching domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.errors import ERROR_RESPONSES
from app.matching.schemas import LoadMatchesResponse

router = APIRouter(prefix="/loads", tags=["matching"])


@router.get(
    "/{load_id}/matches",
    response_model=LoadMatchesResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Get candidate vehicle matches for a load",
)
async def get_load_matches(
    load_id: UUID,
    radius_km: float = Query(50, gt=0, le=500, description="Search radius around the load's pickup point, in km."),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of candidates to return."),
) -> LoadMatchesResponse:
    """Stub — real matching logic (Cluster C.2 onward) lands starting Sprint 3."""
    raise NotImplementedError("Implemented starting Task C.2 (Sprint 3)")
