from __future__ import annotations

import itertools
import json
import re
from typing import Any
from urllib.parse import parse_qsl, urljoin

from selectolax.parser import HTMLParser

from app.novel_research.common import (
    Adapter,
    Book,
    BookMetrics,
    Chapter,
    HarvestError,
    attr,
    canonical_query,
    clean,
    integer,
    non_negative_count,
    text_of,
)


class QidianAdapter(Adapter):
    site = "qidian"
    base = "https://m.qidian.com"
    rank_types = {
        "yuepiao": "月票榜",
        "hotsales": "畅销榜",
        "readindex": "阅读榜",
        "newfans": "书友榜",
        "rec": "推荐榜",
        "update": "更新榜",
        "sign": "签约榜",
        "newbook": "新书榜",
        "newauthor": "新人榜",
    }

    def page_data(self, url: str, stage: str) -> tuple[HTMLParser, dict[str, Any]]:
        tree, _ = self.client.html(
            url,
            stage=stage,
            impersonate="chrome_android",
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 "
                    "Chrome/131 Mobile Safari/537.36"
                )
            },
        )
        node = tree.css_first("#vite-plugin-ssr_pageContext")
        if not node:
            raise HarvestError(f"{stage}: missing page-context JSON")
        try:
            data = json.loads(node.text())["pageContext"]["pageProps"]["pageData"]
        except (KeyError, json.JSONDecodeError) as exc:
            raise HarvestError(f"{stage}: invalid page-context JSON") from exc
        return tree, data

    def rank_url(self, rank_type: str, params: dict[str, str]) -> str:
        path = f"/rank/{rank_type}"
        if "catId" in params:
            path += f"/catid{params['catId']}"
        if "yearmonth" in params:
            path += f"/{params['yearmonth']}"
        if "rankPeriod" in params:
            path += f"/{params['rankPeriod']}"
        return f"{self.base}{path}/"

    def parse_rank_id(self, rank_id: str) -> tuple[str, dict[str, str]]:
        parts = rank_id.split(";")
        rank_type = parts[0]
        if rank_type not in self.rank_types:
            raise HarvestError(f"qidian:rank: unknown rank type: {rank_type}")
        pairs: list[tuple[str, str]] = []
        for part in parts[1:]:
            if "=" not in part:
                raise HarvestError(f"qidian:rank: invalid rank_id: {rank_id}")
            key, value = part.split("=", 1)
            pairs.append((key, value))
        query = canonical_query(
            pairs,
            ("gender", "catId", "yearmonth", "rankPeriod"),
        )
        params = dict(parse_qsl(query))
        if params.get("gender", "male") != "male":
            raise HarvestError("qidian:rank: only the public male channel is supported")
        if any(
            not re.fullmatch(r"-?\d+", value)
            for key, value in params.items()
            if key != "gender"
        ):
            raise HarvestError(f"qidian:rank: invalid rank_id: {rank_id}")
        return rank_type, params

    def ranks(self) -> list[dict[str, Any]]:
        rankings: list[dict[str, Any]] = []
        for rank_type, rank_name in self.rank_types.items():
            _, data = self.page_data(
                f"{self.base}/rank/{rank_type}/",
                f"qidian:ranks:{rank_type}",
            )
            choices: list[list[tuple[str, str, str]]] = []
            for rank_filter in data.get("filters") or []:
                key = rank_filter.get("key")
                if key not in {"catId", "yearmonth", "rankPeriod"}:
                    continue
                choices.append(
                    [
                        (
                            key,
                            str(item["value"]),
                            clean(item.get("text")) or str(item["value"]),
                        )
                        for item in rank_filter.get("items") or []
                    ]
                )
            combinations = itertools.product(*choices) if choices else [()]
            for combination in combinations:
                params = {key: value for key, value, _ in combination}
                rank_id = rank_type + "".join(
                    f";{key}={params[key]}"
                    for key in ("catId", "yearmonth", "rankPeriod")
                    if key in params
                )
                category = next(
                    (
                        (value, name)
                        for key, value, name in combination
                        if key == "catId"
                    ),
                    None,
                )
                period = next(
                    (
                        (value, name)
                        for key, value, name in combination
                        if key in {"yearmonth", "rankPeriod"}
                    ),
                    None,
                )
                suffix = "·".join(item[1] for item in (category, period) if item)
                dimensions: dict[str, Any] = {"gender": {"id": "male", "name": "男频"}}
                if category:
                    dimensions["category"] = {
                        "id": category[0],
                        "name": category[1],
                    }
                if period:
                    dimensions["period"] = {"id": period[0], "name": period[1]}
                rankings.append(
                    {
                        "site": self.site,
                        "rank_id": rank_id,
                        "name": f"{rank_name}·{suffix}" if suffix else rank_name,
                        "rank_type": {"id": rank_type, "name": rank_name},
                        "dimensions": dimensions,
                        "url": self.rank_url(rank_type, params),
                    }
                )
        if not rankings:
            raise HarvestError("qidian:ranks: no ranking identifiers found")
        return rankings

    def book(self, record: dict[str, Any], chapter_limit: int) -> Book:
        book_id = str(record["bid"])
        _, data = self.page_data(f"{self.base}/book/{book_id}/", "qidian:book")
        info = data.get("bookInfo") or {}
        raw_labels = info.get("bookLabels") or []
        labels = [
            clean(item.get("tag")) if isinstance(item, dict) else clean(str(item))
            for item in raw_labels
        ]
        labels = [item for item in labels if item]
        book_tag = info.get("bookTag")
        tag_name = (
            clean(book_tag.get("tagName")) if isinstance(book_tag, dict) else None
        )
        if tag_name and tag_name not in labels:
            labels.append(tag_name)
        categories = [
            item
            for item in (
                clean(info.get("chanName") or record.get("cat")),
                clean(info.get("subCateName") or record.get("subCat")),
            )
            if item
        ]
        raw_status = info.get("bookStatus")
        circle = data.get("seoBookCirclePost") or {}
        source_extra = {
            "rank_count": record.get("rankCnt"),
            "rank_word_count": record.get("cnt"),
            "collect": info.get("collect"),
            "recomAll": info.get("recomAll"),
            "clickTotal": info.get("clickTotal"),
            "bookCirclePostCount": circle.get("bookCirclePostCount"),
        }
        book = Book(
            source_site=self.site,
            source_book_id=book_id,
            title=clean(
                info.get("bookName") or info.get("bName") or record.get("bName")
            )
            or book_id,
            author=clean(info.get("authorName") or record.get("bAuth")),
            categories=categories,
            tags=labels,
            introduction=clean(info.get("desc") or record.get("desc")),
            status=clean(raw_status),
            status_raw=str(raw_status) if raw_status is not None else None,
            cover_url=f"https://bookcover.yuewen.com/qdbimg/349573/{book_id}/600",
            word_count=integer(info.get("wordsCnt")),
            chapter_count=integer(data.get("cTCnt")),
            updated_at=clean(info.get("updTime")),
            official_url=f"https://www.qidian.com/book/{book_id}/",
            source_extra={
                key: value for key, value in source_extra.items() if value is not None
            },
            metrics=BookMetrics(
                reading_count=non_negative_count(info.get("clickTotal")),
                favorite_count=non_negative_count(info.get("collect")),
                recommendation_count=non_negative_count(info.get("recomAll")),
                comment_count=non_negative_count(circle.get("bookCirclePostCount")),
            ),
        )
        if chapter_limit:
            catalog, _ = self.page_data(
                f"{self.base}/book/{book_id}/catalog/",
                "qidian:catalog",
            )
            seen: set[str] = set()
            for anchor in catalog.css("a"):
                href = attr(anchor, "href") or ""
                match = re.search(r"/chapter/\d+/(\d+)/", href)
                label = text_of(anchor) or ""
                classes = attr(anchor, "class") or ""
                if (
                    not match
                    or match.group(1) in seen
                    or "App免费" in label
                    or "_unPay_" in classes
                    or not label.endswith("免费")
                ):
                    continue
                seen.add(match.group(1))
                title = re.sub(r"免费$", "", label).strip()
                url = urljoin(self.base, href)
                content = (
                    self.chapter_content(url, [".content", "main"])
                    if self.chapter_text
                    else None
                )
                if self.chapter_text and content is None:
                    continue
                book.chapters.append(
                    Chapter(
                        source_chapter_id=match.group(1),
                        index=len(book.chapters) + 1,
                        title=title,
                        url=url,
                        content=content,
                    )
                )
                if len(book.chapters) >= chapter_limit:
                    break
        return book

    def read_opening(self, source_book_id: str, chapter_limit: int) -> Book:
        if not re.fullmatch(r"\d+", source_book_id):
            raise HarvestError(f"qidian:book: invalid source_book_id: {source_book_id}")
        return self.book({"bid": source_book_id}, chapter_limit)

    def fetch(
        self,
        rank_id: str,
        limit: int,
        chapters: int = 0,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        rank_type, requested = self.parse_rank_id(rank_id)
        url = self.rank_url(rank_type, requested)
        _, data = self.page_data(url, "qidian:rank")
        records = list(data.get("records") or [])
        if not records:
            raise HarvestError(f"qidian:rank: no records for {rank_id}")
        filters: dict[str, str] = {}
        filter_names: dict[str, str] = {}
        for rank_filter in data.get("filters") or []:
            items = rank_filter.get("items") or []
            selected = int(rank_filter.get("selectedIndex") or 0)
            if items:
                key = str(rank_filter["key"])
                filters[key] = str(items[selected]["value"])
                filter_names[key] = clean(items[selected].get("text")) or str(
                    items[selected]["value"]
                )
        page_num = 2
        while len(records) < limit and not data.get("isLast"):
            csrf = self.client.session.cookies.get("_csrfToken") or ""
            params = {
                "gender": "male",
                "pageNum": page_num,
                **filters,
                "_csrfToken": csrf,
            }
            endpoint = "readIndex" if rank_type == "readindex" else rank_type
            response = self.client.request(
                "GET",
                f"{self.base}/webcommon/rank/{endpoint}list",
                stage="qidian:rank-page",
                params=params,
                headers={"Referer": url},
            )
            try:
                payload = response.json()
            except ValueError as exc:
                raise HarvestError("qidian:rank-page: invalid JSON response") from exc
            if payload.get("code") != 0:
                message = payload.get("msg") or payload.get("message")
                raise HarvestError(
                    f"qidian:rank-page: API code {payload.get('code')}: {message}"
                )
            data = payload.get("data") or {}
            page = data.get("records") or []
            if not page:
                break
            records.extend(page)
            page_num += 1
        items = []
        for index, record in enumerate(records[:limit]):
            rank = integer(record.get("rankNum")) or index + 1
            book = self.book(record, chapters)
            metric = record.get("rankCnt")
            book.metrics.rank_metric = metric
            items.append({"rank": rank, "metric": metric, "book": book.to_dict()})
        dimensions: dict[str, Any] = {"gender": {"id": "male", "name": "男频"}}
        if "catId" in filters:
            dimensions["category"] = {
                "id": filters["catId"],
                "name": filter_names["catId"],
            }
        period_key = (
            "yearmonth"
            if "yearmonth" in filters
            else "rankPeriod"
            if "rankPeriod" in filters
            else None
        )
        if period_key:
            dimensions["period"] = {
                "id": filters[period_key],
                "name": filter_names[period_key],
            }
        ranking = {
            "site": self.site,
            "rank_id": rank_id,
            "name": self.rank_types[rank_type],
            "rank_type": {
                "id": rank_type,
                "name": self.rank_types[rank_type],
            },
            "dimensions": dimensions,
            "url": url,
        }
        return ranking, items
