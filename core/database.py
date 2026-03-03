from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY
from core.logging import get_logger

logger = get_logger(__name__)

_client: Client | None = None


def get_db() -> Client:
    """Return a shared Supabase client, created once on first call."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env"
            )
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialised for %s", SUPABASE_URL)
    return _client
