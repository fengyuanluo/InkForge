"""HTTP protection for optional single-password authentication."""

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.password_auth import (
    extract_bearer_token,
    is_password_auth_enabled,
    verify_access_token,
)


PUBLIC_API_PATHS = {
    "/api/v1/auth/login",
    "/api/v1/auth/status",
    "/api/v1/runtime-config",
}
PUBLIC_API_PREFIXES = ("/api/v1/health",)
PROTECTED_PATH_PREFIXES = (
    "/api/v1",
    "/covers",
    "/character-images",
    "/agent-attachments",
    "/icons/model",
    "/docs",
    "/redoc",
    "/openapi.json",
)


class PasswordAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if not is_password_auth_enabled() or not _requires_authentication(request):
            return await call_next(request)

        token = extract_bearer_token(request.headers.get("Authorization"))
        if verify_access_token(token):
            return await call_next(request)

        return JSONResponse(
            {"detail": "Authentication required"},
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
        )


def _requires_authentication(request: Request) -> bool:
    if request.method == "OPTIONS":
        return False
    path = request.url.path.rstrip("/") or "/"
    if path in PUBLIC_API_PATHS:
        return False
    if any(_matches_prefix(path, prefix) for prefix in PUBLIC_API_PREFIXES):
        return False
    return any(_matches_prefix(path, prefix) for prefix in PROTECTED_PATH_PREFIXES)


def _matches_prefix(path: str, prefix: str) -> bool:
    return path == prefix or path.startswith(f"{prefix.rstrip('/')}/")
