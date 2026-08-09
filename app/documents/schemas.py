"""
documents — API request/response schemas (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py (this sandbox has no persisted state from prior
sessions). Per-shipment document checklist.

IMPORTANT: these are API-facing Pydantic models only. Task A.3's
repository layer (app/repositories/models.py) defines its OWN, separate
internal domain models and must never import from this module — see the
architectural rule in the A.3 task prompt.

Endpoints this file backs (technical spec Sec. 5 / this domain's slice):
  - GET /documents/{loadId}
  - POST /documents/{loadId}/upload
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class DocType(str, Enum):
    COMMERCIAL_INVOICE = "commercial_invoice"
    PACKING_LIST = "packing_list"
    BILL_OF_LADING = "bill_of_lading"
    AIRWAY_BILL = "airway_bill"
    CUSTOMS_CLEARANCE_CERTIFICATE = "customs_clearance_certificate"


class DocumentStatus(str, Enum):
    PENDING = "Pending"
    UPLOADED = "Uploaded"
    VERIFIED = "Verified"
    CLEARED = "Cleared"


class ShipmentDocumentItem(BaseModel):
    doc_type: DocType
    status: DocumentStatus
    file_url: Optional[str] = None


class DocumentsPlaceholderRequest(BaseModel):
    """Placeholder request model — narrowed into per-endpoint models as this
    domain's router logic (Clusters B-H) is implemented."""

    note: str = Field(
        default="stub",
        description="Placeholder field; replaced by real per-endpoint schemas "
        "as this domain's business logic is implemented.",
    )


class DocumentsPlaceholderResponse(BaseModel):
    """Placeholder response model — see DocumentsPlaceholderRequest."""

    note: str = Field(default="stub", description="Placeholder field.")
