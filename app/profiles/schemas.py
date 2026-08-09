"""
profiles — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Shipper and transporter profile creation/edit.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /profiles/me
  - PUT /profiles/shipper
  - PUT /profiles/transporter
"""

from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ShipperProfileCreateRequest(BaseModel):
    company_name: str
    gstin: Optional[str] = None

    @field_validator("company_name")
    def company_name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("company_name is required")
        return value

    @field_validator("gstin")
    def validate_gstin(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not re.fullmatch(r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[Z]{1}[0-9A-Z]{1}", value):
            raise ValueError("gstin must be a valid 15-character GSTIN")
        return value


class TransporterProfileCreateRequest(BaseModel):
    license_no: str

    @field_validator("license_no")
    def license_no_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("license_no is required")
        return value


class ProfilesPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class ProfilesPlaceholderResponse(BaseModel):
    """Placeholder response model — see ProfilesPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
