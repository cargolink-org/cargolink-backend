"""Profiles domain router — route registration only, per A.2 scope.

Handler bodies are stubs; real onboarding logic is scoped for Sprint 2
alongside the rest of the profiles/vehicles/documents/loads work.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.profiles.schemas import (
    ShipperProfileCreateRequest,
    ShipperProfileResponse,
    TransporterProfileCreateRequest,
    TransporterProfileResponse,
)

router = APIRouter(tags=["profiles"])


@router.post(
    "/shippers/profile",
    response_model=ShipperProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Create/complete the calling shipper's profile",
)
async def create_shipper_profile(payload: ShipperProfileCreateRequest) -> ShipperProfileResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")


@router.get(
    "/shippers/profile",
    response_model=ShipperProfileResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Read the calling shipper's own profile",
)
async def get_shipper_profile() -> ShipperProfileResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")


@router.post(
    "/transporters/profile",
    response_model=TransporterProfileResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Create/complete the calling transporter's profile",
)
async def create_transporter_profile(payload: TransporterProfileCreateRequest) -> TransporterProfileResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")


@router.get(
    "/transporters/profile",
    response_model=TransporterProfileResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Read the calling transporter's own profile",
)
async def get_transporter_profile() -> TransporterProfileResponse:
    """Stub — real logic lands with the rest of Sprint 2's onboarding work."""
    raise NotImplementedError("Implemented in Sprint 2")
