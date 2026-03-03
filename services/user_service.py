import uuid
from typing import Optional

from core.database import get_db
from core.security import get_password_hash, verify_password
from core.logging import get_logger

logger = get_logger(__name__)


def register_user(username: str, password: str) -> Optional[str]:
    """
    Register a new user in Supabase.
    Returns the generated api_key on success, or None if username already taken.
    """
    db = get_db()

    # Check for existing username
    existing = db.table("users").select("id").eq("username", username).execute()
    if existing.data:
        return None

    api_key = str(uuid.uuid4())
    hashed = get_password_hash(password)

    try:
        db.table("users").insert({
            "username": username,
            "hashed_password": hashed,
            "api_key": api_key,
            "plan": "free",
        }).execute()
        return api_key
    except Exception as e:
        logger.error("register_user failed for '%s': %s", username, e, exc_info=True)
        return None


def authenticate_user(username: str, password: str) -> bool:
    """Return True if the username exists and password matches."""
    try:
        db = get_db()
        result = db.table("users").select("hashed_password").eq("username", username).execute()
        if not result.data:
            return False
        return verify_password(password, result.data[0]["hashed_password"])
    except Exception as e:
        logger.error("authenticate_user failed for '%s': %s", username, e, exc_info=True)
        return False


def get_api_key(username: str) -> Optional[str]:
    """Return the API key for an existing user, or None."""
    try:
        db = get_db()
        result = db.table("users").select("api_key").eq("username", username).execute()
        return result.data[0]["api_key"] if result.data else None
    except Exception as e:
        logger.error("get_api_key failed for '%s': %s", username, e, exc_info=True)
        return None


def get_user_by_api_key(api_key: str) -> Optional[str]:
    """Return the username that owns this API key, or None."""
    try:
        db = get_db()
        result = db.table("users").select("username").eq("api_key", api_key).execute()
        return result.data[0]["username"] if result.data else None
    except Exception as e:
        logger.error("get_user_by_api_key failed: %s", e, exc_info=True)
        return None


def get_user_id(username: str) -> Optional[str]:
    """Return the UUID of a user."""
    try:
        db = get_db()
        result = db.table("users").select("id").eq("username", username).execute()
        return result.data[0]["id"] if result.data else None
    except Exception as e:
        logger.error("get_user_id failed for '%s': %s", username, e, exc_info=True)
        return None


def user_exists(username: str) -> bool:
    try:
        db = get_db()
        result = db.table("users").select("id").eq("username", username).execute()
        return bool(result.data)
    except Exception:
        return False
