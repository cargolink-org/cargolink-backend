"""Checkpoint status contract — POST /checkpoints/{loadId}.

Enum normalization note: the source documentation writes checkpoint
names in prose ("origin warehouse → port/border → customs hold →
cleared → destination"). We normalize these to snake_case enum values
below (e.g. "port/border" -> PORT_BORDER = "port_border") since raw
slashes/spaces are awkward as API enum values; the human-readable prose
form is preserved only in comments/docs.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class CheckpointName(str, Enum):
    ORIGIN_WAREHOUSE = "origin_warehouse"
    PORT_BORDER = "port_border"
    CUSTOMS_HOLD = "customs_hold"
    CLEARED = "cleared"
    DESTINATION = "destination"


class CheckpointStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class CheckpointCreateRequest(BaseModel):
    checkpoint_name: CheckpointName = Field(..., description="Which checkpoint in the journey this update is for.")
    status: CheckpointStatus = Field(..., description="Status of the load at this checkpoint.")


class CheckpointCreateResponse(BaseModel):
    checkpoint_id: UUID = Field(..., description="Identifier of the created checkpoint_updates record.")


class CheckpointResponse(BaseModel):
    """Read-side projection, for the implicit timeline read path noted in Cluster F.2."""

    checkpoint_id: UUID = Field(..., description="Identifier of this checkpoint update.")
    checkpoint_name: CheckpointName = Field(..., description="Which checkpoint this update is for.")
    status: CheckpointStatus = Field(..., description="Status recorded at this checkpoint.")
    timestamp: datetime = Field(..., description="When this checkpoint update was recorded.")
