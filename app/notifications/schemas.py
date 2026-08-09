"""
notifications — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). In-app notification inbox.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /notifications
  - PATCH /notifications/{id}/read
"""

from enum import Enum

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    BOOKING_CONFIRMATION = "booking_confirmation"
    PICKUP_CONFIRMATION = "pickup_confirmation"
    DELAY_ALERT = "delay_alert"
    DELIVERY_CONFIRMATION = "delivery_confirmation"


class NotificationResponse(BaseModel):
    id: UUID
    type: NotificationType
    message: str
    read: bool = False
    sent_at: datetime


class NotificationsPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class NotificationsPlaceholderResponse(BaseModel):
    """Placeholder response model — see NotificationsPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
