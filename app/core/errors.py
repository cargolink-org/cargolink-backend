"""
Unified error response pattern (Task A.1/A.2), reconstructed here as a
prerequisite for A.3 — see note in app/core/enums.py. A.3 does not extend
or change this file; it is included only so the domain router stubs
created alongside it (needed for main.py to boot) can reference it
consistently, matching the pattern already established across the 13
domain modules per project memory.
"""

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code.")
    message: str = Field(..., description="Human-readable error message.")


class ErrorResponse(BaseModel):
    error: ErrorDetail


ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Validation error"},
    401: {"model": ErrorResponse, "description": "Missing or invalid credentials"},
    403: {"model": ErrorResponse, "description": "Role/ownership check failed"},
    404: {"model": ErrorResponse, "description": "Resource not found"},
    409: {"model": ErrorResponse, "description": "Conflict with current state"},
    501: {"model": ErrorResponse, "description": "Not implemented yet"},
}
