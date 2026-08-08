"""In-app notification contract — GET /notifications, PATCH /notifications/{id}/read.

Inference note: per Cluster G.1's own note ("a read-side API for
Frontend's inbox ... inferred, finalize in the OpenAPI contract"), routes
below are the smallest reasonable shape for a notification inbox scoped
to the calling user (identity from the JWT, not a path parameter).
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class NotificationType(str, Enum):
    BOOKING_CONFIRMATION = "booking_confirmation"
    PICKUP_CONFIRMATION = "pickup_confirmation"
    DELAY_ALERT = "delay_alert"
    DELIVERY_CONFIRMATION = "delivery_confirmation"


class NotificationResponse(BaseModel):
    id: UUID = Field(..., description="Unique notification identifier.")
    type: NotificationType = Field(..., description="Which lifecycle event triggered this notification.")
    message: str = Field(..., description="Human-readable notification text.")
    sent_at: datetime = Field(..., description="When this notification was created/sent.")
    read: bool = Field(False, description="Whether the recipient has marked this notification read.")


class NotificationListResponse(BaseModel):
    notifications: list[NotificationResponse] = Field(
        ..., description="The calling user's notifications, most recent first."
    )
