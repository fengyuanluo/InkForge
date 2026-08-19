from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from app.agent_runtime.agents.tool_categories import get_tool_names_for_categories
from app.agent_runtime.tools.impls.market_research.novels import (
    DiscoverNovelRankingsTool,
    ListRankedNovelsTool,
    ReadNovelOpeningTool,
)
from app.skills import load_builtin_skill


def test_novel_project_research_skill_is_loadable() -> None:
    skill = load_builtin_skill("builtin-skill--novel-project-research")

    assert skill is not None
    assert skill.name == "新书立项与黄金三章研究"
    assert {reference.title for reference in skill.references} == {
        "对标书卡模板",
        "公开采集边界",
    }
    assert "read_novel_opening" in skill.content
    assert "不写入项目笔记" in skill.content


def test_market_research_category_contains_three_readonly_tools() -> None:
    assert get_tool_names_for_categories(["market_research"]) == (
        "discover_novel_rankings",
        "list_ranked_novels",
        "read_novel_opening",
    )
    assert DiscoverNovelRankingsTool().access_level == "readonly"
    assert ListRankedNovelsTool().access_level == "readonly"
    assert ReadNovelOpeningTool().access_level == "readonly"


@pytest.mark.asyncio
async def test_market_research_tools_forward_staged_inputs(monkeypatch) -> None:
    discover = AsyncMock(return_value={"rankings": [{"rank_id": "rank-1"}]})
    list_novels = AsyncMock(return_value={"items": [{"rank": 1}]})
    read_opening = AsyncMock(return_value={"book": {"chapters": []}})
    monkeypatch.setattr(
        "app.agent_runtime.tools.impls.market_research.novels.discover_rankings",
        discover,
    )
    monkeypatch.setattr(
        "app.agent_runtime.tools.impls.market_research.novels.list_ranked_novels",
        list_novels,
    )
    monkeypatch.setattr(
        "app.agent_runtime.tools.impls.market_research.novels.read_novel_opening",
        read_opening,
    )

    discovered = json.loads(
        await DiscoverNovelRankingsTool().ainvoke(
            {"site": "fanqie", "query": "都市", "limit": 5}
        )
    )
    listed = json.loads(
        await ListRankedNovelsTool().ainvoke(
            {"site": "fanqie", "rank_id": "rank-1", "limit": 2}
        )
    )
    opened = json.loads(
        await ReadNovelOpeningTool().ainvoke(
            {"site": "fanqie", "source_book_id": "book-1", "chapter_limit": 3}
        )
    )

    assert discovered["rankings"][0]["rank_id"] == "rank-1"
    assert listed["items"][0]["rank"] == 1
    assert opened["book"]["chapters"] == []
    discover.assert_awaited_once_with("fanqie", query="都市", limit=5)
    list_novels.assert_awaited_once_with("fanqie", rank_id="rank-1", limit=2)
    read_opening.assert_awaited_once_with(
        "fanqie",
        source_book_id="book-1",
        chapter_limit=3,
    )
