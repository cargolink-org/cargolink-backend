"""Auth domain router — route registration only, per A.2 scope.

Handler bodies are stubs; real OTP/JWT logic is Task B.1. This module's
only job right now is to make sure FastAPI's OpenAPI generation reflects
these three endpoints with their exact request/response schemas.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.auth.schemas import (
    OtpRequestRequest,
    OtpRequestResponse,
    OtpVerifyRequest,
    OtpVerifyResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
)
from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/otp/request",
    response_model=OtpRequestResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Request an OTP for a phone number",
)
async def request_otp(payload: OtpRequestRequest) -> OtpRequestResponse:
    """Stub — real logic (rate limiting, SMS dispatch) lands in Task B.1."""
    raise NotImplementedError("Implemented in Task B.1")


@router.post(
    "/otp/verify",
    response_model=OtpVerifyResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Verify an OTP and receive a token pair",
)
async def verify_otp(payload: OtpVerifyRequest) -> OtpVerifyResponse:
    """Stub — real logic lands in Task B.1."""
    raise NotImplementedError("Implemented in Task B.1")


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Exchange a refresh token for a new access token",
)
async def refresh_token(payload: TokenRefreshRequest) -> TokenRefreshResponse:
    """Stub — real logic lands in Task B.1."""
    raise NotImplementedError("Implemented in Task B.1")
