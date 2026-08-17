import importlib
import json
from unittest.mock import AsyncMock

import pytest

from app.agent_runtime.tools.errors import ToolExecutionError
from app.agent_runtime.tools.impls.corpus.read_corpus_unit import ReadCorpusUnitTool
from app.storage.models.corpus import CorpusDocument, CorpusUnit


class FakeSession:
    async def close(self) -> None:
        return None


def _records() -> tuple[CorpusDocument, CorpusUnit]:
    document = CorpusDocument(
        id="document-1",
        content_hash="a" * 64,
        kind="novel",
        title="作品",
        managed_body_path="documents/a/body.txt",
        unit_count=1,
        char_count=10,
    )
    unit = CorpusUnit(
        id="unit-1",
        document_id=document.id,
        external_id="chapter-1",
        kind="chapter",
        order_index=0,
        byte_offset=0,
        byte_length=10,
        char_count=10,
        text_hash="b" * 64,
    )
    return document, unit


def _tool() -> ReadCorpusUnitTool:
    return ReadCorpusUnitTool(
        _state={"project_id": "project-1", "session_id": "session-1"}
    )


async def test_read_corpus_unit_pages_mounted_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = importlib.import_module(
        "app.agent_runtime.tools.impls.corpus.read_corpus_unit"
    )
    document, unit = _records()
    monkeypatch.setattr(module, "create_session", AsyncMock(return_value=FakeSession()))
    monkeypatch.setattr(module.corpus_repo, "get_unit", AsyncMock(return_value=unit))
    monkeypatch.setattr(
        module.corpus_repo,
        "get_document",
        AsyncMock(return_value=document),
    )
    monkeypatch.setattr(
        module.corpus_repo,
        "list_project_library_ids",
        AsyncMock(return_value=["library-1"]),
    )
    monkeypatch.setattr(
        module.corpus_repo,
        "list_library_ids_for_document",
        AsyncMock(return_value=["library-1"]),
    )
    monkeypatch.setattr(module, "read_unit_text", lambda _document, _unit: "0123456789")

    payload = json.loads(await _tool()._execute(unit.id, start=2, max_chars=4))

    assert payload["text"] == "2345"
    assert payload["next_start"] == 6
    assert payload["truncated"] is True


async def test_read_corpus_unit_rejects_unmounted_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = importlib.import_module(
        "app.agent_runtime.tools.impls.corpus.read_corpus_unit"
    )
    document, unit = _records()
    monkeypatch.setattr(module, "create_session", AsyncMock(return_value=FakeSession()))
    monkeypatch.setattr(module.corpus_repo, "get_unit", AsyncMock(return_value=unit))
    monkeypatch.setattr(
        module.corpus_repo,
        "get_document",
        AsyncMock(return_value=document),
    )
    monkeypatch.setattr(
        module.corpus_repo,
        "list_project_library_ids",
        AsyncMock(return_value=["library-1"]),
    )
    monkeypatch.setattr(
        module.corpus_repo,
        "list_library_ids_for_document",
        AsyncMock(return_value=["library-2"]),
    )

    with pytest.raises(ToolExecutionError, match="不属于当前项目"):
        await _tool()._execute(unit.id)
