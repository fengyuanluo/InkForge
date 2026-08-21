from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin

from app.novel_research.common import (
    Adapter,
    Book,
    BookMetrics,
    Chapter,
    HarvestError,
    attr,
    count_value,
    first,
    non_negative_count,
    text_of,
)


class FanqieAdapter(Adapter):
    site = "fanqie"
    base = "https://fanqienovel.com"
    gender_names = {"1": "男频", "0": "女频"}
    rank_type_names = {"1": "新书榜", "2": "阅读榜"}

    @staticmethod
    def page_state(source: str) -> dict[str, Any]:
        marker = "window.__INITIAL_STATE__="
        try:
            start = source.index(marker) + len(marker)
            state, _ = json.JSONDecoder().raw_decode(source[start:])
        except (ValueError, json.JSONDecodeError):
            return {}
        page = state.get("page") if isinstance(state, dict) else None
        return page if isinstance(page, dict) else {}

    def ranks(self) -> list[dict[str, Any]]:
        tree, response = self.client.html(
            f"{self.base}/rank/all",
            stage="fanqie:ranks",
        )
        state_match = re.search(
            r'"rankCategoryTypeList":(\{.*?\}),"defaultPage"',
            response.text,
        )
        categories = (
            json.loads(state_match.group(1))
            if state_match
            else {"male": [], "female": []}
        )
        category_names = {
            ("1" if gender == "male" else "0", str(item["id"])): item["name"]
            for gender, items in categories.items()
            for item in items
        }
        found: dict[str, dict[str, Any]] = {}
        for anchor in tree.css("a"):
            href = attr(anchor, "href") or ""
            match = re.fullmatch(r"/rank/([01]_[12]_\d+)", href)
            if not match:
                continue
            rank_id = match.group(1)
            gender, rank_type, category = rank_id.split("_")
            category_name = category_names.get(
                (gender, category),
                text_of(anchor) or category,
            )
            found[rank_id] = {
                "site": self.site,
                "rank_id": rank_id,
                "name": (
                    f"{self.gender_names[gender]}·"
                    f"{self.rank_type_names[rank_type]}·{category_name}"
                ),
                "rank_type": {
                    "id": rank_type,
                    "name": self.rank_type_names[rank_type],
                },
                "dimensions": {
                    "gender": {
                        "id": gender,
                        "name": self.gender_names[gender],
                    },
                    "category": {"id": category, "name": category_name},
                },
                "url": urljoin(self.base, href),
            }
        if not found:
            raise HarvestError("fanqie:ranks: no ranking identifiers found")
        return list(found.values())

    def book(self, book_id: str, chapter_limit: int) -> Book:
        if not re.fullmatch(r"\d+", book_id):
            raise HarvestError(f"fanqie:book: invalid source_book_id: {book_id}")
        url = f"{self.base}/page/{book_id}"
        tree, response = self.client.html(url, stage="fanqie:book")
        page = self.page_state(response.text)
        title = text_of(first(tree, [".info-name", "h1"])) or page.get("bookName")
        if not title:
            raise HarvestError(f"fanqie:book: missing title for {book_id}")
        labels = [
            text_of(node)
            for node in tree.css(
                ".info-label-grey, .page-tags span, .info-category span"
            )
        ]
        labels = [label for label in labels if label]
        status = text_of(
            first(tree, [".info-label-yellow", ".info-status", ".page-status"])
        )
        cover = attr(
            first(tree, [".page-cover-img", ".book-cover-img", ".info-pic img"]),
            "src",
        )
        if cover and cover.startswith("//"):
            cover = "https:" + cover
        cover = cover or page.get("thumbUrl")
        page_word_count = non_negative_count(page.get("wordNumber"))
        page_chapter_count = non_negative_count(page.get("chapterTotal"))
        book = Book(
            source_site=self.site,
            source_book_id=book_id,
            title=title,
            author=text_of(first(tree, [".author-name", ".info-author"]))
            or page.get("authorName"),
            categories=labels[:1],
            tags=labels[1:],
            introduction=text_of(first(tree, [".page-abstract-content", ".abstract"]))
            or page.get("abstract"),
            status=status,
            status_raw=status,
            cover_url=cover,
            word_count=(
                page_word_count
                if page_word_count is not None
                else count_value(text_of(tree.css_first(".info-count-word")))
            ),
            chapter_count=page_chapter_count,
            updated_at=text_of(tree.css_first(".info-last-time")),
            official_url=url,
            metrics=BookMetrics(
                reading_count=non_negative_count(page.get("readCount")),
            ),
            source_extra={
                key: page[key]
                for key in ("readCount", "wordNumber", "chapterTotal")
                if page.get(key) is not None
            },
        )
        links: list[tuple[str, str]] = []
        for anchor in tree.css("a.chapter-item-title"):
            href = attr(anchor, "href") or ""
            match = re.search(r"/reader/(\d+)", href)
            label = text_of(anchor) or ""
            if match and not label.startswith("最近更新"):
                links.append((match.group(1), label))
        if book.chapter_count is None:
            book.chapter_count = len(links)
        for chapter_id, label in links[:chapter_limit]:
            chapter_url = f"{self.base}/reader/{chapter_id}"
            content = (
                self.chapter_content(
                    chapter_url,
                    [".muye-reader-content", ".reader-content", "article"],
                )
                if self.chapter_text
                else None
            )
            if self.chapter_text and content is None:
                continue
            book.chapters.append(
                Chapter(
                    source_chapter_id=chapter_id,
                    index=len(book.chapters) + 1,
                    title=label,
                    url=chapter_url,
                    content=content,
                )
            )
        return book

    def read_opening(self, source_book_id: str, chapter_limit: int) -> Book:
        return self.book(source_book_id, chapter_limit)

    def fetch(
        self,
        rank_id: str,
        limit: int,
        chapters: int = 0,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        if not re.fullmatch(r"[01]_[12]_\d+", rank_id):
            raise HarvestError(f"fanqie:rank: invalid rank_id: {rank_id}")
        url = f"{self.base}/rank/{rank_id}"
        entries: list[tuple[str, int]] = []
        seen: set[str] = set()
        offset = 0
        category_name = rank_id.split("_")[2]
        while len(entries) < limit:
            page_url = url if offset == 0 else f"{url}?{urlencode({'offset': offset})}"
            tree, response = self.client.html(page_url, stage="fanqie:rank")
            if offset == 0:
                state_match = re.search(
                    r'"rankCategoryTypeList":(\{.*?\}),"defaultPage"',
                    response.text,
                )
                if state_match:
                    categories = json.loads(state_match.group(1))
                    gender_key = "male" if rank_id.startswith("1_") else "female"
                    category_name = next(
                        (
                            item["name"]
                            for item in categories.get(gender_key, [])
                            if str(item["id"]) == category_name
                        ),
                        category_name,
                    )
            page: list[tuple[str, int]] = []
            for node in tree.css(".rank-book-item"):
                anchor = node.css_first('a[href^="/page/"]')
                href = attr(anchor, "href") or ""
                match = re.search(r"/page/(\d+)", href)
                if match and match.group(1) not in seen:
                    seen.add(match.group(1))
                    page.append((match.group(1), offset + len(page) + 1))
            if not page:
                break
            entries.extend(page)
            offset += len(page)
        if not entries:
            raise HarvestError(f"fanqie:rank: no records for {rank_id}")
        items = []
        for book_id, position in entries[:limit]:
            book = self.book(book_id, chapters)
            items.append({"rank": position, "metric": None, "book": book.to_dict()})
        gender, rank_type, category = rank_id.split("_")
        gender_name = self.gender_names[gender]
        rank_type_name = self.rank_type_names[rank_type]
        ranking = {
            "site": self.site,
            "rank_id": rank_id,
            "name": f"{gender_name}·{rank_type_name}·{category_name}",
            "rank_type": {"id": rank_type, "name": rank_type_name},
            "dimensions": {
                "gender": {"id": gender, "name": gender_name},
                "category": {"id": category, "name": category_name},
            },
            "url": url,
        }
        return ranking, items
