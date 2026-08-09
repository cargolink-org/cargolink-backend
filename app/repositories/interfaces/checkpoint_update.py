"""CheckpointUpdateRepository interface (Task A.3)."""

from typing import List, Optional, Protocol

from app.core.enums import CheckpointName, CheckpointStatus
from app.repositories.models import CheckpointUpdate


class CheckpointUpdateRepository(Protocol):
    async def create(
        self,
        load_id: str,
        checkpoint_name: CheckpointName,
        status: CheckpointStatus,
        posted_by: str,
        out_of_sequence: bool,
    ) -> CheckpointUpdate:
        """Append a checkpoint status update to a load's timeline.
        posted_by is the audit-log field (security checklist: 'Audit log
        on checkpoint_updates... status changes'). out_of_sequence is
        computed by F.2's service layer (via get_last, below) and passed
        in here for the record — this repository does not decide
        sequencing policy itself, only persists the flag."""
        ...

    async def list_by_load(self, load_id: str) -> List[CheckpointUpdate]:
        """Full checkpoint timeline for a load, for the timeline UI."""
        ...

    async def get_last(self, load_id: str) -> Optional[CheckpointUpdate]:
        """Most recent checkpoint update for a load, or None if none
        posted yet. F.2's service layer uses this to detect out-of-order
        posts before calling create()."""
        ...
