"""
documents — FastAPI router stub (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py. Every route below is an intentional stub raising
HTTP 501 until this domain's business-logic cluster is implemented; Task
A.3 must NOT change this file (per its "DO NOT" list) beyond this initial
recreation.

Endpoints (technical spec Sec. 5): GET /documents/{loadId}, POST /documents/{loadId}/upload
"""

from fastapi import APIRouter, HTTPException

from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/_stub", responses=ERROR_RESPONSES)
async def documents_stub():
    """Placeholder route — replaced by real endpoints as this domain's
    business logic (see Dinesh-Backend-Implementation-Guide.md, Clusters
    B-H) is implemented."""
    raise HTTPException(status_code=501, detail={"error": {"code": "not_implemented", "message": "documents endpoints not implemented yet"}})
