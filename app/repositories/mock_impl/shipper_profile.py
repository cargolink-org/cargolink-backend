"""InMemoryShipperProfileRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, Optional

from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import ShipperProfile


class InMemoryShipperProfileRepository:
    def __init__(self) -> None:
        self._by_user_id: Dict[str, ShipperProfile] = {}
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("shipper_profiles.json")
        if not records:
            return
        for row in records:
            try:
                profile = ShipperProfile(
                    user_id=row["user_id"],
                    company_name=row.get("company_name"),
                    gstin=row.get("gstin"),
                )
            except KeyError:
                continue
            self._by_user_id[profile.user_id] = profile

    async def get_by_user_id(self, user_id: str) -> Optional[ShipperProfile]:
        return self._by_user_id.get(user_id)

    async def upsert(
        self, user_id: str, company_name: Optional[str], gstin: Optional[str]
    ) -> ShipperProfile:
        profile = ShipperProfile(user_id=user_id, company_name=company_name, gstin=gstin)
        self._by_user_id[user_id] = profile
        return profile
