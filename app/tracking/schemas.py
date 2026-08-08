"""Tracking history contract — GET /tracking/{vehicleId}.

Note for Cluster E.1: the WS `location:update` event payload is NOT
modeled here as a formal Pydantic schema, per the A.2 task instructions
(E.1 owns that). For reference, the payload shape already confirmed in
the technical spec (§2.4) is:

    { "load_id": <uuid>, "vehicle_id": <uuid>, "lat": <float>, "lng": <float>, "ts": <iso8601> }

E.1 should reuse `LocationPoint` below (or a structurally identical
shape) for consistency between the REST history read and the socket
broadcast.
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class LocationPoint(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees (WGS84).")
    lng: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees (WGS84).")
    timestamp: datetime = Field(..., description="When this location was recorded.")


class TrackingHistoryResponse(BaseModel):
    points: list[LocationPoint] = Field(
        ..., description="Location pings for the vehicle within the requested window, chronological order."
    )
