"""NotificationRepository interface (Task A.3)."""

from typing import List, Optional, Protocol

from app.core.enums import NotificationType
from app.repositories.models import Notification


class NotificationRepository(Protocol):
    async def create(
        self, user_id: str, type: NotificationType, message: str
    ) -> Notification:
        """Persist an in-app notification record (G.1 trigger write
        path). SMS/email delivery is orchestrated by G.1's service layer,
        not this repository — this only handles the in-app record.

        NOTE: as specified, this method does not accept a dedupe_key, so
        records it creates have dedupe_key=None. See exists_for_event()
        below and the mock implementation's inline note for the resulting
        gap — G.1's implementer will likely need an interface amendment
        here."""
        ...

    async def list_by_user(self, user_id: str) -> List[Notification]:
        """Frontend inbox read path (GET /notifications)."""
        ...

    async def mark_read(self, notification_id: str) -> Notification:
        """PATCH /notifications/{id}/read. Raises NotFoundError for an
        unknown notification_id."""
        ...

    async def exists_for_event(
        self, user_id: str, type: NotificationType, dedupe_key: str
    ) -> bool:
        """G.1 idempotency check: has a notification of this type already
        been created for this user with this dedupe_key (e.g. a specific
        load_id + lifecycle-event combination)? Prevents duplicate trigger
        firing (e.g. five 'booking confirmed' sends) if an upstream event
        is re-processed."""
        ...
