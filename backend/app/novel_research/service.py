from __future__ import annotations

import asyncio
import copy
import json
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal, TypeAlias

from app.novel_research.adapters import ADAPTERS
from app.novel_research.common import Adapter, Client, HarvestError

NovelSite: TypeAlias = Literal["qidian", "fanqie", "jjwxc", "zongheng"]
SUPPORTED_SITES: tuple[str, ...] = tuple(ADAPTERS)
RANKING_CACHE_TTL_SECONDS = 600.0


@dataclass(frozen=True)
class _RankingCacheEntry:
    expires_at: float
    fetched_at: str
    rankings: tuple[dict[str, Any], ...]


_ranking_cache: dict[str, _RankingCacheEntry] = {}
_ranking_locks: dict[str, asyncio.Lock] = {}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _create_adapter(site: str, *, chapter_text: bool) -> tuple[Adapter, Client]:
    adapter_type = ADAPTERS.get(site)
    if adapter_type is None:
        raise HarvestError(
            f"site: unsupported site {site!r}; expected one of {', '.join(SUPPORTED_SITES)}"
        )
    client = Client()
    return adapter_type(client, chapter_text=chapter_text), client


def _load_rankings(site: str) -> tuple[str, list[dict[str, Any]]]:
    adapter, client = _create_adapter(site, chapter_text=False)
    try:
        try:
            rankings = adapter.ranks()
        except HarvestError:
            raise
        except Exception as exc:
            raise HarvestError(f"{site}:ranks: parser failed: {exc}") from exc
    finally:
        client.close()
    if not rankings:
        raise HarvestError(f"{site}:ranks: no ranking identifiers found")
    return _now_iso(), rankings


def _load_ranked_novels(
    site: str,
    rank_id: str,
    limit: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    adapter, client = _create_adapter(site, chapter_text=False)
    try:
        try:
            return adapter.fetch(rank_id, limit, chapters=0)
        except HarvestError:
            raise
        except Exception as exc:
            raise HarvestError(f"{site}:rank: parser failed: {exc}") from exc
    finally:
        client.close()


def _load_opening(
    site: str,
    source_book_id: str,
    chapter_limit: int,
) -> dict[str, Any]:
    adapter, client = _create_adapter(site, chapter_text=True)
    try:
        try:
            return adapter.read_opening(source_book_id, chapter_limit).to_dict()
        except HarvestError:
            raise
        except Exception as exc:
            raise HarvestError(f"{site}:book: parser failed: {exc}") from exc
    finally:
        client.close()


def _ranking_search_text(ranking: dict[str, Any]) -> str:
    searchable = {
        "rank_id": ranking.get("rank_id"),
        "name": ranking.get("name"),
        "rank_type": ranking.get("rank_type"),
        "dimensions": ranking.get("dimensions"),
    }
    return json.dumps(searchable, ensure_ascii=False).casefold()


async def _get_cached_rankings(site: str) -> tuple[str, list[dict[str, Any]]]:
    if site not in ADAPTERS:
        _create_adapter(site, chapter_text=False)
    now = time.monotonic()
    cached = _ranking_cache.get(site)
    if cached and cached.expires_at > now:
        return cached.fetched_at, copy.deepcopy(list(cached.rankings))

    lock = _ranking_locks.setdefault(site, asyncio.Lock())
    async with lock:
        now = time.monotonic()
        cached = _ranking_cache.get(site)
        if cached and cached.expires_at > now:
            return cached.fetched_at, copy.deepcopy(list(cached.rankings))
        fetched_at, rankings = await asyncio.to_thread(_load_rankings, site)
        _ranking_cache[site] = _RankingCacheEntry(
            expires_at=time.monotonic() + RANKING_CACHE_TTL_SECONDS,
            fetched_at=fetched_at,
            rankings=tuple(copy.deepcopy(rankings)),
        )
        return fetched_at, rankings


async def discover_rankings(
    site: NovelSite,
    *,
    query: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    fetched_at, rankings = await _get_cached_rankings(site)
    normalized_query = query.strip().casefold() if query else ""
    if normalized_query:
        rankings = [
            ranking
            for ranking in rankings
            if normalized_query in _ranking_search_text(ranking)
        ]
    total_matches = len(rankings)
    return {
        "site": site,
        "fetched_at": fetched_at,
        "query": query.strip() if query else None,
        "total_matches": total_matches,
        "rankings": rankings[:limit],
    }


async def list_ranked_novels(
    site: NovelSite,
    *,
    rank_id: str,
    limit: int,
) -> dict[str, Any]:
    ranking, items = await asyncio.to_thread(
        _load_ranked_novels,
        site,
        rank_id,
        limit,
    )
    return {
        "ranking": {**ranking, "fetched_at": _now_iso()},
        "items": items,
    }


async def read_novel_opening(
    site: NovelSite,
    *,
    source_book_id: str,
    chapter_limit: int = 3,
) -> dict[str, Any]:
    book = await asyncio.to_thread(
        _load_opening,
        site,
        source_book_id,
        chapter_limit,
    )
    return {"fetched_at": _now_iso(), "book": book}


def clear_ranking_cache() -> None:
    """Clear the process-local ranking cache for deterministic tests."""

    _ranking_cache.clear()
