"""
containers — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Sea/air container tracking.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /containers/{loadId}
  - PUT /containers/{loadId}
"""

from typing import Optional
import re

from pydantic import BaseModel, Field, field_validator


class ContainerCreateRequest(BaseModel):
    container_no: str
    vessel_or_flight: str
    port_of_loading: str
    port_of_discharge: str

    @field_validator("container_no")
    def validate_container_no(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Z]{4}\d{7}", value):
            raise ValueError("container_no must be a valid ISO 6346 container number")
        return value


class ContainerUpdateRequest(BaseModel):
    container_no: Optional[str] = None
    vessel_or_flight: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None

    @field_validator("container_no")
    def validate_container_no(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not re.fullmatch(r"[A-Z]{4}\d{7}", value):
            raise ValueError("container_no must be a valid ISO 6346 container number")
        return value


class ContainersPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class ContainersPlaceholderResponse(BaseModel):
    """Placeholder response model — see ContainersPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
