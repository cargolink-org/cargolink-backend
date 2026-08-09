"""
auth — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). OTP request/verify, JWT issue/verify/refresh.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - POST /auth/otp/request
  - POST /auth/otp/verify
  - POST /auth/refresh
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class Role(str, Enum):
    SHIPPER = "shipper"
    TRANSPORTER = "transporter"
    ADMIN = "admin"


class OtpRequestRequest(BaseModel):
    phone: str

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        if not value.startswith("+") or not value[1:].isdigit() or len(value) < 8:
            raise ValueError("phone must be a valid E.164 phone number")
        return value


class OtpVerifyRequest(BaseModel):
    phone: str
    otp: str

    @field_validator("otp")
    def validate_otp(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 6:
            raise ValueError("otp must be exactly 6 digits")
        return value


class UserSummary(BaseModel):
    id: UUID
    role: Role
    name: str
    phone: str
    email: Optional[str] = None
    created_at: datetime


class AuthPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class AuthPlaceholderResponse(BaseModel):
    """Placeholder response model — see AuthPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
