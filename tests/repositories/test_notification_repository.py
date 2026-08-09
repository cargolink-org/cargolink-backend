"""Tests for InMemoryNotificationRepository (Task A.3, requirement 11)."""

import pytest

from app.core.enums import NotificationType
from app.repositories.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


async def test_create_and_list_by_user(notification_repo):
    notification = await notification_repo.create(
        user_id="user-1", type=NotificationType.BOOKING_CONFIRMATION, message="Your load is booked."
    )

    notifications = await notification_repo.list_by_user("user-1")

    assert notifications == [notification]
    assert notification.read is False


async def test_list_by_user_only_returns_matching_user(notification_repo):
    await notification_repo.create(
        user_id="user-1", type=NotificationType.BOOKING_CONFIRMATION, message="msg-1"
    )
    await notification_repo.create(
        user_id="user-2", type=NotificationType.BOOKING_CONFIRMATION, message="msg-2"
    )

    notifications = await notification_repo.list_by_user("user-1")

    assert len(notifications) == 1
    assert notifications[0].user_id == "user-1"


async def test_mark_read(notification_repo):
    notification = await notification_repo.create(
        user_id="user-1", type=NotificationType.DELAY_ALERT, message="Running late."
    )

    updated = await notification_repo.mark_read(notification.id)

    assert updated.read is True


async def test_mark_read_raises_not_found(notification_repo):
    with pytest.raises(NotFoundError):
        await notification_repo.mark_read("no-such-id")


async def test_exists_for_event_false_when_none_created(notification_repo):
    exists = await notification_repo.exists_for_event(
        "user-1", NotificationType.PICKUP_CONFIRMATION, "load-1:pickup"
    )

    assert exists is False
