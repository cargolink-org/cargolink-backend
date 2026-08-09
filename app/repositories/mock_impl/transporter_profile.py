"""InMemoryTransporterProfileRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, Optional

from app.repositories.exceptions import NotFoundError
from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import TransporterProfile


class InMemoryTransporterProfileRepository:
    def __init__(self) -> None:
        self._by_user_id: Dict[str, TransporterProfile] = {}
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("transporter_profiles.json")
        if not records:
            return
        for row in records:
            try:
                profile = TransporterProfile(
                    user_id=row["user_id"],
                    license_no=row.get("license_no"),
                    rating_avg=float(row.get("rating_avg", 0.0)),
                )
            except KeyError:
                continue
            self._by_user_id[profile.user_id] = profile

    async def get_by_user_id(self, user_id: str) -> Optional[TransporterProfile]:
        return self._by_user_id.get(user_id)

    async def upsert(self, user_id: str, license_no: Optional[str]) -> TransporterProfile:
        existing = self._by_user_id.get(user_id)
        rating_avg = existing.rating_avg if existing else 0.0
        profile = TransporterProfile(user_id=user_id, license_no=license_no, rating_avg=rating_avg)
        self._by_user_id[user_id] = profile
        return profile

    async def update_rating_avg(self, user_id: str, new_avg: float) -> None:
        profile = self._by_user_id.get(user_id)
        if profile is None:
            raise NotFoundError(f"No transporter profile for user_id={user_id!r}")
        profile.rating_avg = new_avg
