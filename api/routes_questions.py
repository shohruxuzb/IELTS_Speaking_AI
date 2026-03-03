from fastapi import APIRouter, Depends

from core.rate_limiter import check_rate_limit
from core.cache import cache_get, cache_set, make_key
from core.config import CACHE_TTL_QUESTIONS
from core.logging import get_logger
from services.question_service import (
    generate_part1_questions,
    generate_part2_question,
    generate_part3_questions,
)

router = APIRouter()
logger = get_logger(__name__)

# Cache key constants
_KEY_PART1 = make_key("ielts", "q", "part1")
_KEY_PART2 = make_key("ielts", "q", "part2")
_KEY_PART3 = make_key("ielts", "q", "part3")


def _cached_or_generate(cache_key: str, generator_fn, ttl: int = CACHE_TTL_QUESTIONS) -> dict:
    """Check cache first; call AI only on miss, then cache the result."""
    cached = cache_get(cache_key)
    if cached is not None:
        logger.info("Question cache HIT: %s", cache_key)
        return cached

    logger.info("Question cache MISS: %s — calling AI", cache_key)
    result = generator_fn()

    if "error" not in result:
        cache_set(cache_key, result, ttl)

    return result


@router.get("/generate-part1")
async def generate_part1(username: str = Depends(check_rate_limit)):
    return _cached_or_generate(_KEY_PART1, generate_part1_questions)


@router.get("/generate-part2")
async def generate_part2(username: str = Depends(check_rate_limit)):
    return _cached_or_generate(_KEY_PART2, generate_part2_question)


@router.get("/generate-part3")
async def generate_part3(username: str = Depends(check_rate_limit)):
    return _cached_or_generate(_KEY_PART3, generate_part3_questions)
