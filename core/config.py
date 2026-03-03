import os
from dotenv import load_dotenv

load_dotenv()

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-use-a-long-random-string")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Rate limiting
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "20"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))

# File upload validation
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_AUDIO_DURATION_SEC = int(os.getenv("MAX_AUDIO_DURATION_SEC", "180"))
ALLOWED_AUDIO_MIME_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/ogg",
    "audio/webm",
}

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Cache TTLs (seconds)
CACHE_TTL_QUESTIONS = int(os.getenv("CACHE_TTL_QUESTIONS", "3600"))    # 1 hour
CACHE_TTL_EVALUATIONS = int(os.getenv("CACHE_TTL_EVALUATIONS", "86400"))  # 24 hours
JOB_TTL = int(os.getenv("JOB_TTL", "3600"))  # 1 hour

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")