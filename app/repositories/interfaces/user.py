"""UserRepository interface (Task A.3). Consumed by B.1 (OTP verify signup)
and A.4 (role-dependency 'user still exists' check)."""

from typing import Optional, Protocol

from app.core.enums import UserRole
from app.repositories.models import User


class UserRepository(Protocol):
    async def get_by_id(self, user_id: str) -> User:
        """Fetch a user by id. Raises NotFoundError if no such user exists."""
        ...

    async def get_by_phone(self, phone: str) -> Optional[User]:
        """Fetch a user by phone number. Returns None if not yet registered
        (B.1 uses this to distinguish first-verify signup from return login)."""
        ...

    async def create(self, phone: str, role: UserRole) -> User:
        """Create a user on first OTP verify (B.1). Raises ConflictError if
        a user already exists for this phone number."""
        ...

    async def exists(self, user_id: str) -> bool:
        """A.4 dependency check: does this user id still exist (e.g. hasn't
        been deactivated)? Used so an otherwise-valid JWT for a removed
        user fails auth rather than silently succeeding."""
        ...
