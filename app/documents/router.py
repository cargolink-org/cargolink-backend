"""Documents domain router — route registration only, per A.2 scope."""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, status

from app.core.errors import ERROR_RESPONSES
from app.documents.schemas import DocumentChecklistResponse, DocumentUploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get(
    "/{load_id}",
    response_model=DocumentChecklistResponse,
    status_code=status.HTTP_200_OK,
    responses=ERROR_RESPONSES,
    summary="Get the document checklist for a load",
)
async def get_documents(load_id: UUID) -> DocumentChecklistResponse:
    """Stub — real logic lands in Cluster F.1 (Sprint 5)."""
    raise NotImplementedError("Implemented in Task F.1 (Sprint 5)")


@router.post(
    "/{load_id}/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses=ERROR_RESPONSES,
    summary="Upload a shipment document (multipart)",
)
async def upload_document(load_id: UUID) -> DocumentUploadResponse:
    """Stub — real multipart handling + StorageClient wiring lands in B.2/F.1."""
    raise NotImplementedError("Implemented in Tasks B.2 and F.1")
