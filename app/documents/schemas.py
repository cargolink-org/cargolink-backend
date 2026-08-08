"""Shipment document checklist contract.

GET /documents/{loadId}, POST /documents/{loadId}/upload.
"""
from __future__ import annotations

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class DocType(str, Enum):
    COMMERCIAL_INVOICE = "commercial_invoice"
    PACKING_LIST = "packing_list"
    BILL_OF_LADING_OR_AIRWAY_BILL = "bill_of_lading_or_airway_bill"
    CUSTOMS_CLEARANCE_CERTIFICATE = "customs_clearance_certificate"
    CERTIFICATE_OF_ORIGIN = "certificate_of_origin"


class DocumentStatus(str, Enum):
    PENDING = "Pending"
    UPLOADED = "Uploaded"
    VERIFIED = "Verified"
    CLEARED = "Cleared"
    # Note: Cluster F.1 describes an admin-rejection path ("status flips
    # back with a reason field"). That's business logic added in Cluster F;
    # this enum sticks to exactly the four states named in this task's
    # acceptance criteria so the frozen contract matches what was specified.
    # A Rejected state (plus a reason field on the item) is a likely
    # addition when F.1 is implemented — flagged here so it isn't a
    # surprise breaking change to this enum later.


class ShipmentDocumentItem(BaseModel):
    doc_type: DocType = Field(..., description="Which checklist item this is.")
    status: DocumentStatus = Field(..., description="Current status of this document.")
    file_url: str | None = Field(None, description="Short-lived signed URL to read the uploaded file, if any.")


class DocumentChecklistResponse(BaseModel):
    documents: list[ShipmentDocumentItem] = Field(
        ..., description="The cargo-type-conditional checklist for this load (see Cluster F.1's rules.py)."
    )


class DocumentUploadRequest(BaseModel):
    """Metadata accompanying a multipart document upload.

    The technical spec marks this endpoint `(multipart)`; the binary file
    part itself is handled via FastAPI's `UploadFile` in the real B.2/F.1
    handler, not modeled as a Pydantic field here. This schema documents
    the form-field metadata that travels alongside the file.
    """

    doc_type: DocType = Field(..., description="Which checklist item this upload satisfies.")


class DocumentUploadResponse(BaseModel):
    doc_id: UUID = Field(..., description="Identifier of the created/updated document record.")
    status: DocumentStatus = Field(..., description="Document status after upload (typically 'Uploaded').")
