from fastapi import APIRouter, Depends

from core.rate_limiter import check_rate_limit
from services.question_service import (
    generate_part1_questions,
    generate_part2_question,
    generate_part3_questions,
)

router = APIRouter()


@router.get("/generate-part1")
async def generate_part1(username: str = Depends(check_rate_limit)):
    return generate_part1_questions()


@router.get("/generate-part2")
async def generate_part2(username: str = Depends(check_rate_limit)):
    return generate_part2_question()


@router.get("/generate-part3")
async def generate_part3(username: str = Depends(check_rate_limit)):
    return generate_part3_questions()
