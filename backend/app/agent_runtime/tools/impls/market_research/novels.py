from __future__ import annotations

import json
from typing import Literal

from pydantic import BaseModel, Field

from app.agent_runtime.tools.base import AgentTool
from app.agent_runtime.tools.errors import ToolExecutionError
from app.agent_runtime.tools.registry import ToolRegistry
from app.novel_research import (
    discover_rankings,
    list_ranked_novels,
    read_novel_opening,
)
from app.novel_research.common import HarvestError

NovelSite = Literal["qidian", "fanqie", "jjwxc", "zongheng"]


def _json_result(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False)


class DiscoverNovelRankingsInput(BaseModel):
    site: NovelSite = Field(description="平台：qidian、fanqie、jjwxc 或 zongheng")
    query: str | None = Field(
        default=None,
        max_length=100,
        description="可选的榜单名、频道、题材、性别或周期关键词",
    )
    limit: int = Field(default=20, ge=1, le=50, description="最多返回的榜单数量")


@ToolRegistry.register
class DiscoverNovelRankingsTool(AgentTool):
    name: str = "discover_novel_rankings"
    description: str = (
        "发现起点、番茄、晋江或纵横当前公开榜单，并按关键词筛选榜单。"
        "先用它取得平台当前有效的完整 rank_id，再查询榜书。"
    )
    access_level: str = "readonly"
    args_schema: type[BaseModel] = DiscoverNovelRankingsInput

    async def _execute(
        self,
        site: NovelSite,
        query: str | None = None,
        limit: int = 20,
    ) -> str:
        try:
            result = await discover_rankings(site, query=query, limit=limit)
        except HarvestError as exc:
            raise ToolExecutionError(str(exc)) from exc
        return _json_result(result)


class ListRankedNovelsInput(BaseModel):
    site: NovelSite = Field(description="平台：qidian、fanqie、jjwxc 或 zongheng")
    rank_id: str = Field(
        min_length=1,
        max_length=300,
        description="discover_novel_rankings 返回的完整 rank_id，必须原样传入",
    )
    limit: int = Field(default=10, ge=1, le=30, description="最多返回的榜书数量")


@ToolRegistry.register
class ListRankedNovelsTool(AgentTool):
    name: str = "list_ranked_novels"
    description: str = (
        "读取指定实时榜单中的作品排名、简介、分类、标签、状态和公开指标。"
        "本工具不读取章节正文；需要研究少量作品开篇时再逐本调用 read_novel_opening。"
    )
    access_level: str = "readonly"
    args_schema: type[BaseModel] = ListRankedNovelsInput

    async def _execute(
        self,
        site: NovelSite,
        rank_id: str,
        limit: int = 10,
    ) -> str:
        try:
            result = await list_ranked_novels(
                site,
                rank_id=rank_id,
                limit=limit,
            )
        except HarvestError as exc:
            raise ToolExecutionError(str(exc)) from exc
        return _json_result(result)


class ReadNovelOpeningInput(BaseModel):
    site: NovelSite = Field(description="平台：qidian、fanqie、jjwxc 或 zongheng")
    source_book_id: str = Field(
        min_length=1,
        max_length=100,
        description="list_ranked_novels 返回的 source_book_id",
    )
    chapter_limit: int = Field(
        default=3,
        ge=1,
        le=3,
        description="读取的匿名公开开篇章节数，最多三章",
    )


@ToolRegistry.register
class ReadNovelOpeningTool(AgentTool):
    name: str = "read_novel_opening"
    description: str = (
        "逐本读取作品元数据和最多前三章匿名公开正文，用于黄金三章分析。"
        "不会读取登录、付费、锁定、App 专属或加密章节，也不会持久化正文。"
    )
    access_level: str = "readonly"
    args_schema: type[BaseModel] = ReadNovelOpeningInput

    async def _execute(
        self,
        site: NovelSite,
        source_book_id: str,
        chapter_limit: int = 3,
    ) -> str:
        try:
            result = await read_novel_opening(
                site,
                source_book_id=source_book_id,
                chapter_limit=chapter_limit,
            )
        except HarvestError as exc:
            raise ToolExecutionError(str(exc)) from exc
        return _json_result(result)
