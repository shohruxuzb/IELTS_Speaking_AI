from fastapi import APIRouter, Depends

from core.rate_limiter import check_rate_limit
from models.request_models import EvaluationsRequest
from services.scoring_service import aggregate_evaluations

router = APIRouter()


@router.post("/aggregate-results")
async def aggregate_results(
    req: EvaluationsRequest,
    username: str = Depends(check_rate_limit),
):
    """
    Takes a list of JSON evaluations for Part 1, Part 2, and Part 3
    and returns a weighted overall IELTS band report.
    """
    return aggregate_evaluations(req.evaluations)
