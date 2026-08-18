"""Single-password authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel

from app.password_auth import (
    extract_bearer_token,
    is_password_auth_enabled,
    issue_access_token,
    password_matches,
    verify_access_token,
)


router = APIRouter(prefix="/auth", tags=["auth"])


class AuthStatusResponse(BaseModel):
    enabled: bool
    authenticated: bool


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.get("/status", response_model=AuthStatusResponse)
async def get_auth_status(
    authorization: Annotated[str | None, Header()] = None,
) -> AuthStatusResponse:
    enabled = is_password_auth_enabled()
    token = extract_bearer_token(authorization)
    return AuthStatusResponse(
        enabled=enabled,
        authenticated=not enabled or verify_access_token(token),
    )


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    if not is_password_auth_enabled():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not password_matches(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return LoginResponse(access_token=issue_access_token())
