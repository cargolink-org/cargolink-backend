"""InMemoryNotificationRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, List

from app.core.enums import NotificationType
from app.repositories.exceptions import NotFoundError
from app.repositories.models import Notification, new_id


class InMemoryNotificationRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, Notification] = {}
        # No seed file — notifications are generated at runtime by G.1's
        # triggers, not fixture data.

    async def create(self, user_id: str, type: NotificationType, message: str) -> Notification:
        notification = Notification(id=new_id(), user_id=user_id, type=type, message=message)
        self._by_id[notification.id] = notification
        return notification

    async def list_by_user(self, user_id: str) -> List[Notification]:
        return [n for n in self._by_id.values() if n.user_id == user_id]

    async def mark_read(self, notification_id: str) -> Notification:
        notification = self._by_id.get(notification_id)
        if notification is None:
            raise NotFoundError(f"No notification with id={notification_id!r}")
        notification.read = True
        return notification

    async def exists_for_event(
        self, user_id: str, type: NotificationType, dedupe_key: str
    ) -> bool:
        return any(
            n.user_id == user_id and n.type == type and n.dedupe_key == dedupe_key
            for n in self._by_id.values()
        )

    # NOTE (interface gap surfaced while implementing this mock, not fixed
    # here since A.3 must not change interface signatures beyond what the
    # task specifies): create() as specified takes no dedupe_key
    # parameter, so every Notification created via create() has
    # dedupe_key=None and exists_for_event() will only ever match other
    # None-dedupe_key records for a (user_id, type) pair — it cannot yet
    # deduplicate on a real per-event key (e.g. a specific load_id +
    # lifecycle-event combination) as G.1's docstring describes. G.1's
    # implementer will need either an interface amendment (add
    # dedupe_key to create()) or a documented workaround (e.g. embedding
    # the key in `message` and parsing it back out, which is not
    # recommended). Flagged in shared/contracts/repository-interfaces.md.
