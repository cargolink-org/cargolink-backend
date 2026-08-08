"""Notifications domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.notifications.schemas import NotificationListResponse, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get(
    "",
    response_model=NotificationListResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="List the calling user's notifications",
)
async def list_notifications() -> NotificationListResponse:
    """Stub — real logic lands in Cluster G.1 (Sprint 6)."""
    raise NotImplementedError("Implemented in Task G.1 (Sprint 6)")


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Mark a notification as read",
)
async def mark_notification_read(notification_id: UUID) -> NotificationResponse:
    """Stub — real logic lands in Cluster G.1 (Sprint 6)."""
    raise NotImplementedError("Implemented in Task G.1 (Sprint 6)")
