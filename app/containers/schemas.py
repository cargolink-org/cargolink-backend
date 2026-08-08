"""Container tracking contract.

Inference note: not enumerated in the technical spec at all. Routes below
are inferred as CRUD-style operations consistent with the `containers`
table (technical spec §4: container_no, vessel_or_flight,
port_of_loading, port_of_discharge), scoped to a load since containers
are always load-scoped in the schema (`load_id UUID REFERENCES
loads(id)`):

    POST  /containers/{loadId}       attach container data to a load
    GET   /containers/{loadId}       read a load's container data (null/empty if road-only, per Cluster F.3)
    PATCH /containers/{containerId}  update container data
"""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

# ISO 6346 container number: 4 letters (owner code + category id) + 7 digits.
CONTAINER_NO_PATTERN = r"^[A-Z]{4}\d{7}$"


class ContainerCreateRequest(BaseModel):
    container_no: str = Field(
        ..., pattern=CONTAINER_NO_PATTERN, description="ISO 6346 container number, e.g. MSCU1234567."
    )
    vessel_or_flight: str = Field(
        ..., min_length=1, max_length=100, description="Vessel name or flight number carrying this container."
    )
    port_of_loading: str = Field(
        ..., min_length=1, max_length=100, description="Port/airport where the container was loaded."
    )
    port_of_discharge: str = Field(
        ..., min_length=1, max_length=100, description="Port/airport where the container will be discharged."
    )


class ContainerUpdateRequest(BaseModel):
    container_no: str | None = Field(None, pattern=CONTAINER_NO_PATTERN, description="ISO 6346 container number.")
    vessel_or_flight: str | None = Field(None, max_length=100, description="Vessel name or flight number.")
    port_of_loading: str | None = Field(None, max_length=100, description="Port/airport where the container was loaded.")
    port_of_discharge: str | None = Field(
        None, max_length=100, description="Port/airport where the container will be discharged."
    )


class ContainerResponse(BaseModel):
    id: UUID = Field(..., description="Unique container record identifier.")
    load_id: UUID = Field(..., description="The load this container data belongs to.")
    container_no: str = Field(..., description="ISO 6346 container number.")
    vessel_or_flight: str = Field(..., description="Vessel name or flight number.")
    port_of_loading: str = Field(..., description="Port/airport where the container was loaded.")
    port_of_discharge: str = Field(..., description="Port/airport where the container will be discharged.")
