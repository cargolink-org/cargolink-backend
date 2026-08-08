"""Tracking domain router — route registration only, per A.2 scope.

Only the REST history read (GET /tracking/{vehicleId}) is registered
here. The WS /socket.io `location:update` event is Task E.1's job.
"""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.errors import ERROR_RESPONSES
from app.tracking.schemas import TrackingHistoryResponse

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.get(
    "/{vehicle_id}",
    response_model=TrackingHistoryResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Get historical location pings for a vehicle",
)
async def get_tracking_history(
    vehicle_id: UUID,
    from_: datetime | None = Query(None, alias="from", description="Start of the time window (inclusive)."),
    to: datetime | None = Query(None, description="End of the time window (inclusive)."),
) -> TrackingHistoryResponse:
    """Stub — real read-path logic lands alongside Cluster E.1's write path (Sprint 4)."""
    raise NotImplementedError("Implemented in Task E.1 (Sprint 4)")
