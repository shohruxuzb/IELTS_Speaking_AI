import uuid
from typing import Dict, Optional

from core.security import get_password_hash, verify_password

# ─── In-memory user store ─────────────────────────────────────────────────────
# Schema: { username: { "hashed_password": str, "api_key": str } }
# Swap this dict for a real DB (SQLite, Postgres, etc.) in production.

_users: Dict[str, dict] = {}

# Reverse index: api_key -> username  (for fast API-key lookups)
_api_keys: Dict[str, str] = {}


def register_user(username: str, password: str) -> Optional[str]:
    """
    Register a new user.
    Returns the generated api_key on success, or None if username already exists.
    """
    if username in _users:
        return None

    api_key = str(uuid.uuid4())
    _users[username] = {
        "hashed_password": get_password_hash(password),
        "api_key": api_key,
    }
    _api_keys[api_key] = username
    return api_key


def authenticate_user(username: str, password: str) -> bool:
    """Return True if the username exists and password matches."""
    user = _users.get(username)
    if not user:
        return False
    return verify_password(password, user["hashed_password"])


def get_api_key(username: str) -> Optional[str]:
    """Return the API key for an existing user, or None."""
    user = _users.get(username)
    return user["api_key"] if user else None


def get_user_by_api_key(api_key: str) -> Optional[str]:
    """Return the username that owns this API key, or None."""
    return _api_keys.get(api_key)


def user_exists(username: str) -> bool:
    return username in _users
