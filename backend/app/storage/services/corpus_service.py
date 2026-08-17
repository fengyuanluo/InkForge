"""Managed corpus library import and lifecycle service."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.background.jobs import service as background_service
from app.background.jobs.constants import JOB_TYPE_CORPUS_INDEX_BATCH
from app.core.errors import NotFoundError, ValidationError
from app.corpus.package import (
    CorpusPackageDocument,
    CorpusPackageUnit,
    ValidatedCorpusPackage,
    iter_units,
    normalize_unit_text,
)
from app.settings import settings
from app.storage.models.corpus import (
    CorpusDocument,
    CorpusDocumentIndexState,
    CorpusLibrary,
    CorpusLibraryDocument,
    CorpusUnit,
)
from app.storage.repos import corpus_repo, project_repo


CORPUS_CHUNK_SCHEMA_VERSION = 1
_HASH_SEPARATOR = b"\n\x1e\n"
_IMPORT_ARTIFACTS_KEY = "corpus_import_artifacts"


@dataclass
class CorpusImportResult:
    library: CorpusLibrary
    document_ids: list[str]
    imported_count: int
    deduplicated_count: int
    unit_count: int
    job_id: str


@dataclass
class _PreparedDocument:
    content_hash: str
    body_path: Path
    units: list[dict[str, Any]]
    char_count: int


@dataclass
class _ImportArtifacts:
    document_dirs: set[Path] = field(default_factory=set)
    files: set[Path] = field(default_factory=set)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _json_list(raw: str | None) -> list[str]:
    try:
        value = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


async def create_library(
    session: AsyncSession,
    *,
    name: str,
    description: str | None = None,
    tags: list[str] | None = None,
) -> CorpusLibrary:
    name = name.strip()
    if not name:
        raise ValidationError("语料库名称不能为空")
    return await corpus_repo.create_library(
        session,
        CorpusLibrary(
            name=name,
            description=(description or "").strip() or None,
            tags_json=_json(list(dict.fromkeys(tags or []))),
        ),
    )


async def get_library(session: AsyncSession, library_id: str) -> CorpusLibrary:
    library = await corpus_repo.get_library(session, library_id)
    if library is None:
        raise NotFoundError(f"语料库不存在: {library_id}")
    return library


async def update_library(
    session: AsyncSession,
    library_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
) -> CorpusLibrary:
    library = await get_library(session, library_id)
    if name is not None:
        cleaned = name.strip()
        if not cleaned:
            raise ValidationError("语料库名称不能为空")
        library.name = cleaned
    if description is not None:
        library.description = description.strip() or None
    if tags is not None:
        library.tags_json = _json(list(dict.fromkeys(tags)))
    return await corpus_repo.update_library(session, library)


async def update_document_metadata(
    session: AsyncSession,
    document_id: str,
    *,
    title: str | None = None,
    author: str | None = None,
    dynasty: str | None = None,
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> CorpusDocument:
    document = await corpus_repo.get_document(session, document_id)
    if document is None:
        raise NotFoundError(f"语料文档不存在: {document_id}")
    if title is not None:
        cleaned = title.strip()
        if not cleaned:
            raise ValidationError("文档标题不能为空")
        document.title = cleaned
    if author is not None:
        document.author = author.strip() or None
    if dynasty is not None:
        document.dynasty = dynasty.strip() or None
    if tags is not None:
        document.tags_json = _json(list(dict.fromkeys(tags)))
    if metadata is not None:
        document.metadata_json = _json(metadata)
    return await corpus_repo.update_document(session, document)


def _prepare_document(
    document: CorpusPackageDocument,
    unit_iterator,
    current_unit: CorpusPackageUnit | None,
) -> tuple[_PreparedDocument, CorpusPackageUnit | None]:
    staging = settings.corpus_dir / "staging"
    staging.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix="body-", suffix=".txt", dir=staging)
    os.close(fd)
    temporary = Path(temporary_name)
    digest = hashlib.sha256()
    unit_rows: list[dict[str, Any]] = []
    char_count = 0
    first = True
    try:
        with temporary.open("wb") as body:
            while current_unit is not None and current_unit.document_id == document.id:
                text = normalize_unit_text(current_unit.text)
                encoded = text.encode("utf-8")
                if not first:
                    digest.update(_HASH_SEPARATOR)
                digest.update(encoded)
                first = False
                offset = body.tell()
                body.write(encoded)
                unit_rows.append(
                    {
                        "external_id": current_unit.id,
                        "kind": current_unit.kind,
                        "order_index": current_unit.order,
                        "title": current_unit.title,
                        "volume": current_unit.volume,
                        "byte_offset": offset,
                        "byte_length": len(encoded),
                        "char_count": len(text),
                        "text_hash": hashlib.sha256(encoded).hexdigest(),
                        "metadata_json": _json(current_unit.metadata),
                    }
                )
                char_count += len(text)
                current_unit = next(unit_iterator, None)
        if not unit_rows:
            raise ValidationError(f"文档没有 unit: {document.id}")
        return (
            _PreparedDocument(
                content_hash=digest.hexdigest(),
                body_path=temporary,
                units=unit_rows,
                char_count=char_count,
            ),
            current_unit,
        )
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _managed_document_dir(content_hash: str) -> Path:
    return settings.corpus_dir / "documents" / content_hash


def _import_artifacts(session: AsyncSession) -> _ImportArtifacts:
    artifacts = session.info.get(_IMPORT_ARTIFACTS_KEY)
    if isinstance(artifacts, _ImportArtifacts):
        return artifacts
    artifacts = _ImportArtifacts()
    session.info[_IMPORT_ARTIFACTS_KEY] = artifacts
    return artifacts


def confirm_import_files(session: AsyncSession) -> None:
    session.info.pop(_IMPORT_ARTIFACTS_KEY, None)


def cleanup_import_files(session: AsyncSession) -> None:
    artifacts = session.info.pop(_IMPORT_ARTIFACTS_KEY, None)
    if not isinstance(artifacts, _ImportArtifacts):
        return
    for path in artifacts.files:
        path.unlink(missing_ok=True)
    for path in sorted(artifacts.document_dirs, key=lambda item: len(item.parts), reverse=True):
        shutil.rmtree(path, ignore_errors=True)

    documents_root = (settings.corpus_dir / "documents").resolve()
    for path in artifacts.files:
        parent = path.parent
        while parent != documents_root and parent.is_relative_to(documents_root):
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent


def _install_body(prepared: _PreparedDocument, artifacts: _ImportArtifacts) -> str:
    document_dir = _managed_document_dir(prepared.content_hash)
    if not document_dir.exists():
        artifacts.document_dirs.add(document_dir)
    document_dir.mkdir(parents=True, exist_ok=True)
    body_path = document_dir / "body.txt"
    if not body_path.exists():
        artifacts.files.add(body_path)
        os.replace(prepared.body_path, body_path)
    else:
        prepared.body_path.unlink(missing_ok=True)
    return body_path.relative_to(settings.corpus_dir).as_posix()


def _copy_source(
    package: ValidatedCorpusPackage,
    document: CorpusPackageDocument,
    *,
    content_hash: str,
    library_id: str,
    artifacts: _ImportArtifacts,
) -> None:
    if document.source is None:
        return
    pure = PurePosixPath(document.source)
    relative = Path(*pure.parts[1:])
    source = package.root / Path(*pure.parts)
    destination = _managed_document_dir(content_hash) / "sources" / library_id / relative
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    artifacts.files.add(destination)
    shutil.copy2(source, destination)


async def _resolve_import_library(
    session: AsyncSession,
    package: ValidatedCorpusPackage,
    *,
    library_id: str | None,
    library_name: str | None,
) -> CorpusLibrary:
    if library_id:
        return await get_library(session, library_id)
    return await create_library(
        session,
        name=(library_name or package.manifest.name).strip(),
        description=package.manifest.description,
        tags=package.manifest.tags,
    )


async def queue_documents_for_index(
    session: AsyncSession,
    document_ids: list[str],
) -> str:
    from app.corpus.config import get_corpus_retrieval_config

    document_ids = list(dict.fromkeys(document_ids))
    model_ref_id = (await get_corpus_retrieval_config(session)).embedding_model_ref_id
    job = await background_service.submit_job(
        session,
        job_type=JOB_TYPE_CORPUS_INDEX_BATCH,
        payload={"document_ids": document_ids},
        context={"embedding_model_ref_id": model_ref_id},
        subject_type="corpus",
        subject_id=None,
        max_attempts=1,
        timeout_seconds=3600,
    )
    for document in await corpus_repo.list_documents_by_ids(session, document_ids):
        state = await corpus_repo.get_index_state(session, document.id)
        if state is None:
            state = CorpusDocumentIndexState(
                document_id=document.id,
                status="queued",
                source_hash=document.content_hash,
                schema_version=CORPUS_CHUNK_SCHEMA_VERSION,
                job_id=job.id,
            )
        else:
            state.status = "queued"
            state.job_id = job.id
            state.last_error = None
        await corpus_repo.save_index_state(session, state)
    return job.id


async def import_package(
    session: AsyncSession,
    package: ValidatedCorpusPackage,
    *,
    library_id: str | None = None,
    library_name: str | None = None,
) -> CorpusImportResult:
    settings.corpus_dir.mkdir(parents=True, exist_ok=True)
    artifacts = _import_artifacts(session)
    prepared: _PreparedDocument | None = None
    try:
        library = await _resolve_import_library(
            session,
            package,
            library_id=library_id,
            library_name=library_name,
        )
        unit_iterator = iter(iter_units(package.root))
        current_unit = next(unit_iterator, None)
        document_ids: list[str] = []
        imported_count = 0
        deduplicated_count = 0
        unit_count = 0

        for package_document in package.documents:
            prepared, current_unit = _prepare_document(
                package_document,
                unit_iterator,
                current_unit,
            )
            existing = await corpus_repo.get_document_by_hash(
                session, prepared.content_hash
            )
            if existing is None:
                managed_path = _install_body(prepared, artifacts)
                document = await corpus_repo.create_document(
                    session,
                    CorpusDocument(
                        content_hash=prepared.content_hash,
                        kind=package_document.kind,
                        title=package_document.title,
                        author=package_document.author,
                        dynasty=package_document.dynasty,
                        tags_json=_json(package_document.tags),
                        metadata_json=_json(package_document.metadata),
                        managed_body_path=managed_path,
                        unit_count=len(prepared.units),
                        char_count=prepared.char_count,
                    ),
                )
                await corpus_repo.create_units(
                    session,
                    [CorpusUnit(document_id=document.id, **row) for row in prepared.units],
                )
                imported_count += 1
            else:
                prepared.body_path.unlink(missing_ok=True)
                document = existing
                deduplicated_count += 1
            prepared = None

            _copy_source(
                package,
                package_document,
                content_hash=document.content_hash,
                library_id=library.id,
                artifacts=artifacts,
            )
            link = await corpus_repo.get_library_document_link(
                session, library.id, document.id
            )
            aliases = [package_document.source] if package_document.source else []
            if link is None:
                link = CorpusLibraryDocument(
                    library_id=library.id,
                    document_id=document.id,
                    source_aliases_json=_json(aliases),
                    metadata_json=_json(package_document.metadata),
                )
            else:
                link.source_aliases_json = _json(
                    list(dict.fromkeys([*_json_list(link.source_aliases_json), *aliases]))
                )
                link.metadata_json = _json(package_document.metadata)
            await corpus_repo.save_library_document_link(session, link)
            document_ids.append(document.id)
            unit_count += document.unit_count

        if current_unit is not None:
            raise ValidationError(f"存在未归属的 unit: {current_unit.id}")
        library.updated_at = datetime.now(UTC)
        await corpus_repo.update_library(session, library)
        job_id = await queue_documents_for_index(session, document_ids)
        return CorpusImportResult(
            library=library,
            document_ids=document_ids,
            imported_count=imported_count,
            deduplicated_count=deduplicated_count,
            unit_count=unit_count,
            job_id=job_id,
        )
    except Exception:
        if prepared is not None:
            prepared.body_path.unlink(missing_ok=True)
        cleanup_import_files(session)
        raise


def read_unit_text(document: CorpusDocument, unit: CorpusUnit) -> str:
    root = settings.corpus_dir.resolve()
    body_path = (settings.corpus_dir / document.managed_body_path).resolve()
    if not body_path.is_relative_to(root):
        raise RuntimeError("语料正文路径越界")
    try:
        with body_path.open("rb") as stream:
            stream.seek(unit.byte_offset)
            raw = stream.read(unit.byte_length)
    except OSError as exc:
        raise RuntimeError(f"无法读取语料正文: {document.id}") from exc
    if len(raw) != unit.byte_length:
        raise RuntimeError(f"语料正文不完整: {unit.id}")
    return raw.decode("utf-8")


async def mount_project_libraries(
    session: AsyncSession, project_id: str, library_ids: list[str]
) -> list[str]:
    if await project_repo.get_by_id(session, project_id) is None:
        raise NotFoundError(f"项目不存在: {project_id}")
    unique_ids = list(dict.fromkeys(library_ids))
    for library_id in unique_ids:
        if await corpus_repo.get_library(session, library_id) is None:
            raise NotFoundError(f"语料库不存在: {library_id}")
    await corpus_repo.replace_project_libraries(session, project_id, unique_ids)
    return unique_ids


async def delete_library(session: AsyncSession, library_id: str) -> None:
    library = await get_library(session, library_id)
    document_ids = await corpus_repo.list_document_ids_for_library(session, library_id)
    await corpus_repo.delete_project_mounts_for_library(session, library_id)
    await corpus_repo.unlink_library_documents(session, library_id)

    retained_document_ids: list[str] = []
    for document_id in document_ids:
        document = await corpus_repo.get_document(session, document_id)
        if document is None:
            continue
        shutil.rmtree(
            _managed_document_dir(document.content_hash) / "sources" / library_id,
            ignore_errors=True,
        )
        if await corpus_repo.document_membership_count(session, document_id) > 0:
            retained_document_ids.append(document_id)
            continue
        units = await corpus_repo.list_document_units(session, document_id)
        try:
            from app.corpus.index import CORPUS_INDEX_KEY, corpus_unit_document_id
            from app.retrieval.service import OpenFicRetrievalService

            await OpenFicRetrievalService().delete_documents(
                session,
                CORPUS_INDEX_KEY,
                [corpus_unit_document_id(unit.id) for unit in units],
            )
        except ValueError:
            pass
        await corpus_repo.delete_document_row(session, document)
        shutil.rmtree(_managed_document_dir(document.content_hash), ignore_errors=True)

    await corpus_repo.delete_library_row(session, library)
    if retained_document_ids:
        await queue_documents_for_index(session, retained_document_ids)
