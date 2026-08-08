from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.notifications.schemas import NotificationResponse, NotificationType


def test_notification_type_matches_the_four_named_lifecycle_events():
    assert {t.value for t in NotificationType} == {
        "booking_confirmation",
        "pickup_confirmation",
        "delay_alert",
        "delivery_confirmation",
    }


def test_notification_response_defaults_read_to_false():
    notif = NotificationResponse(
        id=uuid4(),
        type=NotificationType.BOOKING_CONFIRMATION,
        message="Your load has been booked.",
        sent_at=datetime.now(timezone.utc),
    )
    assert notif.read is False
