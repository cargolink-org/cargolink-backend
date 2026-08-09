"""ShipmentDocumentRepository interface (Task A.3).

Real-implementation note for Kishor (mirrored in
shared/contracts/repository-interfaces.md): the natural key here is the
composite (load_id, doc_type) — every method below is keyed on that pair,
not a surrogate id, matching how F.1's checklist is always read/written
per-load-per-type.
"""

from typing import List, Protocol

from app.core.enums import DocumentStatus, ShipmentDocType
from app.repositories.models import ShipmentDocument


class ShipmentDocumentRepository(Protocol):
    async def list_by_load(self, load_id: str) -> List[ShipmentDocument]:
        """F.1's checklist read path: every shipment document row that
        exists for a load. Note this may be a subset of the cargo-type's
        *required* doc types (F.1's rules.py computes the full required
        checklist; this method only returns what's actually been
        created/uploaded so far)."""
        ...

    async def upsert(
        self,
        load_id: str,
        doc_type: ShipmentDocType,
        file_url: str,
        status: DocumentStatus,
    ) -> ShipmentDocument:
        """Create or update the checklist row for (load_id, doc_type),
        e.g. on upload."""
        ...

    async def update_status(
        self, load_id: str, doc_type: ShipmentDocType, status: DocumentStatus
    ) -> ShipmentDocument:
        """Transition a checklist item's status (Pending -> Uploaded ->
        Verified -> Cleared, or -> Rejected). Raises NotFoundError if no
        row exists yet for (load_id, doc_type)."""
        ...
