"""Global corpus indexing and hybrid retrieval."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.corpus.config import (
    build_corpus_embedding_client,
    build_corpus_rerank_client,
    get_corpus_retrieval_config,
    resolve_corpus_embedding_model,
)
from app.models.entities.model import Model
from app.retrieval.chapter_index import DEFAULT_FTS_INDEX_PARAMS
from app.retrieval.internal.contracts.index_contracts import contract_from_row
from app.retrieval.internal.indexing.chunking import RecursiveCharacterChunker
from app.retrieval.service import OpenFicRetrievalService
from app.retrieval.types import (
    ChunkSearchResult,
    FilterableField,
    FilterableFieldType,
    IndexChunk,
    JSONScalar,
    RetrievalIndexContract,
)
from app.storage.models.corpus import CorpusDocument, CorpusUnit
from app.storage.repos import corpus_repo, retrieval_index_repo
from app.storage.services.corpus_service import (
    CORPUS_CHUNK_SCHEMA_VERSION,
    read_unit_text,
)


CORPUS_INDEX_KEY = "corpus:global"
CORPUS_CHUNK_SIZE = 800
CORPUS_CHUNK_OVERLAP = 100
CORPUS_POETRY_WHOLE_UNIT_LIMIT = 2000
CORPUS_EMBEDDING_BATCH_SIZE = 50
CORPUS_SEARCH_CANDIDATE_TOP_K = 40
CORPUS_RERANK_TOP_N = 30
CORPUS_SEARCH_MAX_RESULTS = 8
CORPUS_CONTEXT_BUDGET = 12_000


@dataclass(frozen=True)
class CorpusSearchHit:
    document_id: str
    unit_id: str
    chunk_index: int
    text: str
    context_text: str | None
    score: float
    matched_by: str
    title: str
    author: str | None
    dynasty: str | None
    document_kind: str
    unit_kind: str
    unit_title: str | None
    volume: str | None
    unit_order: int
    tags: list[str]
    library_ids: list[str]


def corpus_unit_document_id(unit_id: str) -> str:
    return f"corpus-unit:{unit_id}"


def build_corpus_contract(model: Model) -> RetrievalIndexContract:
    if model.dimensions is None:
        raise ValueError("语料库 Embedding 模型缺少 dimensions")
    return RetrievalIndexContract(
        embedding_model_ref_id=model.id,
        embedding_model_id_snapshot=model.model_id,
        embedding_dimensions_snapshot=model.dimensions,
        distance_metric="cosine",
        chunker_type="corpus_structure_aware",
        chunk_size=CORPUS_CHUNK_SIZE,
        chunk_overlap=CORPUS_CHUNK_OVERLAP,
        filterable_fields=[
            FilterableField(
                name="library_ids",
                field_type=FilterableFieldType.STRING_LIST,
            ),
            FilterableField(name="document_kind", field_type=FilterableFieldType.STRING),
            FilterableField(name="unit_kind", field_type=FilterableFieldType.STRING),
        ],
        fts_index_params=dict(DEFAULT_FTS_INDEX_PARAMS),
        schema_version=CORPUS_CHUNK_SCHEMA_VERSION,
    )


async def ensure_corpus_index(
    session: AsyncSession, model: Model
) -> tuple[OpenFicRetrievalService, bool]:
    service = OpenFicRetrievalService()
    contract = build_corpus_contract(model)
    existing = await retrieval_index_repo.get_by_index_key(session, CORPUS_INDEX_KEY)
    rebuild = False
    if existing is not None and contract_from_row(existing) != contract:
        existing.status = "needs_rebuild"
        await retrieval_index_repo.update(session, existing)
        rebuild = True
    elif existing is not None and existing.status == "needs_rebuild":
        rebuild = True
    await service.register_index(
        session,
        CORPUS_INDEX_KEY,
        contract,
        replace_contract_if_needs_rebuild=rebuild,
    )
    return service, rebuild


def _json_list(raw: str) -> list[str]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _metadata_prefix(document: CorpusDocument, unit: CorpusUnit) -> str:
    values = [
        document.title,
        document.author,
        document.dynasty,
        unit.volume,
        unit.title,
        " ".join(_json_list(document.tags_json)),
    ]
    return "\n".join(value for value in values if value)


def _split_unit(document: CorpusDocument, unit: CorpusUnit, text: str) -> list[str]:
    if document.kind == "poetry" and len(text) <= CORPUS_POETRY_WHOLE_UNIT_LIMIT:
        return [text]
    return RecursiveCharacterChunker(
        chunk_size=CORPUS_CHUNK_SIZE,
        chunk_overlap=CORPUS_CHUNK_OVERLAP,
    ).split_text(text)


def _build_unit_chunks(
    document: CorpusDocument,
    unit: CorpusUnit,
    text: str,
    *,
    library_values: list[JSONScalar],
    tag_values: list[JSONScalar],
) -> list[IndexChunk]:
    chunks: list[IndexChunk] = []
    prefix = _metadata_prefix(document, unit)
    retrieval_document_id = corpus_unit_document_id(unit.id)
    for chunk_index, raw_text in enumerate(_split_unit(document, unit, text)):
        chunks.append(
            IndexChunk(
                document_id=retrieval_document_id,
                chunk_index=chunk_index,
                raw_text=raw_text,
                indexed_text=f"{prefix}\n{raw_text}" if prefix else raw_text,
                attributes={
                    "library_ids": library_values,
                    "document_kind": document.kind,
                    "unit_kind": unit.kind,
                },
                metadata={
                    "corpus_document_id": document.id,
                    "unit_id": unit.id,
                    "title": document.title,
                    "author": document.author,
                    "dynasty": document.dynasty,
                    "document_kind": document.kind,
                    "unit_kind": unit.kind,
                    "unit_title": unit.title,
                    "volume": unit.volume,
                    "unit_order": unit.order_index,
                    "tags": tag_values,
                    "library_ids": library_values,
                },
            )
        )
    return chunks


async def index_corpus_document(
    session: AsyncSession,
    *,
    document_id: str,
    model: Model,
) -> int:
    document = await corpus_repo.get_document(session, document_id)
    if document is None:
        return 0
    state = await corpus_repo.get_index_state(session, document_id)
    if state is None:
        from app.storage.models.corpus import CorpusDocumentIndexState

        state = CorpusDocumentIndexState(
            document_id=document.id,
            source_hash=document.content_hash,
        )
    state.status = "indexing"
    state.embedding_model_ref_id = model.id
    state.embedding_dimensions = model.dimensions
    state.schema_version = CORPUS_CHUNK_SCHEMA_VERSION
    state.last_error = None
    await corpus_repo.save_index_state(session, state)
    await session.commit()

    unit_document_ids: list[str] = []
    service = OpenFicRetrievalService()
    try:
        units = await corpus_repo.list_document_units(session, document.id)
        unit_document_ids = [corpus_unit_document_id(unit.id) for unit in units]
        library_values: list[JSONScalar] = list(
            await corpus_repo.list_library_ids_for_document(session, document.id)
        )
        tag_values: list[JSONScalar] = list(_json_list(document.tags_json))
        client = await build_corpus_embedding_client(session, model)
        await service.delete_documents(session, CORPUS_INDEX_KEY, unit_document_ids)

        chunk_count = 0
        pending_chunks: list[IndexChunk] = []

        async def flush_chunks() -> None:
            nonlocal chunk_count
            if not pending_chunks:
                return
            await service.index_chunk_batch(
                session,
                CORPUS_INDEX_KEY,
                pending_chunks,
                client,
                mark_building=False,
            )
            chunk_count += len(pending_chunks)
            pending_chunks.clear()

        for unit in units:
            for chunk in _build_unit_chunks(
                document,
                unit,
                read_unit_text(document, unit),
                library_values=library_values,
                tag_values=tag_values,
            ):
                pending_chunks.append(chunk)
                if len(pending_chunks) == CORPUS_EMBEDDING_BATCH_SIZE:
                    await flush_chunks()
        await flush_chunks()

        state.status = "ready"
        state.source_hash = document.content_hash
        state.chunk_count = chunk_count
        state.job_id = None
        state.last_error = None
        from datetime import UTC, datetime

        state.indexed_at = datetime.now(UTC)
        await corpus_repo.save_index_state(session, state)
        await session.commit()
        return chunk_count
    except Exception as exc:
        await session.rollback()
        cleanup_error: Exception | None = None
        if unit_document_ids:
            try:
                await service.delete_documents(
                    session,
                    CORPUS_INDEX_KEY,
                    unit_document_ids,
                )
            except Exception as cleanup_exc:
                cleanup_error = cleanup_exc
        state = await corpus_repo.get_index_state(session, document_id)
        if state is not None:
            state.status = "failed"
            state.job_id = None
            state.last_error = (
                str(exc)
                if cleanup_error is None
                else f"{exc}; partial index cleanup failed: {cleanup_error}"
            )
            await corpus_repo.save_index_state(session, state)
            await session.commit()
        raise


def _metadata_string(metadata: dict[str, Any], key: str) -> str | None:
    value = metadata.get(key)
    return value if isinstance(value, str) and value else None


def _metadata_string_list(metadata: dict[str, Any], key: str) -> list[str]:
    value = metadata.get(key)
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


async def _to_search_hit(
    session: AsyncSession,
    result: ChunkSearchResult,
    *,
    remaining_context_budget: int,
) -> CorpusSearchHit | None:
    metadata = result.metadata
    document_id = _metadata_string(metadata, "corpus_document_id")
    unit_id = _metadata_string(metadata, "unit_id")
    if not document_id or not unit_id:
        return None
    document = await corpus_repo.get_document(session, document_id)
    unit = await corpus_repo.get_unit(session, unit_id)
    if document is None or unit is None or unit.document_id != document.id:
        return None
    context_text: str | None = None
    if document.kind in {"novel", "generic"} and remaining_context_budget > len(result.text):
        full_text = read_unit_text(document, unit)
        position = full_text.find(result.text)
        if position >= 0:
            allowance = min(remaining_context_budget, 3000)
            side = max((allowance - len(result.text)) // 2, 0)
            start = max(0, position - side)
            context_text = full_text[start : start + allowance]
    return CorpusSearchHit(
        document_id=document.id,
        unit_id=unit.id,
        chunk_index=result.chunk_index,
        text=result.text,
        context_text=context_text,
        score=result.score,
        matched_by=result.matched_by,
        title=document.title,
        author=document.author,
        dynasty=document.dynasty,
        document_kind=document.kind,
        unit_kind=unit.kind,
        unit_title=unit.title,
        volume=unit.volume,
        unit_order=unit.order_index,
        tags=_json_list(document.tags_json),
        library_ids=_metadata_string_list(metadata, "library_ids"),
    )


async def search_corpus(
    session: AsyncSession,
    *,
    query: str,
    project_id: str | None = None,
    library_ids: list[str] | None = None,
    limit: int = CORPUS_SEARCH_MAX_RESULTS,
) -> list[CorpusSearchHit]:
    query = query.strip()
    if not query:
        raise ValueError("检索语句不能为空")
    selected_library_ids = list(dict.fromkeys(library_ids or []))
    if project_id is not None:
        mounted = await corpus_repo.list_project_library_ids(session, project_id)
        selected_library_ids = (
            [library_id for library_id in selected_library_ids if library_id in mounted]
            if selected_library_ids
            else mounted
        )
    if not selected_library_ids:
        raise ValueError("没有可检索的语料库，请先挂载或选择语料库")

    config = await get_corpus_retrieval_config(session)
    model = await resolve_corpus_embedding_model(session, config.embedding_model_ref_id)
    client = await build_corpus_embedding_client(session, model)
    builder = await OpenFicRetrievalService().query(
        session,
        CORPUS_INDEX_KEY,
        query,
        client,
    )
    builder = (
        builder.hybrid()
        .vector_top_k(CORPUS_SEARCH_CANDIDATE_TOP_K)
        .bm25_top_k(CORPUS_SEARCH_CANDIDATE_TOP_K)
        .rrf_weights(vector=0.7, bm25=0.3)
        .filter_array_any("library_ids", selected_library_ids)
    )
    if config.rerank_enabled:
        rerank_client = await build_corpus_rerank_client(
            session, config.rerank_model_ref_id
        )
        if rerank_client is not None:
            builder = builder.rerank(rerank_client, top_n=CORPUS_RERANK_TOP_N)
    results = await builder.limit(max(1, min(limit, CORPUS_SEARCH_MAX_RESULTS))).run()

    hits: list[CorpusSearchHit] = []
    context_budget = CORPUS_CONTEXT_BUDGET
    for result in results:
        hit = await _to_search_hit(
            session,
            result,
            remaining_context_budget=context_budget,
        )
        if hit is None:
            continue
        hits.append(hit)
        context_budget -= len(hit.context_text or hit.text)
        if context_budget <= 0:
            break
    return hits
