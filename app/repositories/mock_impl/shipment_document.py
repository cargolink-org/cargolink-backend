"""InMemoryShipmentDocumentRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from app.core.enums import DocumentStatus, ShipmentDocType
from app.repositories.exceptions import NotFoundError
from app.repositories.models import ShipmentDocument

_Key = Tuple[str, ShipmentDocType]


class InMemoryShipmentDocumentRepository:
    def __init__(self) -> None:
        self._by_key: Dict[_Key, ShipmentDocument] = {}
        # No seed file — checklist rows are created per-load via F.1's
        # upload flow, not pre-existing fixture data.

    async def list_by_load(self, load_id: str) -> List[ShipmentDocument]:
        return [doc for (lid, _), doc in self._by_key.items() if lid == load_id]

    async def upsert(
        self, load_id: str, doc_type: ShipmentDocType, file_url: Optional[str], status: DocumentStatus
    ) -> ShipmentDocument:
        doc = ShipmentDocument(load_id=load_id, doc_type=doc_type, file_url=file_url, status=status)
        self._by_key[(load_id, doc_type)] = doc
        return doc

    async def update_status(
        self, load_id: str, doc_type: ShipmentDocType, status: DocumentStatus
    ) -> ShipmentDocument:
        key = (load_id, doc_type)
        doc = self._by_key.get(key)
        if doc is None:
            raise NotFoundError(
                f"No shipment document row for load_id={load_id!r}, doc_type={doc_type!r}"
            )
        doc.status = status
        return doc
