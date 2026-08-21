from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, parse_qsl, urlencode, urljoin, urlparse

from app.novel_research.common import (
    Adapter,
    Book,
    Chapter,
    HarvestError,
    attr,
    canonical_query,
    clean,
    integer,
    parse_rank_query,
    text_of,
)


class JjwxcAdapter(Adapter):
    site = "jjwxc"
    base = "https://www.jjwxc.net/"

    def get(self, url: str, stage: str):
        return self.client.html(url, stage=stage, encoding="gb18030")

    def ranks(self) -> list[dict[str, Any]]:
        tree, _ = self.get(urljoin(self.base, "topten.php"), "jjwxc:ranks")
        found: dict[str, dict[str, Any]] = {}
        for anchor in tree.css("a"):
            href = attr(anchor, "href") or ""
            parsed = urlparse(urljoin(self.base, href))
            pairs = parse_qsl(parsed.query, keep_blank_values=True)
            if (
                parsed.netloc != "www.jjwxc.net"
                or parsed.path != "/topten.php"
                or not any(key == "orderstr" for key, _ in pairs)
            ):
                continue
            try:
                rank_id = canonical_query(pairs, ("orderstr", "t", "timeid"))
            except HarvestError:
                continue
            values = dict(parse_qsl(rank_id))
            dimensions: dict[str, Any] = {}
            if "t" in values:
                dimensions["channel"] = {
                    "id": values["t"],
                    "name": {"0": "言情", "1": "纯爱衍生"}.get(
                        values["t"],
                        values["t"],
                    ),
                }
            if "timeid" in values:
                dimensions["period"] = {
                    "id": values["timeid"],
                    "name": text_of(anchor),
                }
            name = text_of(anchor) or rank_id
            found[rank_id] = {
                "site": self.site,
                "rank_id": rank_id,
                "name": name,
                "rank_type": {"id": values["orderstr"], "name": name},
                "dimensions": dimensions,
                "url": f"{self.base}topten.php?{rank_id}",
            }
        if not found:
            raise HarvestError("jjwxc:ranks: no ranking identifiers found")
        return list(found.values())

    def book(self, book_id: str, chapter_limit: int) -> Book:
        if not re.fullmatch(r"\d+", book_id):
            raise HarvestError(f"jjwxc:book: invalid source_book_id: {book_id}")
        url = urljoin(self.base, f"onebook.php?novelid={book_id}")
        tree, _ = self.get(url, "jjwxc:book")
        title = text_of(tree.css_first("h1"))
        if not title:
            raise HarvestError(f"jjwxc:book: missing title for {book_id}")
        description_meta = tree.css_first('meta[name="Description"]') or tree.css_first(
            'meta[name="description"]'
        )
        read_bodies = tree.css(".smallreadbody")
        description = (text_of(read_bodies[0]) if read_bodies else None) or attr(
            description_meta, "content"
        )
        author_text = text_of(tree.css_first("h2"))
        author = clean(re.sub(r"^.*?作者[：:]", "", author_text or ""))
        genre = text_of(tree.css_first('[itemprop="genre"]'))
        categories = [
            item for item in (clean(part) for part in (genre or "").split("-")) if item
        ]
        tag_block = read_bodies[-1] if read_bodies else None
        tags = (
            [text_of(anchor) for anchor in tag_block.css('a[href*="bookbase.php?bq="]')]
            if tag_block
            else []
        )
        tags = [tag for tag in tags if tag]
        status = text_of(tree.css_first('[itemprop="updataStatus"]'))
        image = tree.css_first('[itemprop="image"]')
        cover = attr(image, "src") or attr(image, "_src")
        metadata_text = attr(description_meta, "content") or ""
        updated_match = re.search(r"最新更新:([^|]+)", metadata_text)
        updated = updated_match.group(1) if updated_match else None
        book = Book(
            source_site=self.site,
            source_book_id=book_id,
            title=title,
            author=author,
            categories=categories,
            tags=tags,
            introduction=description,
            status=status,
            status_raw=status,
            cover_url=cover,
            word_count=integer(text_of(tree.css_first('[itemprop="wordCount"]'))),
            updated_at=clean(updated),
            official_url=url,
        )
        if not chapter_limit:
            return book
        candidates: list[tuple[str, str, str]] = []
        for anchor in tree.css("a"):
            href = attr(anchor, "href") or ""
            query = parse_qs(urlparse(href).query)
            if (
                query.get("novelid") == [book_id]
                and "chapterid" in query
                and text_of(anchor)
            ):
                candidates.append(
                    (
                        query["chapterid"][0],
                        text_of(anchor) or "",
                        urljoin(self.base, href),
                    )
                )
        book.chapter_count = len({chapter_id for chapter_id, _, _ in candidates})
        seen: set[str] = set()
        for chapter_id, label, chapter_url in candidates:
            if chapter_id in seen:
                continue
            seen.add(chapter_id)
            content = (
                self.chapter_content(
                    chapter_url,
                    [".noveltext", "#content", "div.noveltext"],
                    encoding="gb18030",
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
            if len(book.chapters) >= chapter_limit:
                break
        return book

    def read_opening(self, source_book_id: str, chapter_limit: int) -> Book:
        return self.book(source_book_id, chapter_limit)

    def fetch(
        self,
        rank_id: str,
        limit: int,
        chapters: int = 0,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        params = parse_rank_query(
            rank_id,
            ("orderstr", "t", "timeid"),
            ("orderstr",),
        )
        ordered_pairs = [
            (key, params[key]) for key in ("orderstr", "t", "timeid") if key in params
        ]
        url = urljoin(self.base, f"topten.php?{urlencode(ordered_pairs)}")
        tree, _ = self.get(url, "jjwxc:rank")
        entries: list[tuple[str, int | None]] = []
        for row in tree.css("tr"):
            anchor = row.css_first('a[href*="onebook.php?novelid="]')
            if not anchor:
                continue
            query = parse_qs(urlparse(attr(anchor, "href") or "").query)
            book_id = (query.get("novelid") or [None])[0]
            cells = row.css("td")
            if book_id:
                entries.append((book_id, integer(text_of(cells[0])) if cells else None))
        if not entries:
            raise HarvestError(f"jjwxc:rank: no records for {rank_id}")
        items = []
        for index, (book_id, position) in enumerate(entries[:limit]):
            rank = position or index + 1
            book = self.book(book_id, chapters)
            items.append({"rank": rank, "metric": None, "book": book.to_dict()})
        ranking = {
            "site": self.site,
            "rank_id": rank_id,
            "name": rank_id,
            "url": url,
        }
        return ranking, items
