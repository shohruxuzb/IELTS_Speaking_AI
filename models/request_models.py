from pydantic import BaseModel
from typing import List, Dict, Optional


# ─── Auth request/response models ─────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    api_key: str


class UserInfo(BaseModel):
    username: str
    api_key: str


# ─── Evaluation / scoring models ──────────────────────────────────────────────

class EvaluationsRequest(BaseModel):
    """Request body for the /aggregate-results endpoint."""
    evaluations: List[Dict]