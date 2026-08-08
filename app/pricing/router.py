"""Pricing domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status

from app.core.errors import ERROR_RESPONSES
from app.pricing.schemas import PricingQuoteResponse

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.get(
    "/quote",
    response_model=PricingQuoteResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Get a fare quote for a load",
)
async def get_pricing_quote(
    load_id: UUID = Query(..., description="The load to quote a fare for."),
) -> PricingQuoteResponse:
    """Stub — real pricing logic (Cluster D.1) lands in Sprint 3."""
    raise NotImplementedError("Implemented in Task D.1 (Sprint 3)")
