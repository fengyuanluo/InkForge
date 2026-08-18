"""Managed corpus library API endpoints."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from typing import Annotated, Any

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.corpus import (
    CorpusDocumentListResponse,
    CorpusDocumentResponse,
    CorpusDocumentUpdateRequest,
    CorpusImportFromRootRequest,
    CorpusImportResponse,
    CorpusJobListResponse,
    CorpusJobResponse,
    CorpusLibraryCreateRequest,
    CorpusLibraryListResponse,
    CorpusLibraryResponse,
    CorpusLibraryUpdateRequest,
    CorpusProjectMountResponse,
    CorpusProjectMountUpdateRequest,
    CorpusRebuildResponse,
    CorpusSearchHitResponse,
    CorpusSearchRequest,
    CorpusSearchResponse,
    CorpusUnitBriefResponse,
    CorpusUnitListResponse,
    CorpusUnitResponse,
)
from app.background.jobs import service as background_service
from app.background.jobs.constants import JOB_TYPE_CORPUS_INDEX_BATCH
from app.background.runtime.supervisor import get_background_supervisor
from app.corpus.index import search_corpus
from app.corpus.package import prepared_package
from app.settings import settings
from app.storage.database import get_session
from app.storage.models.corpus import (
    CorpusDocument,
    CorpusDocumentIndexState,
    CorpusLibrary,
    CorpusLibraryDocument,
    CorpusUnit,
)
from app.storage.repos import corpus_repo, project_repo
from app.storage.services import corpus_service


router = APIRouter(prefix="/corpus", tags=["corpus"])
_UPLOAD_CHUNK_SIZE = 1024 * 1024


async def _commit_import(session: AsyncSession) -> None:
    try:
        await background_service.commit_and_notify(session)
    except Exception:
        try:
            await background_service.rollback_and_discard(session)
        finally:
            corpus_service.cleanup_import_files(session)
        raise
    corpus_service.confirm_import_files(session)


def _json_list(raw: str | None) -> list[str]:
    try:
        value = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return []
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _json_object(raw: str | None) -> dict[str, Any]:
    try:
        value = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


async def _library_response(
    session: AsyncSession, library: CorpusLibrary
) -> CorpusLibraryResponse:
    return CorpusLibraryResponse(
        id=library.id,
        name=library.name,
        description=library.description,
        tags=_json_list(library.tags_json),
        document_count=await corpus_repo.count_library_documents(session, library.id),
        char_count=await corpus_repo.count_library_characters(session, library.id),
        created_at=library.created_at,
        updated_at=library.updated_at,
    )


async def _document_response(
    session: AsyncSession,
    document: CorpusDocument,
    *,
    link: CorpusLibraryDocument | None = None,
    index_state: CorpusDocumentIndexState | None = None,
) -> CorpusDocumentResponse:
    if index_state is None:
        index_state = await corpus_repo.get_index_state(session, document.id)
    return CorpusDocumentResponse(
        id=document.id,
        kind=document.kind,
        title=document.title,
        author=document.author,
        dynasty=document.dynasty,
        tags=_json_list(document.tags_json),
        metadata=_json_object(document.metadata_json),
        library_ids=await corpus_repo.list_library_ids_for_document(session, document.id),
        source_aliases=_json_list(link.source_aliases_json) if link else [],
        unit_count=document.unit_count,
        char_count=document.char_count,
        index_status=index_state.status if index_state else "not_indexed",
        index_chunk_count=index_state.chunk_count if index_state else 0,
        index_job_id=index_state.job_id if index_state else None,
        index_error=index_state.last_error if index_state else None,
        indexed_at=index_state.indexed_at if index_state else None,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


def _unit_brief(unit: CorpusUnit) -> CorpusUnitBriefResponse:
    return CorpusUnitBriefResponse(
        id=unit.id,
        document_id=unit.document_id,
        kind=unit.kind,
        order=unit.order_index,
        title=unit.title,
        volume=unit.volume,
        char_count=unit.char_count,
        metadata=_json_object(unit.metadata_json),
    )


def _import_response(result: corpus_service.CorpusImportResult) -> CorpusImportResponse:
    return CorpusImportResponse(
        library_id=result.library.id,
        document_ids=result.document_ids,
        imported_count=result.imported_count,
        deduplicated_count=result.deduplicated_count,
        unit_count=result.unit_count,
        job_id=result.job_id,
    )


def _job_response(job) -> CorpusJobResponse:
    return CorpusJobResponse(
        id=job.id,
        status=job.status,
        progress=background_service.parse_json_object(job.progress_json),
        result=background_service.parse_json_object(job.result_json),
        error=background_service.parse_json_object(job.error_json),
        attempt_count=job.attempt_count,
        created_at=job.created_at,
        updated_at=job.updated_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )


async def _require_corpus_job(session: AsyncSession, job_id: str):
    job = await background_service.get_job(session, job_id)
    if job is None or job.type != JOB_TYPE_CORPUS_INDEX_BATCH:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="语料索引任务不存在",
        )
    return job


@router.get("/libraries", response_model=CorpusLibraryListResponse)
async def list_libraries(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusLibraryListResponse:
    libraries = await corpus_repo.list_libraries(session)
    return CorpusLibraryListResponse(
        items=[await _library_response(session, library) for library in libraries]
    )


@router.post(
    "/libraries",
    response_model=CorpusLibraryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_library(
    data: CorpusLibraryCreateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusLibraryResponse:
    library = await corpus_service.create_library(
        session,
        name=data.name,
        description=data.description,
        tags=data.tags,
    )
    return await _library_response(session, library)


@router.get("/libraries/{library_id}", response_model=CorpusLibraryResponse)
async def get_library(
    library_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusLibraryResponse:
    return await _library_response(
        session, await corpus_service.get_library(session, library_id)
    )


@router.patch("/libraries/{library_id}", response_model=CorpusLibraryResponse)
async def update_library(
    library_id: str,
    data: CorpusLibraryUpdateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusLibraryResponse:
    library = await corpus_service.update_library(
        session,
        library_id,
        **data.model_dump(exclude_unset=True),
    )
    return await _library_response(session, library)


@router.delete("/libraries/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(
    library_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    await corpus_service.delete_library(session, library_id)
    await background_service.commit_and_notify(session)


@router.get(
    "/libraries/{library_id}/documents",
    response_model=CorpusDocumentListResponse,
)
async def list_library_documents(
    library_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusDocumentListResponse:
    await corpus_service.get_library(session, library_id)
    rows = await corpus_repo.list_library_documents(session, library_id)
    return CorpusDocumentListResponse(
        items=[
            await _document_response(
                session,
                document,
                link=link,
                index_state=index_state,
            )
            for document, link, index_state in rows
        ]
    )


@router.get("/documents/{document_id}", response_model=CorpusDocumentResponse)
async def get_document(
    document_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusDocumentResponse:
    document = await corpus_repo.get_document(session, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="语料文档不存在")
    return await _document_response(session, document)


@router.patch("/documents/{document_id}", response_model=CorpusDocumentResponse)
async def update_document(
    document_id: str,
    data: CorpusDocumentUpdateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusDocumentResponse:
    values = data.model_dump(exclude_unset=True)
    if not values:
        raise ValueError("至少需要更新一个文档字段")
    document = await corpus_service.update_document_metadata(
        session,
        document_id,
        **values,
    )
    await corpus_service.queue_documents_for_index(session, [document.id])
    await background_service.commit_and_notify(session)
    return await _document_response(session, document)


@router.get(
    "/documents/{document_id}/units",
    response_model=CorpusUnitListResponse,
)
async def list_document_units(
    document_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusUnitListResponse:
    if await corpus_repo.get_document(session, document_id) is None:
        raise HTTPException(status_code=404, detail="语料文档不存在")
    units = await corpus_repo.list_document_units(session, document_id)
    return CorpusUnitListResponse(items=[_unit_brief(unit) for unit in units])


@router.get("/units/{unit_id}", response_model=CorpusUnitResponse)
async def read_unit(
    unit_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusUnitResponse:
    unit = await corpus_repo.get_unit(session, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="语料单元不存在")
    document = await corpus_repo.get_document(session, unit.document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="语料文档不存在")
    brief = _unit_brief(unit)
    return CorpusUnitResponse(
        **brief.model_dump(),
        document_title=document.title,
        author=document.author,
        dynasty=document.dynasty,
        text=corpus_service.read_unit_text(document, unit),
    )


@router.post("/imports/upload", response_model=CorpusImportResponse)
async def import_upload(
    file: Annotated[UploadFile, File(description="Corpus ZIP package or TXT")],
    session: Annotated[AsyncSession, Depends(get_session)],
    library_id: Annotated[str | None, Form()] = None,
    library_name: Annotated[str | None, Form(max_length=200)] = None,
) -> CorpusImportResponse:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".zip", ".txt"}:
        raise ValueError("上传仅支持 .zip 标准语料包或 .txt")
    upload_dir = settings.corpus_dir / "staging" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(suffix=suffix, dir=upload_dir)
    os.close(descriptor)
    temporary = Path(temporary_name)
    size = 0
    try:
        async with aiofiles.open(temporary, "wb") as stream:
            while chunk := await file.read(_UPLOAD_CHUNK_SIZE):
                size += len(chunk)
                if size > settings.corpus_upload_max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="语料上传文件超过服务器限制",
                    )
                await stream.write(chunk)
        with prepared_package(temporary) as package:
            result = await corpus_service.import_package(
                session,
                package,
                library_id=library_id,
                library_name=library_name,
            )
        await _commit_import(session)
        return _import_response(result)
    finally:
        temporary.unlink(missing_ok=True)
        await file.close()


@router.post("/imports/from-root", response_model=CorpusImportResponse)
async def import_from_root(
    data: CorpusImportFromRootRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusImportResponse:
    root = settings.corpus_import_root.resolve()
    relative = Path(data.path)
    source = (root / relative).resolve()
    if relative.is_absolute() or not source.is_relative_to(root):
        raise ValueError("导入路径必须位于只读导入目录内")
    with prepared_package(source) as package:
        result = await corpus_service.import_package(
            session,
            package,
            library_id=data.library_id,
            library_name=data.library_name,
        )
    await _commit_import(session)
    return _import_response(result)


@router.get(
    "/projects/{project_id}/libraries",
    response_model=CorpusProjectMountResponse,
)
async def get_project_libraries(
    project_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusProjectMountResponse:
    if await project_repo.get_by_id(session, project_id) is None:
        raise HTTPException(status_code=404, detail="项目不存在")
    library_ids = await corpus_repo.list_project_library_ids(session, project_id)
    return CorpusProjectMountResponse(project_id=project_id, library_ids=library_ids)


@router.put(
    "/projects/{project_id}/libraries",
    response_model=CorpusProjectMountResponse,
)
async def update_project_libraries(
    project_id: str,
    data: CorpusProjectMountUpdateRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusProjectMountResponse:
    library_ids = await corpus_service.mount_project_libraries(
        session, project_id, data.library_ids
    )
    return CorpusProjectMountResponse(project_id=project_id, library_ids=library_ids)


@router.post("/search", response_model=CorpusSearchResponse)
async def search(
    data: CorpusSearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusSearchResponse:
    hits = await search_corpus(
        session,
        query=data.query,
        project_id=data.project_id,
        library_ids=data.library_ids,
        limit=data.limit,
    )
    return CorpusSearchResponse(
        items=[CorpusSearchHitResponse(**hit.__dict__) for hit in hits]
    )


@router.post("/rebuild", response_model=CorpusRebuildResponse)
async def rebuild(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusRebuildResponse:
    documents = await corpus_repo.list_all_documents(session)
    if not documents:
        raise ValueError("没有可重建的语料文档")
    job_id = await corpus_service.queue_documents_for_index(
        session, [document.id for document in documents]
    )
    await background_service.commit_and_notify(session)
    return CorpusRebuildResponse(document_count=len(documents), job_id=job_id)


@router.get("/jobs", response_model=CorpusJobListResponse)
async def list_jobs(
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = Query(default=50, ge=1, le=100),
) -> CorpusJobListResponse:
    jobs = await background_service.list_jobs(
        session,
        job_type=JOB_TYPE_CORPUS_INDEX_BATCH,
        limit=limit,
    )
    return CorpusJobListResponse(items=[_job_response(job) for job in jobs])


@router.get("/jobs/{job_id}", response_model=CorpusJobResponse)
async def get_job(
    job_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusJobResponse:
    return _job_response(await _require_corpus_job(session, job_id))


@router.post("/jobs/{job_id}/pause", response_model=CorpusJobResponse)
async def pause_job(
    job_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusJobResponse:
    job = await background_service.pause_job(
        session,
        get_background_supervisor().create_event_publisher(),
        await _require_corpus_job(session, job_id),
    )
    await background_service.commit_and_notify(session)
    return _job_response(job)


@router.post("/jobs/{job_id}/resume", response_model=CorpusJobResponse)
async def resume_job(
    job_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusJobResponse:
    job = await background_service.resume_job(
        session,
        get_background_supervisor().create_event_publisher(),
        await _require_corpus_job(session, job_id),
    )
    await background_service.commit_and_notify(session)
    return _job_response(job)


@router.post("/jobs/{job_id}/cancel", response_model=CorpusJobResponse)
async def cancel_job(
    job_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusJobResponse:
    job = await background_service.cancel_job(
        session,
        get_background_supervisor().create_event_publisher(),
        await _require_corpus_job(session, job_id),
        reason="用户取消语料索引",
    )
    await background_service.commit_and_notify(session)
    return _job_response(job)


@router.post("/jobs/{job_id}/retry", response_model=CorpusJobResponse)
async def retry_job(
    job_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CorpusJobResponse:
    job = await background_service.retry_job(
        session,
        get_background_supervisor().create_event_publisher(),
        await _require_corpus_job(session, job_id),
    )
    payload = background_service.parse_json_object(job.payload_json)
    document_ids = payload.get("document_ids", [])
    if isinstance(document_ids, list):
        for document_id in document_ids:
            if not isinstance(document_id, str):
                continue
            index_state = await corpus_repo.get_index_state(session, document_id)
            if index_state is not None:
                index_state.status = "queued"
                index_state.job_id = job.id
                index_state.last_error = None
                await corpus_repo.save_index_state(session, index_state)
    await background_service.commit_and_notify(session)
    return _job_response(job)
