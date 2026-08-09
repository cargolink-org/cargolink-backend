"""
checkpoints — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Checkpoint status timeline.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - POST /checkpoints/{loadId}
"""

from app.core.enums import CheckpointName, CheckpointStatus
from pydantic import BaseModel, Field


class CheckpointCreateRequest(BaseModel):
    checkpoint_name: CheckpointName
    status: CheckpointStatus


class CheckpointsPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class CheckpointsPlaceholderResponse(BaseModel):
    """Placeholder response model — see CheckpointsPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
