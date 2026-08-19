from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import app.novel_research.service as service
from app.novel_research.common import HarvestError


def test_unexpected_parser_failure_is_reported_with_site_and_stage(monkeypatch) -> None:
    class BrokenAdapter:
        def ranks(self):
            raise ValueError("changed markup")

    class Client:
        def close(self):
            return None

    monkeypatch.setattr(
        service,
        "_create_adapter",
        lambda *_args, **_kwargs: (BrokenAdapter(), Client()),
    )

    with pytest.raises(HarvestError, match="fanqie:ranks: parser failed"):
        service._load_rankings("fanqie")


@pytest.mark.asyncio
async def test_discover_rankings_filters_and_reuses_process_cache(monkeypatch) -> None:
    calls = 0

    def load_rankings(site: str):
        nonlocal calls
        calls += 1
        assert site == "fanqie"
        return "2026-08-19T12:00:00+00:00", [
            {
                "site": "fanqie",
                "rank_id": "1_1_1141",
                "name": "男频·新书榜·都市",
                "dimensions": {"category": {"id": "1141", "name": "都市"}},
                "url": "https://fanqienovel.com/rank/1_1_1141",
            },
            {
                "site": "fanqie",
                "rank_id": "0_2_7",
                "name": "女频·阅读榜·古言",
                "dimensions": {"category": {"id": "7", "name": "古言"}},
                "url": "https://fanqienovel.com/rank/0_2_7",
            },
        ]

    service.clear_ranking_cache()
    monkeypatch.setattr(service, "_load_rankings", load_rankings)

    first = await service.discover_rankings("fanqie", query="都市", limit=10)
    second = await service.discover_rankings("fanqie", query="新书", limit=10)

    assert calls == 1
    assert first["total_matches"] == 1
    assert first["rankings"][0]["rank_id"] == "1_1_1141"
    assert second["rankings"][0]["name"] == "男频·新书榜·都市"


@pytest.mark.asyncio
async def test_list_and_opening_do_not_write_or_cache_content(monkeypatch) -> None:
    ranked = (
        {"site": "fanqie", "rank_id": "1_1_1141", "name": "新书榜"},
        [{"rank": 1, "book": {"source_book_id": "book-1", "title": "样书"}}],
    )
    opening = {
        "source_book_id": "book-1",
        "title": "样书",
        "chapters": [{"index": 1, "content": "正文"}],
    }
    load_ranked = AsyncMock(return_value=ranked)
    load_opening = AsyncMock(return_value=opening)

    async def to_thread(function, *args):
        if function is service._load_ranked_novels:
            return await load_ranked(*args)
        return await load_opening(*args)

    monkeypatch.setattr(service.asyncio, "to_thread", to_thread)

    listed = await service.list_ranked_novels(
        "fanqie",
        rank_id="1_1_1141",
        limit=1,
    )
    read = await service.read_novel_opening(
        "fanqie",
        source_book_id="book-1",
    )

    assert listed["items"][0]["book"]["title"] == "样书"
    assert read["book"]["chapters"][0]["content"] == "正文"
    load_ranked.assert_awaited_once_with("fanqie", "1_1_1141", 1)
    load_opening.assert_awaited_once_with("fanqie", "book-1", 3)
