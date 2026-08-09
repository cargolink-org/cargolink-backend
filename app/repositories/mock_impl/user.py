"""InMemoryUserRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, Optional

from app.core.enums import UserRole
from app.repositories.exceptions import ConflictError, NotFoundError
from app.repositories.mock_impl._seed import load_seed_json
from app.repositories.models import User, new_id


class InMemoryUserRepository:
    """Instance-scoped in-memory store (never a module-level global — see
    A.3 requirement 3), so each test / each DI-container lifetime gets an
    isolated dataset."""

    def __init__(self) -> None:
        self._by_id: Dict[str, User] = {}
        self._phone_index: Dict[str, str] = {}  # phone -> user_id
        self._seed()

    def _seed(self) -> None:
        records = load_seed_json("users.json")
        if not records:
            return
        for row in records:
            try:
                user = User(
                    id=row.get("id") or new_id(),
                    role=UserRole(row["role"]),
                    phone=row["phone"],
                    name=row.get("name"),
                    email=row.get("email"),
                    password_hash=row.get("password_hash"),
                )
            except (KeyError, ValueError):
                continue  # malformed seed row — skip rather than crash startup
            self._by_id[user.id] = user
            self._phone_index[user.phone] = user.id

    async def get_by_id(self, user_id: str) -> User:
        user = self._by_id.get(user_id)
        if user is None:
            raise NotFoundError(f"No user with id={user_id!r}")
        return user

    async def get_by_phone(self, phone: str) -> Optional[User]:
        user_id = self._phone_index.get(phone)
        return self._by_id.get(user_id) if user_id else None

    async def create(self, phone: str, role: UserRole) -> User:
        if phone in self._phone_index:
            raise ConflictError(f"A user already exists for phone={phone!r}")
        user = User(id=new_id(), role=role, phone=phone)
        self._by_id[user.id] = user
        self._phone_index[phone] = user.id
        return user

    async def exists(self, user_id: str) -> bool:
        return user_id in self._by_id
