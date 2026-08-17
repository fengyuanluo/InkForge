"""Background job for indexing managed corpus documents."""

from __future__ import annotations

import asyncio

from pydantic import BaseModel, Field

from app.background.jobs.base import JobDefinition
from app.background.jobs.constants import JOB_QUEUE_DEFAULT, JOB_TYPE_CORPUS_INDEX_BATCH
from app.background.runtime.context import JobContext
from app.corpus.config import get_corpus_retrieval_config, resolve_corpus_embedding_model
from app.corpus.index import CORPUS_INDEX_KEY, ensure_corpus_index, index_corpus_document
from app.retrieval.service import OpenFicRetrievalService
from app.storage.database import create_session
from app.storage.repos import corpus_repo, retrieval_index_repo
from app.storage.services.corpus_service import CORPUS_CHUNK_SCHEMA_VERSION


class CorpusIndexBatchInput(BaseModel):
    document_ids: list[str] = Field(min_length=1)


class CorpusIndexBatchContext(BaseModel):
    embedding_model_ref_id: str = ""


async def _index_one(document_id: str, model) -> tuple[str, int, str | None]:
    session = await create_session()
    try:
        try:
            chunks = await index_corpus_document(
                session,
                document_id=document_id,
                model=model,
            )
            return document_id, chunks, None
        except Exception as exc:
            return document_id, 0, str(exc)
    finally:
        await session.close()


async def _mark_owned_states(
    context: JobContext,
    reason: str,
    *,
    status: str,
) -> None:
    payload = CorpusIndexBatchInput.model_validate(context.input)
    for document_id in payload.document_ids:
        state = await corpus_repo.get_index_state(context.session, document_id)
        if state is None or state.job_id != context.job_id:
            continue
        state.status = status
        state.job_id = None
        state.last_error = reason
        await corpus_repo.save_index_state(context.session, state)


async def _handle_failed(context: JobContext, reason: str) -> None:
    await _mark_owned_states(context, reason, status="failed")
    await _settle_global_index(context, reason)


async def _handle_cancelled(context: JobContext, reason: str) -> None:
    await _mark_owned_states(context, reason, status="needs_rebuild")
    await _settle_global_index(context, reason)


async def _settle_global_index(context: JobContext, reason: str) -> None:
    index = await retrieval_index_repo.get_by_index_key(
        context.session, CORPUS_INDEX_KEY
    )
    if index is None or index.status == "ready":
        return
    if await corpus_repo.has_ready_index_state(context.session):
        try:
            await OpenFicRetrievalService().finalize_chunk_index(
                context.session, CORPUS_INDEX_KEY
            )
            return
        except Exception as exc:
            reason = f"{reason}; finalize failed: {exc}"
            index = await retrieval_index_repo.get_by_index_key(
                context.session, CORPUS_INDEX_KEY
            )
            if index is None:
                return
    index.status = "failed"
    index.last_error = reason
    await retrieval_index_repo.update(context.session, index)


async def handle_corpus_index_batch(context: JobContext) -> dict[str, int]:
    payload = CorpusIndexBatchInput.model_validate(context.input)
    snapshot = CorpusIndexBatchContext.model_validate(context.metadata)
    config = await get_corpus_retrieval_config(context.session)
    if snapshot.embedding_model_ref_id and (
        snapshot.embedding_model_ref_id != config.embedding_model_ref_id
    ):
        await corpus_repo.mark_all_index_states_needs_rebuild(context.session)
    model = await resolve_corpus_embedding_model(
        context.session,
        config.embedding_model_ref_id,
    )
    retrieval_service, rebuild = await ensure_corpus_index(context.session, model)

    if rebuild:
        documents = await corpus_repo.list_all_documents(context.session)
    else:
        documents = await corpus_repo.list_documents_by_ids(
            context.session,
            list(dict.fromkeys(payload.document_ids)),
        )

    targets = []
    for document in documents:
        state = await corpus_repo.get_index_state(context.session, document.id)
        if (
            not rebuild
            and state is not None
            and state.status == "ready"
            and state.source_hash == document.content_hash
            and state.embedding_model_ref_id == model.id
            and state.embedding_dimensions == model.dimensions
            and state.schema_version == CORPUS_CHUNK_SCHEMA_VERSION
        ):
            continue
        targets.append(document.id)
    await context.commit()

    succeeded = 0
    failed = 0
    chunk_count = 0
    errors: list[str] = []
    for offset in range(0, len(targets), config.index_concurrency):
        await context.check_cancelled()
        await context.check_paused()
        batch = targets[offset : offset + config.index_concurrency]
        results = await asyncio.gather(
            *[_index_one(document_id, model) for document_id in batch]
        )
        for document_id, chunks, error in results:
            if error is None:
                succeeded += 1
                chunk_count += chunks
            else:
                failed += 1
                errors.append(f"{document_id}: {error}")
        await context.progress(
            succeeded + failed,
            total=len(targets),
            message=f"语料索引 {succeeded + failed}/{len(targets)}",
        )

    await context.check_cancelled()
    await context.check_paused()
    index = await retrieval_index_repo.get_by_index_key(
        context.session, CORPUS_INDEX_KEY
    )
    should_finalize = succeeded > 0 or (
        not targets
        and bool(documents)
        and index is not None
        and index.status != "ready"
    )
    if should_finalize:
        await retrieval_service.finalize_chunk_index(context.session, CORPUS_INDEX_KEY)
        await context.commit()
    if errors:
        raise RuntimeError(f"{failed} 个语料文档索引失败：{errors[0]}")
    return {
        "total": len(targets),
        "succeeded": succeeded,
        "failed": failed,
        "chunks": chunk_count,
    }


CORPUS_INDEX_BATCH_JOB = JobDefinition(
    type=JOB_TYPE_CORPUS_INDEX_BATCH,
    name="Corpus index batch",
    description="Index managed corpus documents into the shared retrieval table.",
    input_model=CorpusIndexBatchInput,
    handler=handle_corpus_index_batch,
    on_failed=_handle_failed,
    on_timeout=_handle_failed,
    on_cancelled=_handle_cancelled,
    default_queue=JOB_QUEUE_DEFAULT,
    default_timeout_seconds=3600,
    default_max_attempts=1,
    supports_cancel=True,
    supports_batch=True,
)
