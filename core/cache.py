import hashlib
import json
from typing import Any, Optional

import redis

from core.config import REDIS_URL
from core.logging import get_logger

logger = get_logger(__name__)

# ── Lazy singleton ────────────────────────────────────────────────────────────
_client: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    """Return a shared Redis client, creating it once."""
    global _client
    if _client is None:
        _client = redis.from_url(REDIS_URL, decode_responses=True)
    return _client


# ── Key builder ───────────────────────────────────────────────────────────────

def make_key(*parts: str) -> str:
    """Build a deterministic, namespaced cache key."""
    raw = ":".join(str(p) for p in parts)
    return raw


def make_hash_key(*parts: Any) -> str:
    """SHA-256 hash of serialised parts — used for long/variable data."""
    payload = json.dumps(parts, sort_keys=True)
    digest = hashlib.sha256(payload.encode()).hexdigest()[:24]
    return digest


# ── Get / Set ─────────────────────────────────────────────────────────────────

def cache_get(key: str) -> Optional[Any]:
    """
    Retrieve a JSON-deserialised value from Redis.
    Returns None on miss or on any Redis error.
    """
    try:
        raw = get_redis().get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.warning("Redis cache_get error for key '%s': %s", key, exc)
        return None


def cache_set(key: str, value: Any, ttl: int) -> None:
    """
    Serialise value as JSON and store it in Redis with a TTL.
    Silently swallows errors so a Redis failure never breaks the API.
    """
    try:
        get_redis().setex(key, ttl, json.dumps(value))
    except Exception as exc:
        logger.warning("Redis cache_set error for key '%s': %s", key, exc)


def cache_delete(key: str) -> None:
    """Delete a key — used for manual cache busting."""
    try:
        get_redis().delete(key)
    except Exception as exc:
        logger.warning("Redis cache_delete error for key '%s': %s", key, exc)


def is_redis_available() -> bool:
    """Ping Redis — useful for a health-check endpoint."""
    try:
        return get_redis().ping()
    except Exception:
        return False
