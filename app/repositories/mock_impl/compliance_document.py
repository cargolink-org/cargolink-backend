"""InMemoryComplianceDocumentRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, List

from app.core.enums import ComplianceDocType, DocumentStatus
from app.repositories.exceptions import NotFoundError
from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import ComplianceDocument, new_id


class InMemoryComplianceDocumentRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, ComplianceDocument] = {}
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("documents.json")
        if not records:
            return
        for row in records:
            try:
                doc = ComplianceDocument(
                    id=row.get("id") or new_id(),
                    owner_id=row["owner_id"],
                    doc_type=ComplianceDocType(row["doc_type"]),
                    file_url=row["file_url"],
                    status=DocumentStatus(row.get("status", DocumentStatus.PENDING.value)),
                )
            except (KeyError, ValueError):
                continue
            self._by_id[doc.id] = doc

    async def create(
        self, owner_id: str, doc_type: ComplianceDocType, file_url: str
    ) -> ComplianceDocument:
        doc = ComplianceDocument(id=new_id(), owner_id=owner_id, doc_type=doc_type, file_url=file_url)
        self._by_id[doc.id] = doc
        return doc

    async def list_by_owner(self, owner_id: str) -> List[ComplianceDocument]:
        return [d for d in self._by_id.values() if d.owner_id == owner_id]

    async def update_status(self, doc_id: str, status: DocumentStatus) -> ComplianceDocument:
        doc = self._by_id.get(doc_id)
        if doc is None:
            raise NotFoundError(f"No compliance document with id={doc_id!r}")
        doc.status = status
        return doc
