"""Containers domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.containers.schemas import ContainerCreateRequest, ContainerResponse, ContainerUpdateRequest
from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/containers", tags=["containers"])


@router.post(
    "/{load_id}",
    response_model=ContainerResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Attach container tracking data to a load",
)
async def create_container(load_id: UUID, payload: ContainerCreateRequest) -> ContainerResponse:
    """Stub — real logic lands in Cluster F.3 (Sprint 5)."""
    raise NotImplementedError("Implemented in Task F.3 (Sprint 5)")


@router.get(
    "/{load_id}",
    response_model=ContainerResponse | None,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Read a load's container data (null for road-only loads)",
)
async def get_container(load_id: UUID) -> ContainerResponse | None:
    """Stub — real logic lands in Cluster F.3 (Sprint 5)."""
    raise NotImplementedError("Implemented in Task F.3 (Sprint 5)")


@router.patch(
    "/{container_id}",
    response_model=ContainerResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Update container tracking data",
)
async def update_container(container_id: UUID, payload: ContainerUpdateRequest) -> ContainerResponse:
    """Stub — real logic lands in Cluster F.3 (Sprint 5)."""
    raise NotImplementedError("Implemented in Task F.3 (Sprint 5)")
