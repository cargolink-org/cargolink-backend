"""Shipper & transporter profile contract.

Inference note (A.2 task instructions ask us to choose reasonable routes):
the technical spec does not enumerate profile routes explicitly. We choose
the smallest reasonable REST shape consistent with the schema tables in
cargolink-technical-specification.md §4 (`shipper_profiles`,
`transporter_profiles`):

    POST /shippers/profile       create/complete the caller's shipper profile
    GET  /shippers/profile       read the caller's own shipper profile
    POST /transporters/profile   create/complete the caller's transporter profile
    GET  /transporters/profile   read the caller's own transporter profile

Both POST routes are "my own profile" endpoints — the caller's identity
comes from the JWT (once B.1/A.4 exist), not a path parameter. This
matches the source doc's onboarding flow where a user completes their own
profile right after OTP signup, and avoids exposing an admin-style "any
user's profile by id" surface that was never asked for.
"""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

# Simplified GSTIN shape check (15 alphanumeric chars, standard format);
# not a full checksum validator — good enough to catch obviously malformed
# input at the contract layer.
GSTIN_PATTERN = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"


class ShipperProfileCreateRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200, description="Registered or trading company name.")
    gstin: str | None = Field(
        None,
        description="15-character GST Identification Number. Optional — not every shipper is GST-registered.",
        pattern=GSTIN_PATTERN,
        examples=["22AAAAA0000A1Z5"],
    )


class ShipperProfileResponse(BaseModel):
    user_id: UUID = Field(..., description="The shipper's user id.")
    company_name: str = Field(..., description="Registered or trading company name.")
    gstin: str | None = Field(None, description="15-character GST Identification Number, if provided.")


class TransporterProfileCreateRequest(BaseModel):
    license_no: str = Field(..., min_length=1, max_length=50, description="Driving/operator license number.")


class TransporterProfileResponse(BaseModel):
    user_id: UUID = Field(..., description="The transporter's user id.")
    license_no: str = Field(..., description="Driving/operator license number.")
    rating_avg: float = Field(
        0.0,
        ge=0,
        le=5,
        description="Rolling average rating (0-5), fed back from the ratings module (Cluster H.2).",
    )
