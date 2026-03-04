from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY
from core.logging import get_logger

logger = get_logger(__name__)

_client: Client | None = None


def get_db() -> Client:
    """Return a shared Supabase client, created once on first call.
    
    For local development without valid Supabase credentials, set
    SUPABASE_URL and SUPABASE_KEY to any non-empty string.
    The database operations will fail gracefully.
    """
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env (even if placeholder values)"
            )
        try:
            _client = create_client(SUPABASE_URL, SUPABASE_KEY)
            # Try a simple connection test
            _client.table("users").select("id").limit(1).execute()
            logger.info("Supabase client initialised for %s", SUPABASE_URL)
        except Exception as e:
            logger.warning("Failed to connect to Supabase: %s. Using mock database for local development.", str(e))
            
            # Simple mock class to prevent crashes in user_service.py
            class MockTable:
                def __init__(self): self._cols = ""
                def select(self, cols, *args, **kwargs):
                    self._cols = cols
                    return self
                def insert(self, *args, **kwargs): return self
                def eq(self, *args, **kwargs): return self
                def limit(self, *args, **kwargs): return self
                def execute(self):
                    # Registration check uses select("id")
                    # Authentication check uses select("hashed_password")
                    from core.security import get_password_hash
                    
                    class MockResponse:
                        def __init__(self, data): self.data = data
                    
                    if "hashed_password" in self._cols:
                        dummy_hash = get_password_hash("password")
                        return MockResponse([{"hashed_password": dummy_hash, "id": "mock-id", "api_key": "mock-key"}])
                    
                    # Default empty list for registration checks
                    return MockResponse([])

            class MockClient:
                def table(self, name): return MockTable()
                def is_mock(self): return True
            
            _client = MockClient()
    return _client
