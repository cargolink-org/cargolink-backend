"""InMemoryLoadRepository (Task A.3)."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from app.core.enums import CargoType, LoadStatus
from app.repositories.exceptions import NotFoundError
from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import GeoPoint, Load, new_id


class InMemoryLoadRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, Load] = {}
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("loads.json")
        if not records:
            return
        for row in records:
            try:
                load = Load(
                    id=row.get("id") or new_id(),
                    shipper_id=row["shipper_id"],
                    weight=float(row["weight"]),
                    cargo_type=CargoType(row["cargo_type"]),
                    source=GeoPoint(**row["source"]),
                    destination=GeoPoint(**row["destination"]),
                    deadline=datetime.fromisoformat(row["deadline"]),
                    status=LoadStatus(row.get("status", LoadStatus.POSTED.value)),
                )
            except (KeyError, ValueError):
                continue
            self._by_id[load.id] = load

    async def create(
        self,
        shipper_id: str,
        weight: float,
        cargo_type: CargoType,
        source: GeoPoint,
        destination: GeoPoint,
        deadline: datetime,
    ) -> Load:
        load = Load(
            id=new_id(),
            shipper_id=shipper_id,
            weight=weight,
            cargo_type=cargo_type,
            source=source,
            destination=destination,
            deadline=deadline,
        )
        self._by_id[load.id] = load
        return load

    async def get_by_id(self, load_id: str) -> Optional[Load]:
        return self._by_id.get(load_id)

    async def get_owner_id(self, load_id: str) -> str:
        load = self._by_id.get(load_id)
        if load is None:
            raise NotFoundError(f"No load with id={load_id!r}")
        return load.shipper_id

    async def update_status(self, load_id: str, status: LoadStatus) -> None:
        load = self._by_id.get(load_id)
        if load is None:
            raise NotFoundError(f"No load with id={load_id!r}")
        load.status = status

    async def list_open(self) -> List[Load]:
        return [l for l in self._by_id.values() if l.status == LoadStatus.POSTED]
