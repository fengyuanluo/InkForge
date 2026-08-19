from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

from app.novel_research.common import (
    Adapter,
    Book,
    Chapter,
    HarvestError,
    attr,
    canonical_query,
    clean,
    first,
    integer,
    parse_rank_query,
    text_of,
)


class ZonghengAdapter(Adapter):
    site = "zongheng"
    base = "https://www.zongheng.com"

    def ranks(self) -> list[dict[str, Any]]:
        tree, _ = self.client.html(f"{self.base}/rank", stage="zongheng:ranks")
        found: dict[str, dict[str, Any]] = {}
        for anchor in tree.css("a"):
            href = attr(anchor, "href") or ""
            query = parse_qs(urlparse(href).query)
            if "rankType" not in query:
                continue
            rank_type = query["rankType"][0]
            response = self.client.request(
                "POST",
                f"{self.base}/api/rank/details",
                stage="zongheng:ranks",
                data={
                    "cateFineId": 0,
                    "cateType": 0,
                    "pageNum": 1,
                    "pageSize": 1,
                    "period": 0,
                    "rankNo": "",
                    "rankType": rank_type,
                },
                headers={"Referer": urljoin(self.base, href)},
            )
            try:
                result = response.json()["result"]
            except (ValueError, KeyError, TypeError) as exc:
                raise HarvestError("zongheng:ranks: invalid JSON response") from exc
            rank_name = clean(result.get("title")) or text_of(anchor) or rank_type
            categories = [
                {"cateFineId": 0, "cateFineName": "全部"},
                *(result.get("cateList") or []),
            ]
            for category in categories:
                category_id = str(category["cateFineId"])
                raw_category_name = category.get("cateFineName")
                category_name = (
                    clean(str(raw_category_name))
                    if raw_category_name is not None
                    else None
                ) or category_id
                rank_id = canonical_query(
                    [("rankType", rank_type), ("cateFineId", category_id)],
                    ("rankType", "cateFineId"),
                )
                found[rank_id] = {
                    "site": self.site,
                    "rank_id": rank_id,
                    "name": f"{rank_name}·{category_name}",
                    "rank_type": {"id": rank_type, "name": rank_name},
                    "dimensions": {
                        "category": {
                            "id": category_id,
                            "name": category_name,
                        }
                    },
                    "url": f"{self.base}/rank?{rank_id}",
                }
        if not found:
            raise HarvestError("zongheng:ranks: no ranking identifiers found")
        return list(found.values())

    def chapter_chain(self, first_url: str, limit: int) -> list[Chapter]:
        chapters: list[Chapter] = []
        url = first_url
        seen: set[str] = set()
        while url and len(chapters) < limit and url not in seen:
            seen.add(url)
            tree, response = self.client.html(url, stage="zongheng:chapter")
            if "/captcha" in str(response.url):
                raise HarvestError(
                    "zongheng:chapter: anonymous reader was redirected to CAPTCHA"
                )
            content = text_of(
                first(tree, [".content", ".reader-box .content", ".chapter-content"])
            )
            if (
                not content
                or len(content) < 80
                or re.search(r"订阅|购买本章|登录后阅读", content)
            ):
                break
            title = (
                text_of(first(tree, ["h1", ".title_txtbox", ".chapter-title"]))
                or f"chapter {len(chapters) + 1}"
            )
            chapter_match = re.search(r"/(\d+)\.html", str(response.url))
            chapter_id = (
                chapter_match.group(1) if chapter_match else str(len(chapters) + 1)
            )
            chapters.append(
                Chapter(
                    source_chapter_id=chapter_id,
                    index=len(chapters) + 1,
                    title=title,
                    url=str(response.url),
                    content=content if self.chapter_text else None,
                )
            )
            next_anchor = first(
                tree,
                ['a[rel="next"]', "a.nextchapter", "a.next"],
            )
            if not next_anchor:
                next_anchor = next(
                    (
                        anchor
                        for anchor in tree.css("a")
                        if (text_of(anchor) or "").strip() == "下一章"
                    ),
                    None,
                )
            next_href = attr(next_anchor, "href")
            url = urljoin(str(response.url), next_href) if next_href else ""
        return chapters

    def book(self, record: dict[str, Any], chapter_limit: int) -> Book:
        book_id = str(record.get("bookId"))
        if not re.fullmatch(r"\d+", book_id):
            raise HarvestError(f"zongheng:book: invalid source_book_id: {book_id}")
        url = f"{self.base}/detail/{book_id}"
        tree, _ = self.client.html(url, stage="zongheng:book")
        title = clean(record.get("bookName")) or text_of(tree.css_first("h1"))
        if not title:
            page_title = text_of(tree.css_first("title"))
            title = (clean(page_title.split("-")[0]) if page_title else None) or book_id
        cover = record.get("bookCover") or record.get("imageUrl")
        if not cover:
            cover = attr(tree.css_first(".book-img img"), "src")
        tag_nodes = tree.css(".book-info--tags span")
        categories = [
            item
            for item in (
                clean(record.get("cateFineName")),
                text_of(tree.css_first(".book-info--tags .cateFineId")),
            )
            if item
        ]
        categories = list(dict.fromkeys(categories))
        tags = [
            text_of(node)
            for node in tag_nodes
            if not set((attr(node, "class") or "").split())
            & {"vip", "serialStatus", "cateFineId"}
        ]
        tags = [tag for tag in tags if tag]
        status = text_of(tree.css_first(".book-info--tags .serialStatus"))
        author = clean(record.get("pseudonym") or record.get("authorName"))
        if not author:
            author = text_of(
                tree.css_first(".book-info--author") or tree.css_first(".au-name")
            )
        introduction = clean(record.get("description")) or text_of(
            tree.css_first(".book-dec") or tree.css_first(".book-info--intro")
        )
        raw_status = record.get("serialStatus")
        book = Book(
            source_site=self.site,
            source_book_id=book_id,
            title=title,
            author=author,
            categories=categories,
            tags=tags,
            introduction=introduction,
            status=status or (str(raw_status) if raw_status is not None else None),
            status_raw=str(raw_status) if raw_status is not None else None,
            cover_url=cover,
            word_count=integer(record.get("totalWords")),
            official_url=url,
            source_extra={
                key: record.get(key)
                for key in ("number", "reward", "orderNo")
                if record.get(key) is not None
            },
        )
        if chapter_limit:
            read_anchor = first(
                tree,
                [
                    "a.book-info--btn-reading",
                    'a[href*="read.zongheng.com/chapter/"]',
                ],
            )
            href = attr(read_anchor, "href")
            if href:
                book.chapters = self.chapter_chain(
                    urljoin(url, href),
                    chapter_limit,
                )
        return book

    def read_opening(self, source_book_id: str, chapter_limit: int) -> Book:
        return self.book({"bookId": source_book_id}, chapter_limit)

    def fetch(
        self,
        rank_id: str,
        limit: int,
        chapters: int = 0,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        params = parse_rank_query(
            rank_id,
            ("rankType", "cateFineId"),
            ("rankType", "cateFineId"),
        )
        if not all(re.fullmatch(r"\d+", value) for value in params.values()):
            raise HarvestError(f"zongheng:rank: invalid rank_id: {rank_id}")
        records: list[dict[str, Any]] = []
        page_num = 1
        page_size = min(limit, 100)
        result: dict[str, Any] = {}
        while len(records) < limit:
            data = {
                "cateFineId": params["cateFineId"],
                "cateType": 0,
                "pageNum": page_num,
                "pageSize": page_size,
                "period": 0,
                "rankNo": "",
                "rankType": params["rankType"],
            }
            response = self.client.request(
                "POST",
                f"{self.base}/api/rank/details",
                stage="zongheng:rank",
                data=data,
                headers={"Referer": f"{self.base}/rank?{rank_id}"},
            )
            try:
                payload = response.json()
                result = payload["result"]
                page = result["resultList"]
            except (ValueError, KeyError, TypeError) as exc:
                raise HarvestError("zongheng:rank: invalid JSON response") from exc
            if not page:
                break
            records.extend(page)
            if len(page) < page_size:
                break
            page_num += 1
        if not records:
            raise HarvestError(f"zongheng:rank: no records for {rank_id}")
        items = [
            {
                "rank": integer(record.get("orderNo")) or index + 1,
                "metric": record.get("number"),
                "book": self.book(record, chapters).to_dict(),
            }
            for index, record in enumerate(records[:limit])
        ]
        category_name = next(
            (
                clean(item.get("cateFineName"))
                for item in result.get("cateList") or []
                if str(item.get("cateFineId")) == params["cateFineId"]
            ),
            None,
        ) or ("全部" if params["cateFineId"] == "0" else params["cateFineId"])
        rank_name = clean(result.get("title")) or rank_id
        ranking = {
            "site": self.site,
            "rank_id": rank_id,
            "name": rank_name,
            "rank_type": {"id": params["rankType"], "name": rank_name},
            "dimensions": {
                "category": {
                    "id": params["cateFineId"],
                    "name": category_name,
                }
            },
            "url": f"{self.base}/rank?{rank_id}",
        }
        return ranking, items
