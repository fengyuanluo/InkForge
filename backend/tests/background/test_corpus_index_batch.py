import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.background.events.publisher import BackgroundEventPublisher
from app.background.jobs import service as background_service
from app.background.jobs.constants import JOB_TYPE_CORPUS_INDEX_BATCH
from app.background.jobs.definitions import register_background_job_type
from app.background.jobs.definitions import corpus_index_batch
from app.background.jobs.models import BackgroundJob
from app.background.jobs.states import (
    JOB_STATUS_CANCEL_REQUESTED,
    JOB_STATUS_CANCELLED,
    JOB_STATUS_PAUSED,
)
from app.storage.models.corpus import CorpusDocument, CorpusDocumentIndexState
from app.storage.repos import corpus_repo


async def _paused_corpus_job(
    session: AsyncSession, *, locked: bool
) -> tuple[BackgroundJob, CorpusDocumentIndexState]:
    document = CorpusDocument(
        id="corpus-document",
        content_hash="a" * 64,
        kind="generic",
        title="测试语料",
        managed_body_path="documents/a/body.txt",
        unit_count=1,
        char_count=4,
    )
    job = BackgroundJob(
        id="corpus-job",
        type=JOB_TYPE_CORPUS_INDEX_BATCH,
        status=JOB_STATUS_PAUSED,
        payload_json=json.dumps({"document_ids": [document.id]}),
        locked_by="worker-1" if locked else None,
    )
    state = CorpusDocumentIndexState(
        document_id=document.id,
        status="queued",
        source_hash=document.content_hash,
        job_id=job.id,
    )
    session.add_all([document, job, state])
    await session.flush()
    return job, state


async def test_cancel_unlocked_paused_job_runs_corpus_cleanup(
    session: AsyncSession,
) -> None:
    register_background_job_type(JOB_TYPE_CORPUS_INDEX_BATCH)
    job, state = await _paused_corpus_job(session, locked=False)

    cancelled = await background_service.cancel_job(
        session,
        BackgroundEventPublisher(),
        job,
        reason="user cancelled",
    )
    await session.refresh(state)

    assert cancelled.status == JOB_STATUS_CANCELLED
    assert state.status == "needs_rebuild"
    assert state.job_id is None


async def test_cancel_locked_paused_job_waits_for_worker_checkpoint(
    session: AsyncSession,
) -> None:
    register_background_job_type(JOB_TYPE_CORPUS_INDEX_BATCH)
    job, state = await _paused_corpus_job(session, locked=True)

    requested = await background_service.cancel_job(
        session,
        BackgroundEventPublisher(),
        job,
        reason="user cancelled",
    )
    persisted = await corpus_repo.get_index_state(session, state.document_id)

    assert requested.status == JOB_STATUS_CANCEL_REQUESTED
    assert requested.cancel_requested_at is not None
    assert persisted is not None
    assert persisted.status == "queued"
    assert persisted.job_id == job.id


async def test_failed_batch_marks_unready_global_index_failed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    index = SimpleNamespace(status="registered", last_error=None)
    update = AsyncMock()
    monkeypatch.setattr(
        corpus_index_batch.retrieval_index_repo,
        "get_by_index_key",
        AsyncMock(return_value=index),
    )
    monkeypatch.setattr(
        corpus_index_batch.retrieval_index_repo,
        "update",
        update,
    )
    monkeypatch.setattr(
        corpus_index_batch.corpus_repo,
        "has_ready_index_state",
        AsyncMock(return_value=False),
    )
    context = SimpleNamespace(session=object())

    await corpus_index_batch._settle_global_index(context, "embedding failed")

    assert index.status == "failed"
    assert index.last_error == "embedding failed"
    update.assert_awaited_once_with(context.session, index)
