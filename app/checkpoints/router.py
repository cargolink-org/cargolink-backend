"""Checkpoints domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.checkpoints.schemas import CheckpointCreateRequest, CheckpointCreateResponse
from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/checkpoints", tags=["checkpoints"])


@router.post(
    "/{load_id}",
    response_model=CheckpointCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Post a checkpoint status update for a load",
)
async def create_checkpoint(load_id: UUID, payload: CheckpointCreateRequest) -> CheckpointCreateResponse:
    """Stub — real logic + audit log lands in Cluster F.2 (Sprint 5)."""
    raise NotImplementedError("Implemented in Task F.2 (Sprint 5)")
