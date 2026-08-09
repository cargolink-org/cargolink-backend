"""InMemoryRatingRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, List, Optional

from app.repositories.exceptions import ConflictError
from app.repositories.models import Rating, new_id


class InMemoryRatingRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, Rating] = {}
        # No seed file — ratings are submitted post-trip at runtime, not
        # fixture data (large-volume *seed* data for load-testing the
        # Hungarian assignment, per Sprint 7, is Kishor's concern at the
        # database layer, not this mock).

    async def create(
        self, load_id: str, rater_id: str, ratee_id: str, score: int, comment: Optional[str]
    ) -> Rating:
        if await self.exists(load_id, rater_id, ratee_id):
            raise ConflictError(
                f"A rating already exists for load_id={load_id!r}, "
                f"rater_id={rater_id!r}, ratee_id={ratee_id!r}"
            )
        rating = Rating(
            id=new_id(), load_id=load_id, rater_id=rater_id, ratee_id=ratee_id, score=score, comment=comment
        )
        self._by_id[rating.id] = rating
        return rating

    async def exists(self, load_id: str, rater_id: str, ratee_id: str) -> bool:
        return any(
            r.load_id == load_id and r.rater_id == rater_id and r.ratee_id == ratee_id
            for r in self._by_id.values()
        )

    async def list_for_ratee(self, ratee_id: str) -> List[Rating]:
        return [r for r in self._by_id.values() if r.ratee_id == ratee_id]
