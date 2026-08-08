"""Vehicles domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.vehicles.schemas import VehicleCreateRequest, VehicleListResponse, VehicleResponse

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Register a vehicle owned by the calling transporter",
)
async def create_vehicle(payload: VehicleCreateRequest) -> VehicleResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Read a single vehicle",
)
async def get_vehicle(vehicle_id: UUID) -> VehicleResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")


@router.get(
    "",
    response_model=VehicleListResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="List the calling transporter's own vehicles",
)
async def list_vehicles() -> VehicleListResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")
