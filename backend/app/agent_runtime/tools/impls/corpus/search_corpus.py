"""Read-only corpus search tool."""

from pydantic import BaseModel, Field

from app.agent_runtime.tools.base import AgentTool
from app.agent_runtime.tools.errors import ToolExecutionError
from app.agent_runtime.tools.registry import ToolRegistry
from app.corpus.index import search_corpus
from app.storage.database import create_session


class SearchCorpusInput(BaseModel):
    query: str = Field(min_length=1, max_length=2000, description="自然语言检索语句")
    limit: int = Field(default=8, ge=1, le=8, description="最多返回的结果数")


@ToolRegistry.register
class SearchCorpusTool(AgentTool):
    name: str = "search_corpus"
    description: str = (
        "检索当前项目已挂载的精品语料库，返回可引用的原文片段、作品信息和 unit_id。"
        "需要完整上下文时，再用 read_corpus_unit 分页读取对应语料单元。"
    )
    access_level: str = "readonly"
    args_schema: type[BaseModel] = SearchCorpusInput

    async def _execute(self, query: str, limit: int = 8) -> str:
        session = await create_session()
        try:
            try:
                hits = await search_corpus(
                    session,
                    query=query,
                    project_id=self.project_id,
                    limit=limit,
                )
            except ValueError as exc:
                raise ToolExecutionError(str(exc)) from exc
            return SearchCorpusOutput(
                query=query,
                results=[
                    SearchCorpusHitOutput(
                        document_id=hit.document_id,
                        unit_id=hit.unit_id,
                        chunk_index=hit.chunk_index,
                        text=hit.context_text or hit.text,
                        score=hit.score,
                        matched_by=hit.matched_by,
                        title=hit.title,
                        author=hit.author,
                        dynasty=hit.dynasty,
                        document_kind=hit.document_kind,
                        unit_kind=hit.unit_kind,
                        unit_title=hit.unit_title,
                        volume=hit.volume,
                        unit_order=hit.unit_order,
                        tags=hit.tags,
                    )
                    for hit in hits
                ],
            ).model_dump_json()
        finally:
            await session.close()


class SearchCorpusHitOutput(BaseModel):
    document_id: str
    unit_id: str
    chunk_index: int
    text: str
    score: float
    matched_by: str
    title: str
    author: str | None = None
    dynasty: str | None = None
    document_kind: str
    unit_kind: str
    unit_title: str | None = None
    volume: str | None = None
    unit_order: int
    tags: list[str] = Field(default_factory=list)


class SearchCorpusOutput(BaseModel):
    query: str
    results: list[SearchCorpusHitOutput]
