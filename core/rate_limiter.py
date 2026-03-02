import time
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import Depends, HTTPException, status

from core.config import RATE_LIMIT_MAX, RATE_LIMIT_WINDOW
from core.auth import get_current_user

# In-memory store: username -> deque of call timestamps
_call_log: Dict[str, Deque[float]] = defaultdict(deque)


def check_rate_limit(username: str = Depends(get_current_user)) -> str:
    """
    FastAPI dependency — sliding-window rate limiter.
    Raises HTTP 429 when the user exceeds RATE_LIMIT_MAX
    requests within RATE_LIMIT_WINDOW seconds.
    Returns the username so routes can use it downstream.
    """
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    calls = _call_log[username]

    # Evict timestamps outside the current window
    while calls and calls[0] < window_start:
        calls.popleft()

    if len(calls) >= RATE_LIMIT_MAX:
        retry_after = int(calls[0] - window_start) + 1
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Rate limit exceeded. Max {RATE_LIMIT_MAX} requests "
                f"per {RATE_LIMIT_WINDOW}s. Retry after {retry_after}s."
            ),
            headers={"Retry-After": str(retry_after)},
        )

    calls.append(now)
    return username
