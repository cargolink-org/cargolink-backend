"""Auth domain contract — OTP request/verify, JWT issue/refresh.

Endpoints (technical spec §5, implementation guide Cluster B.1):
  POST /auth/otp/request   -> OtpRequestRequest  -> OtpRequestResponse
  POST /auth/otp/verify    -> OtpVerifyRequest    -> OtpVerifyResponse
  POST /auth/refresh       -> TokenRefreshRequest -> TokenRefreshResponse

Naming note: `OtpRequestRequest` looks unusual but is the parallel
construction to the guide's own example `OtpVerifyRequest` for
/auth/otp/verify — "action + Request" applied consistently to both
otp/request and otp/verify.

Never return password_hash or a raw OTP value in any response (A.2
requirement 7) — OtpVerifyResponse below intentionally has no otp field,
and UserSummary intentionally omits password_hash.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# E.164-ish phone pattern; permissive across countries but validates the
# India-format examples used throughout the source docs (+91XXXXXXXXXX).
PHONE_PATTERN = r"^\+[1-9]\d{6,14}$"
OTP_PATTERN = r"^\d{6}$"


class Role(str, Enum):
    SHIPPER = "shipper"
    TRANSPORTER = "transporter"
    ADMIN = "admin"


class UserSummary(BaseModel):
    """Minimal user projection returned alongside auth tokens.

    Deliberately excludes password_hash and any other internal-only field.
    """

    id: UUID = Field(..., description="Unique user identifier.")
    role: Role = Field(..., description="The user's platform role.")
    name: str | None = Field(None, description="Display name, if set during onboarding.")
    phone: str = Field(..., description="E.164 phone number used for OTP login.", pattern=PHONE_PATTERN)
    email: EmailStr | None = Field(None, description="Optional email address.")
    created_at: datetime = Field(..., description="When this user account was created.")


class OtpRequestRequest(BaseModel):
    phone: str = Field(
        ...,
        description="Phone number to send the OTP to, E.164 format (e.g. +919876543210).",
        pattern=PHONE_PATTERN,
        examples=["+919876543210"],
    )


class OtpRequestResponse(BaseModel):
    otp_sent: bool = Field(..., description="True if the OTP was dispatched (or queued) successfully.")


class OtpVerifyRequest(BaseModel):
    phone: str = Field(..., description="Phone number the OTP was requested for.", pattern=PHONE_PATTERN)
    otp: str = Field(..., description="The 6-digit one-time password received by SMS.", pattern=OTP_PATTERN)


class OtpVerifyResponse(BaseModel):
    token: str = Field(..., description="Short-lived JWT access token (~15 min).")
    refresh_token: str = Field(..., description="Longer-lived, rotating refresh token.")
    user: UserSummary = Field(..., description="The authenticated user (created on first verify, returned as-is otherwise).")


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="A previously issued, still-valid (unrotated) refresh token.")


class TokenRefreshResponse(BaseModel):
    token: str = Field(..., description="A newly issued short-lived JWT access token.")
