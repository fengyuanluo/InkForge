from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.corpus.package import validate_package
from app.settings import settings
from app.storage.models.project import Project
from app.storage.repos import corpus_repo
from app.storage.services import corpus_service
from tests.corpus.test_package import write_package


async def test_import_deduplicates_reads_offsets_mounts_and_deletes(
    session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    corpus_dir = tmp_path / "managed"
    monkeypatch.setattr(settings, "corpus_dir", corpus_dir)
    text = "  山有木兮木有枝  \n心悦君兮君不知  "

    first = await corpus_service.import_package(
        session,
        validate_package(write_package(tmp_path / "package-1", text=text)),
    )
    corpus_service.confirm_import_files(session)
    await session.commit()

    document = await corpus_repo.get_document(session, first.document_ids[0])
    assert document is not None
    unit = (await corpus_repo.list_document_units(session, document.id))[0]
    assert corpus_service.read_unit_text(document, unit) == text
    assert first.imported_count == 1
    assert first.deduplicated_count == 0

    second = await corpus_service.import_package(
        session,
        validate_package(write_package(tmp_path / "package-2", text=text)),
        library_name="第二语料库",
    )
    corpus_service.confirm_import_files(session)
    await session.commit()

    assert second.document_ids == first.document_ids
    assert second.imported_count == 0
    assert second.deduplicated_count == 1
    assert await corpus_repo.list_library_ids_for_document(session, document.id) == sorted(
        [first.library.id, second.library.id]
    )

    project = Project(id="corpus-project", title="语料项目")
    session.add(project)
    await session.flush()
    mounted = await corpus_service.mount_project_libraries(
        session,
        project.id,
        [second.library.id, first.library.id, second.library.id],
    )
    assert mounted == [second.library.id, first.library.id]

    await corpus_service.delete_library(session, first.library.id)
    await session.commit()
    assert await corpus_repo.get_document(session, document.id) is not None

    await corpus_service.delete_library(session, second.library.id)
    await session.commit()
    assert await corpus_repo.get_document(session, document.id) is None
    assert not (corpus_dir / document.managed_body_path).exists()


async def test_import_failure_removes_new_managed_files(
    session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    corpus_dir = tmp_path / "managed"
    monkeypatch.setattr(settings, "corpus_dir", corpus_dir)

    async def fail_queue(_session: AsyncSession, _document_ids: list[str]) -> str:
        raise RuntimeError("queue failed")

    monkeypatch.setattr(corpus_service, "queue_documents_for_index", fail_queue)

    with pytest.raises(RuntimeError, match="queue failed"):
        await corpus_service.import_package(
            session,
            validate_package(write_package(tmp_path / "package")),
        )

    assert not list((corpus_dir / "documents").glob("*/body.txt"))
    await session.rollback()
