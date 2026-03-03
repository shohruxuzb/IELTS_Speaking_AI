from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.logging import get_logger
from workers.tasks import get_job_result

router = APIRouter()
logger = get_logger(__name__)


@router.get("/jobs/{job_id}")
async def poll_job(job_id: str, username: str = Depends(get_current_user)):
    """
    Poll the result of a background evaluation job.

    Returns:
    - `{"status": "pending"}` — job is still processing
    - `{"status": "done", "result": {...}}` — job completed successfully
    - `{"status": "error", "detail": "..."}` — job failed
    - 404 — job_id unknown or expired
    """
    result = get_job_result(job_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found or expired.",
        )

    return result
