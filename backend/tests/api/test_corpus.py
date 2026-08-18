from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.storage.models.project import Project


async def test_corpus_library_crud_and_project_mount(
    client: AsyncClient,
    session: AsyncSession,
) -> None:
    created = await client.post(
        "/api/v1/corpus/libraries",
        json={"name": "唐诗", "description": "精选诗歌", "tags": ["poetry"]},
    )
    assert created.status_code == 201
    library_id = created.json()["id"]

    listed = await client.get("/api/v1/corpus/libraries")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()["items"]] == [library_id]

    session.add(Project(id="corpus-project", title="语料项目"))
    await session.flush()
    mounted = await client.put(
        "/api/v1/corpus/projects/corpus-project/libraries",
        json={"library_ids": [library_id]},
    )
    assert mounted.status_code == 200
    assert mounted.json()["library_ids"] == [library_id]

    deleted = await client.delete(f"/api/v1/corpus/libraries/{library_id}")
    assert deleted.status_code == 204


async def test_import_from_root_rejects_path_escape(
    client: AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    import_root = tmp_path / "imports"
    import_root.mkdir()
    monkeypatch.setattr(settings, "corpus_import_root", import_root)

    response = await client.post(
        "/api/v1/corpus/imports/from-root",
        json={"path": "../outside.zip"},
    )

    assert response.status_code == 400
    assert "只读导入目录" in response.json()["detail"]
