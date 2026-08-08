"""Loads domain router — route registration only, per A.2 scope.

Owns POST /loads and POST /loads/{id}/accept. GET /loads/{id}/matches
lives in app/matching/router.py — see loads/schemas.py for the
module-boundary rationale.
"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.loads.schemas import LoadAcceptRequest, LoadAcceptResponse, LoadCreateRequest, LoadCreateResponse

router = APIRouter(prefix="/loads", tags=["loads"])


@router.post(
    "",
    response_model=LoadCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Post a new cargo load",
)
async def create_load(payload: LoadCreateRequest) -> LoadCreateResponse:
    """Stub — real logic lands alongside Cluster C's matching work (Sprint 3)."""
    raise NotImplementedError("Implemented in Sprint 3")


@router.post(
    "/{load_id}/accept",
    response_model=LoadAcceptResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Transporter accepts a matched load",
)
async def accept_load(load_id: UUID, payload: LoadAcceptRequest) -> LoadAcceptResponse:
    """Stub — real logic lands in Sprint 4 alongside Cluster E's tracking work."""
    raise NotImplementedError("Implemented in Sprint 4")
