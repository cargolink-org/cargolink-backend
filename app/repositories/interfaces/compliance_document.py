"""ComplianceDocumentRepository interface (Task A.3).

Table: `documents` — user- or vehicle-level verification documents
(driving_license implies a user owner; RC/permit/insurance imply a
vehicle owner, per ComplianceDocType). Owner-type inference flagged for
Kishor's schema review in shared/contracts/repository-interfaces.md.
"""

from typing import List, Protocol

from app.core.enums import ComplianceDocType, DocumentStatus
from app.repositories.models import ComplianceDocument


class ComplianceDocumentRepository(Protocol):
    async def create(
        self, owner_id: str, doc_type: ComplianceDocType, file_url: str
    ) -> ComplianceDocument:
        """Register a newly uploaded compliance document, status PENDING."""
        ...

    async def list_by_owner(self, owner_id: str) -> List[ComplianceDocument]:
        """List every compliance document for a given owner (user or
        vehicle id, per the doc_type's implied owner-type)."""
        ...

    async def update_status(
        self, doc_id: str, status: DocumentStatus
    ) -> ComplianceDocument:
        """Transition a document's verification status (admin review
        queue, per source documentation §4.1). Raises NotFoundError if
        doc_id doesn't exist."""
        ...
