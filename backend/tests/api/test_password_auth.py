from pathlib import Path

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
import pytest
from fastapi.staticfiles import StaticFiles

from app.api.middleware.password_auth import PasswordAuthMiddleware
from app.api.routers import password_auth
from app.password_auth import issue_access_token
from app.settings import settings
from app.socket.handlers import register_handlers


def _create_app(files_dir: Path) -> FastAPI:
    app = FastAPI()
    app.add_middleware(PasswordAuthMiddleware)
    app.include_router(password_auth.router, prefix="/api/v1")

    @app.get("/api/v1/private")
    async def private_route() -> dict[str, bool]:
        return {"ok": True}

    app.mount("/covers", StaticFiles(directory=files_dir), name="covers")
    return app


@pytest.mark.asyncio
async def test_password_auth_login_and_protected_routes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(settings, "password", "精品密码")
    (tmp_path / "cover.txt").write_text("protected", encoding="utf-8")
    app = _create_app(tmp_path)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        status_response = await client.get("/api/v1/auth/status")
        rejected_response = await client.get("/api/v1/private")
        wrong_login = await client.post(
            "/api/v1/auth/login",
            json={"password": "wrong"},
        )
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"password": "精品密码"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        private_response = await client.get("/api/v1/private", headers=headers)
        cover_response = await client.get("/covers/cover.txt", headers=headers)

    assert status_response.json() == {"enabled": True, "authenticated": False}
    assert rejected_response.status_code == 401
    assert wrong_login.status_code == 401
    assert login_response.status_code == 200
    assert private_response.json() == {"ok": True}
    assert cover_response.text == "protected"


@pytest.mark.asyncio
async def test_password_auth_is_optional_and_rotation_invalidates_token(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    app = _create_app(tmp_path)
    monkeypatch.setattr(settings, "password", None)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        disabled_response = await client.get("/api/v1/private")
        monkeypatch.setattr(settings, "password", "first-password")
        token = issue_access_token()
        monkeypatch.setattr(settings, "password", "second-password")
        rotated_response = await client.get(
            "/api/v1/private",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert disabled_response.status_code == 200
    assert rotated_response.status_code == 401


@pytest.mark.asyncio
async def test_socket_connection_requires_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import socketio

    server = socketio.AsyncServer(async_mode="asgi")
    register_handlers(server)
    connect = server.handlers["/"]["connect"]

    monkeypatch.setattr(settings, "password", "socket-password")
    assert await connect("rejected", {}, None) is False

    token = issue_access_token()
    assert await connect("accepted", {}, {"token": token}) is None
    disconnect = server.handlers["/"]["disconnect"]
    await disconnect("accepted")
