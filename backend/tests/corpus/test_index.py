import hashlib
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.corpus import index as corpus_index
from app.models.entities.model import Model
from app.settings import settings
from app.storage.models.corpus import (
    CorpusDocument,
    CorpusDocumentIndexState,
    CorpusUnit,
)
from app.storage.repos import corpus_repo
from tests.model_registry import register_sqlmodel_models


@pytest_asyncio.fixture
async def index_session():
    register_sqlmodel_models()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


class FakeRetrievalService:
    def __init__(self, *, fail_on_batch: int | None = None) -> None:
        self.fail_on_batch = fail_on_batch
        self.batch_sizes: list[int] = []
        self.delete_calls: list[list[str]] = []

    async def delete_documents(
        self, _session, _index_key: str, document_ids: list[str]
    ) -> None:
        self.delete_calls.append(document_ids)

    async def index_chunk_batch(
        self,
        _session,
        _index_key: str,
        chunks,
        _client,
        *,
        mark_building: bool,
    ) -> None:
        assert mark_building is False
        self.batch_sizes.append(len(chunks))
        if self.fail_on_batch == len(self.batch_sizes):
            raise RuntimeError("embedding failed")


async def _document_with_large_unit(
    session: AsyncSession,
    tmp_path: Path,
) -> tuple[CorpusDocument, Model]:
    text = "dragon hero passage. " * 5000
    encoded = text.encode("utf-8")
    content_hash = hashlib.sha256(encoded).hexdigest()
    relative = Path("documents") / content_hash / "body.txt"
    body = settings.corpus_dir / relative
    body.parent.mkdir(parents=True, exist_ok=True)
    body.write_bytes(encoded)
    document = CorpusDocument(
        id="large-document",
        content_hash=content_hash,
        kind="novel",
        title="Large work",
        managed_body_path=relative.as_posix(),
        unit_count=1,
        char_count=len(text),
    )
    unit = CorpusUnit(
        id="large-unit",
        document_id=document.id,
        external_id="chapter-1",
        kind="chapter",
        order_index=0,
        byte_offset=0,
        byte_length=len(encoded),
        char_count=len(text),
        text_hash=hashlib.sha256(encoded).hexdigest(),
    )
    state = CorpusDocumentIndexState(
        document_id=document.id,
        status="queued",
        source_hash=document.content_hash,
        job_id="job-1",
    )
    session.add_all([document, unit, state])
    await session.flush()
    model = Model(
        id="embedding-model",
        name="Embedding",
        provider_id="provider-1",
        model_id="fake-embedding",
        task_type="embedding",
        dimensions=3,
    )
    return document, model


async def test_document_indexing_flushes_bounded_embedding_batches(
    index_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    session = index_session
    monkeypatch.setattr(settings, "corpus_dir", tmp_path / "corpus")
    document, model = await _document_with_large_unit(session, tmp_path)
    document_id = document.id
    service = FakeRetrievalService()
    monkeypatch.setattr(corpus_index, "OpenFicRetrievalService", lambda: service)

    async def fake_client(_session, _model):
        return object()

    monkeypatch.setattr(corpus_index, "build_corpus_embedding_client", fake_client)

    chunk_count = await corpus_index.index_corpus_document(
        session,
        document_id=document_id,
        model=model,
    )

    state = await corpus_repo.get_index_state(session, document_id)
    assert chunk_count > corpus_index.CORPUS_EMBEDDING_BATCH_SIZE
    assert sum(service.batch_sizes) == chunk_count
    assert max(service.batch_sizes) <= corpus_index.CORPUS_EMBEDDING_BATCH_SIZE
    assert state is not None
    assert state.status == "ready"
    assert state.chunk_count == chunk_count


async def test_document_indexing_failure_deletes_partial_chunks(
    index_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    session = index_session
    monkeypatch.setattr(settings, "corpus_dir", tmp_path / "corpus")
    document, model = await _document_with_large_unit(session, tmp_path)
    document_id = document.id
    service = FakeRetrievalService(fail_on_batch=2)
    monkeypatch.setattr(corpus_index, "OpenFicRetrievalService", lambda: service)

    async def fake_client(_session, _model):
        return object()

    monkeypatch.setattr(corpus_index, "build_corpus_embedding_client", fake_client)

    with pytest.raises(RuntimeError, match="embedding failed"):
        await corpus_index.index_corpus_document(
            session,
            document_id=document_id,
            model=model,
        )

    state = await corpus_repo.get_index_state(session, document_id)
    assert len(service.delete_calls) == 2
    assert service.delete_calls[0] == service.delete_calls[1]
    assert state is not None
    assert state.status == "failed"
    assert state.job_id is None
