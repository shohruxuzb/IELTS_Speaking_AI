from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.auth import create_access_token, get_current_user
from models.request_models import UserRegisterRequest, TokenResponse, UserInfo
from services.user_service import (
    register_user,
    authenticate_user,
    get_api_key,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegisterRequest):
    """Register a new user. Returns a JWT access token and API key."""
    api_key = register_user(req.username, req.password)
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )
    token = create_access_token(data={"sub": req.username})
    return TokenResponse(access_token=token, api_key=api_key)


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2-compatible login. Returns a JWT access token and API key."""
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": form_data.username})
    api_key = get_api_key(form_data.username)
    return TokenResponse(access_token=token, api_key=api_key)


@router.get("/me", response_model=UserInfo)
async def me(username: str = Depends(get_current_user)):
    """Return info about the currently authenticated user."""
    api_key = get_api_key(username)
    return UserInfo(username=username, api_key=api_key)
