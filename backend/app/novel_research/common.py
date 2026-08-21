from __future__ import annotations

import html
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Literal
from urllib.parse import parse_qsl, urlencode

from curl_cffi import requests
from selectolax.parser import HTMLParser, Node


class HarvestError(RuntimeError):
    """A public site request or parser failed at a named collection stage."""


def clean(text: str | None) -> str | None:
    if text is None:
        return None
    value = re.sub(r"[ \t\r\f\v]+", " ", html.unescape(text))
    value = re.sub(r"\n\s*\n+", "\n", value).strip()
    return value or None


def integer(value: Any) -> int | None:
    if value in (None, ""):
        return None
    match = re.search(r"[\d,]+", str(value))
    return int(match.group().replace(",", "")) if match else None


def count_value(value: Any) -> int | None:
    if value in (None, ""):
        return None
    match = re.search(r"([\d.]+)\s*([万亿]?)", str(value))
    if not match:
        return None
    multiplier = {"": 1, "万": 10_000, "亿": 100_000_000}[match.group(2)]
    return round(float(match.group(1)) * multiplier)


def non_negative_count(value: Any) -> int | None:
    if value in (None, ""):
        return None
    normalized = str(value).strip()
    if normalized.startswith("-"):
        return None
    return count_value(normalized)


def text_of(node: Node | None) -> str | None:
    return clean(node.text(separator="\n")) if node else None


def attr(node: Node | None, name: str) -> str | None:
    return node.attributes.get(name) if node else None


def first(tree: HTMLParser | Node, selectors: list[str]) -> Node | None:
    for selector in selectors:
        node = tree.css_first(selector)
        if node:
            return node
    return None


def canonical_query(pairs: list[tuple[str, str]], allowed: tuple[str, ...]) -> str:
    values: dict[str, str] = {}
    for key, value in pairs:
        if key not in allowed or key in values or not re.fullmatch(r"[\w-]+", value):
            raise HarvestError(f"invalid ranking parameter: {key}={value}")
        values[key] = value
    return urlencode([(key, values[key]) for key in allowed if key in values])


def parse_rank_query(
    rank_id: str,
    allowed: tuple[str, ...],
    required: tuple[str, ...],
) -> dict[str, str]:
    try:
        canonical = canonical_query(parse_qsl(rank_id, keep_blank_values=True), allowed)
    except ValueError as exc:
        raise HarvestError(f"invalid rank_id: {rank_id}") from exc
    values = dict(parse_qsl(canonical))
    if any(key not in values for key in required):
        raise HarvestError(f"rank_id requires: {', '.join(required)}")
    return values


@dataclass
class Chapter:
    source_chapter_id: str
    index: int
    title: str
    url: str
    public: bool = True
    content: str | None = None


@dataclass
class BookMetrics:
    reading_count: int | None = None
    favorite_count: int | None = None
    recommendation_count: int | None = None
    comment_count: int | None = None
    rating: int | float | str | None = None
    hot_score: int | float | str | None = None
    rank_metric: int | float | str | None = None


@dataclass
class Book:
    source_site: str
    source_book_id: str
    title: str
    author: str | None = None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    introduction: str | None = None
    status: str | None = None
    status_raw: str | None = None
    cover_url: str | None = None
    word_count: int | None = None
    chapter_count: int | None = None
    updated_at: str | None = None
    official_url: str | None = None
    chapters: list[Chapter] = field(default_factory=list)
    metrics: BookMetrics = field(default_factory=BookMetrics)
    source_extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Client:
    def __init__(self, delay: float = 0.35, timeout: float = 30.0):
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session(impersonate="chrome")
        self.last_request = 0.0

    def close(self) -> None:
        self.session.close()

    def request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        *,
        stage: str,
        **kwargs: Any,
    ):
        wait = self.delay - (time.monotonic() - self.last_request)
        if wait > 0:
            time.sleep(wait)
        try:
            response = self.session.request(
                method,
                url,
                timeout=self.timeout,
                **kwargs,
            )
        except Exception as exc:
            raise HarvestError(f"{stage}: request failed: {exc}") from exc
        finally:
            self.last_request = time.monotonic()
        if response.status_code == 429:
            raise HarvestError(f"{stage}: HTTP 429; retry later")
        if response.status_code >= 400:
            raise HarvestError(f"{stage}: HTTP {response.status_code} for {url}")
        return response

    def html(
        self,
        url: str,
        *,
        stage: str,
        encoding: str | None = None,
        **kwargs: Any,
    ) -> tuple[HTMLParser, Any]:
        response = self.request("GET", url, stage=stage, **kwargs)
        source = (
            response.content.decode(encoding, "replace") if encoding else response.text
        )
        return HTMLParser(source), response


class Adapter:
    site = ""

    def __init__(self, client: Client, chapter_text: bool = False):
        self.client = client
        self.chapter_text = chapter_text

    def ranks(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def fetch(
        self,
        rank_id: str,
        limit: int,
        chapters: int = 0,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        raise NotImplementedError

    def read_opening(self, source_book_id: str, chapter_limit: int) -> Book:
        raise NotImplementedError

    def chapter_content(
        self,
        url: str,
        selectors: list[str],
        *,
        encoding: str | None = None,
    ) -> str | None:
        tree, _ = self.client.html(
            url,
            stage=f"{self.site}:chapter",
            encoding=encoding,
        )
        node = first(tree, selectors)
        content = text_of(node)
        if (
            not content
            or len(content) < 80
            or re.search(r"订阅|购买本章|登录后阅读|VIP章节", content)
        ):
            return None
        return content
