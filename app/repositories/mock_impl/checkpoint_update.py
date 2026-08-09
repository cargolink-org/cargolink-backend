"""InMemoryCheckpointUpdateRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, List, Optional

from app.core.enums import CheckpointName, CheckpointStatus
from app.repositories.models import CheckpointUpdate, new_id


class InMemoryCheckpointUpdateRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, CheckpointUpdate] = {}
        # No seed file — checkpoint updates are a runtime audit trail, not
        # fixture data.

    async def create(
        self,
        load_id: str,
        checkpoint_name: CheckpointName,
        status: CheckpointStatus,
        posted_by: str,
        out_of_sequence: bool,
    ) -> CheckpointUpdate:
        update = CheckpointUpdate(
            id=new_id(),
            load_id=load_id,
            checkpoint_name=checkpoint_name,
            status=status,
            posted_by=posted_by,
            out_of_sequence=out_of_sequence,
        )
        self._by_id[update.id] = update
        return update

    async def list_by_load(self, load_id: str) -> List[CheckpointUpdate]:
        updates = [u for u in self._by_id.values() if u.load_id == load_id]
        return sorted(updates, key=lambda u: u.timestamp)

    async def get_last(self, load_id: str) -> Optional[CheckpointUpdate]:
        updates = await self.list_by_load(load_id)
        return updates[-1] if updates else None
