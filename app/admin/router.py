"""Admin domain router — route registration only, per A.2 scope.

Real admin-role gating (Cluster A.4) is applied when the handler body is
implemented in Cluster H.1 — not modeled at the schema layer, but noted
here since this endpoint must never be reachable by shipper/transporter
roles once real.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.admin.schemas import AdminStatsOverviewResponse
from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/stats/overview",
    response_model=AdminStatsOverviewResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Get admin dashboard summary metrics (admin-only)",
)
async def get_admin_stats_overview() -> AdminStatsOverviewResponse:
    """Stub — real aggregation logic lands in Cluster H.1 (Sprint 6)."""
    raise NotImplementedError("Implemented in Task H.1 (Sprint 6)")
