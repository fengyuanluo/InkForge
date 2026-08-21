from __future__ import annotations

import json
from collections import deque
from typing import Any

import pytest
from selectolax.parser import HTMLParser

from app.novel_research.adapters.fanqie import FanqieAdapter
from app.novel_research.adapters.jjwxc import JjwxcAdapter
from app.novel_research.adapters.qidian import QidianAdapter
from app.novel_research.adapters.zongheng import ZonghengAdapter


class FixtureResponse:
    def __init__(
        self,
        text: str = "",
        *,
        url: str = "https://fixture.invalid/",
        payload: dict[str, Any] | None = None,
    ) -> None:
        self.text = text
        self.content = text.encode()
        self.url = url
        self.status_code = 200
        self._payload = payload

    def json(self) -> dict[str, Any]:
        if self._payload is None:
            raise ValueError("fixture has no JSON payload")
        return self._payload


class FixtureClient:
    def __init__(
        self,
        *,
        html: dict[str, list[FixtureResponse]] | None = None,
        requests: dict[str, list[FixtureResponse]] | None = None,
    ) -> None:
        self.html_routes = {key: deque(values) for key, values in (html or {}).items()}
        self.request_routes = {
            key: deque(values) for key, values in (requests or {}).items()
        }

    @staticmethod
    def _take(
        routes: dict[str, deque[FixtureResponse]],
        stage: str,
    ) -> FixtureResponse:
        route = routes.get(stage)
        if not route:
            raise AssertionError(f"unexpected fixture stage: {stage}")
        return route.popleft()

    def html(self, _url: str, *, stage: str, **_kwargs):
        response = self._take(self.html_routes, stage)
        return HTMLParser(response.text), response

    def request(self, _method: str, _url: str, *, stage: str, **_kwargs):
        return self._take(self.request_routes, stage)


def _qidian_page(data: dict[str, Any]) -> FixtureResponse:
    payload = {"pageContext": {"pageProps": {"pageData": data}}}
    return FixtureResponse(
        '<script id="vite-plugin-ssr_pageContext">'
        f"{json.dumps(payload, ensure_ascii=False)}"
        "</script>"
    )


def test_qidian_discovers_live_rank_dimensions_from_page_data() -> None:
    rank_data = {
        "filters": [
            {
                "key": "catId",
                "items": [{"value": "21", "text": "玄幻"}],
            }
        ]
    }
    client = FixtureClient(
        html={
            f"qidian:ranks:{rank_type}": [_qidian_page(rank_data)]
            for rank_type in QidianAdapter.rank_types
        }
    )

    rankings = QidianAdapter(client).ranks()

    assert len(rankings) == len(QidianAdapter.rank_types)
    assert rankings[0]["rank_id"].endswith(";catId=21")
    assert rankings[0]["dimensions"]["category"]["name"] == "玄幻"


def test_fanqie_discovers_rank_ids_from_public_links() -> None:
    html = """
    <script>{"rankCategoryTypeList":{"male":[{"id":1141,"name":"都市"}],"female":[]},"defaultPage":1}</script>
    <a href="/rank/1_1_1141">都市新书榜</a>
    """
    client = FixtureClient(html={"fanqie:ranks": [FixtureResponse(html)]})

    rankings = FanqieAdapter(client).ranks()

    assert rankings == [
        {
            "site": "fanqie",
            "rank_id": "1_1_1141",
            "name": "男频·新书榜·都市",
            "rank_type": {"id": "1", "name": "新书榜"},
            "dimensions": {
                "gender": {"id": "1", "name": "男频"},
                "category": {"id": "1141", "name": "都市"},
            },
            "url": "https://fanqienovel.com/rank/1_1_1141",
        }
    ]


def test_jjwxc_discovers_only_canonical_public_rank_links() -> None:
    html = '<a href="topten.php?orderstr=20&amp;t=0">月榜</a>'
    client = FixtureClient(html={"jjwxc:ranks": [FixtureResponse(html)]})

    rankings = JjwxcAdapter(client).ranks()

    assert rankings[0]["rank_id"] == "orderstr=20&t=0"
    assert rankings[0]["dimensions"]["channel"]["name"] == "言情"


def test_zongheng_discovers_categories_returned_by_rank_api() -> None:
    html = '<a href="/rank?rankType=1">月票榜</a>'
    response = FixtureResponse(
        payload={
            "result": {
                "title": "月票榜",
                "cateList": [{"cateFineId": 8102, "cateFineName": "玄幻"}],
            }
        }
    )
    client = FixtureClient(
        html={"zongheng:ranks": [FixtureResponse(html)]},
        requests={"zongheng:ranks": [response]},
    )

    rankings = ZonghengAdapter(client).ranks()

    assert [item["rank_id"] for item in rankings] == [
        "rankType=1&cateFineId=0",
        "rankType=1&cateFineId=8102",
    ]


def test_fanqie_book_reads_public_metrics_from_initial_state() -> None:
    state = {
        "page": {
            "bookName": "番茄指标样书",
            "authorName": "作者乙",
            "abstract": "简介",
            "readCount": 485984,
            "wordNumber": 3203153,
            "chapterTotal": 1586,
        }
    }
    html = (
        '<h1 class="info-name">番茄指标样书</h1>'
        f"<script>window.__INITIAL_STATE__={json.dumps(state, ensure_ascii=False)};</script>"
    )
    client = FixtureClient(html={"fanqie:book": [FixtureResponse(html)]})

    book = FanqieAdapter(client).read_opening("1002", 0).to_dict()

    assert book["word_count"] == 3203153
    assert book["chapter_count"] == 1586
    assert book["metrics"] == {
        "reading_count": 485984,
        "favorite_count": None,
        "recommendation_count": None,
        "comment_count": None,
        "rating": None,
        "hot_score": None,
        "rank_metric": None,
    }
    assert book["source_extra"]["readCount"] == 485984


def test_qidian_book_maps_only_confirmed_public_metrics() -> None:
    client = FixtureClient(
        html={
            "qidian:book": [
                _qidian_page(
                    {
                        "bookInfo": {
                            "bookName": "起点指标样书",
                            "collect": 106,
                            "recomAll": 140,
                            "clickTotal": -1,
                        },
                        "seoBookCirclePost": {"bookCirclePostCount": 96},
                    }
                )
            ]
        }
    )

    book = QidianAdapter(client).read_opening("1001", 0).to_dict()

    assert book["title"] == "起点指标样书"
    assert book["metrics"] == {
        "reading_count": None,
        "favorite_count": 106,
        "recommendation_count": 140,
        "comment_count": 96,
        "rating": None,
        "hot_score": None,
        "rank_metric": None,
    }
    assert book["source_extra"]["clickTotal"] == -1


@pytest.mark.parametrize(
    ("adapter", "client", "book_id"),
    [
        pytest.param(
            QidianAdapter,
            FixtureClient(
                html={
                    "qidian:book": [
                        _qidian_page(
                            {
                                "bookInfo": {
                                    "bName": "起点样书",
                                    "authorName": "作者甲",
                                    "desc": "简介",
                                },
                                "cTCnt": 2,
                            }
                        )
                    ],
                    "qidian:catalog": [_qidian_page({})],
                }
            ),
            "1001",
            id="qidian",
        ),
        pytest.param(
            FanqieAdapter,
            FixtureClient(
                html={
                    "fanqie:book": [
                        FixtureResponse(
                            '<h1 class="info-name">番茄样书</h1>'
                            '<a class="chapter-item-title" href="/reader/2001">第一章</a>'
                            '<a class="chapter-item-title" href="/reader/2002">第二章</a>'
                        )
                    ],
                    "fanqie:chapter": [
                        FixtureResponse(
                            f'<article class="reader-content">{"公开正文" * 30}</article>'
                        ),
                        FixtureResponse(
                            f'<article class="reader-content">订阅后阅读{"付费正文" * 30}</article>'
                        ),
                    ],
                }
            ),
            "1002",
            id="fanqie",
        ),
        pytest.param(
            JjwxcAdapter,
            FixtureClient(
                html={
                    "jjwxc:book": [
                        FixtureResponse(
                            "<h1>晋江样书</h1>"
                            '<a href="onebook.php?novelid=1003&amp;chapterid=1">第一章</a>'
                            '<a href="onebook.php?novelid=1003&amp;chapterid=2">第二章</a>'
                        )
                    ],
                    "jjwxc:chapter": [
                        FixtureResponse(
                            f'<div class="noveltext">{"公开正文" * 30}</div>'
                        ),
                        FixtureResponse(
                            f'<div class="noveltext">VIP章节{"付费正文" * 30}</div>'
                        ),
                    ],
                }
            ),
            "1003",
            id="jjwxc",
        ),
        pytest.param(
            ZonghengAdapter,
            FixtureClient(
                html={
                    "zongheng:book": [
                        FixtureResponse(
                            "<h1>纵横样书</h1>"
                            '<a class="book-info--btn-reading" href="https://read.zongheng.com/chapter/1004/1.html">立即阅读</a>'
                        )
                    ],
                    "zongheng:chapter": [
                        FixtureResponse(
                            f'<h1>第一章</h1><div class="content">{"公开正文" * 30}</div>'
                            '<a rel="next" href="2.html">下一章</a>',
                            url="https://read.zongheng.com/chapter/1004/1.html",
                        ),
                        FixtureResponse(
                            f'<h1>第二章</h1><div class="content">登录后阅读{"付费正文" * 30}</div>',
                            url="https://read.zongheng.com/chapter/1004/2.html",
                        ),
                    ],
                }
            ),
            "1004",
            id="zongheng",
        ),
    ],
)
def test_read_opening_keeps_only_anonymous_public_chapters(
    adapter,
    client,
    book_id: str,
) -> None:
    if adapter is QidianAdapter:
        catalog_html = (
            '<a href="/chapter/1001/1/">第一章免费</a>'
            '<a class="_unPay_" href="/chapter/1001/2/">第二章免费</a>'
        )
        payload = {"pageContext": {"pageProps": {"pageData": {}}}}
        client.html_routes["qidian:catalog"] = deque(
            [
                FixtureResponse(
                    '<script id="vite-plugin-ssr_pageContext">'
                    f"{json.dumps(payload)}"
                    f"</script>{catalog_html}"
                )
            ]
        )
        client.html_routes["qidian:chapter"] = deque(
            [FixtureResponse(f"<main>{'公开正文' * 30}</main>")]
        )

    book = adapter(client, chapter_text=True).read_opening(book_id, 3)

    assert book.title.endswith("样书")
    assert len(book.chapters) == 1
    assert book.chapters[0].content
    assert "付费正文" not in book.chapters[0].content
