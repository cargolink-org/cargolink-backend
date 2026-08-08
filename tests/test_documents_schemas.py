from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.documents.schemas import DocType, DocumentStatus, ShipmentDocumentItem


def test_all_five_doc_types_are_valid():
    assert len(list(DocType)) == 5
    for doc_type in DocType:
        ShipmentDocumentItem(doc_type=doc_type, status=DocumentStatus.PENDING, file_url=None)


def test_document_status_restricted_to_four_defined_states():
    assert {s.value for s in DocumentStatus} == {"Pending", "Uploaded", "Verified", "Cleared"}


def test_shipment_document_item_rejects_unknown_status():
    with pytest.raises(ValidationError):
        ShipmentDocumentItem(doc_type=DocType.COMMERCIAL_INVOICE, status="Rejected", file_url=None)
