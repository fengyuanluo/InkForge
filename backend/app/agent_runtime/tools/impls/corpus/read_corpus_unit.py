"""Read-only corpus unit tool."""

import json

from pydantic import BaseModel, Field

from app.agent_runtime.tools.base import AgentTool
from app.agent_runtime.tools.errors import ToolExecutionError
from app.agent_runtime.tools.registry import ToolRegistry
from app.storage.database import create_session
from app.storage.repos import corpus_repo
from app.storage.services.corpus_service import read_unit_text


class ReadCorpusUnitInput(BaseModel):
    unit_id: str = Field(min_length=1, description="search_corpus 返回的 unit_id")
    start: int = Field(default=0, ge=0, description="从第几个字符开始读取")
    max_chars: int = Field(
        default=12000,
        ge=1,
        le=20000,
        description="本次最多读取的字符数",
    )


@ToolRegistry.register
class ReadCorpusUnitTool(AgentTool):
    name: str = "read_corpus_unit"
    description: str = (
        "分页读取 search_corpus 命中的完整语料单元。"
        "仅允许读取当前项目已挂载语料库中的 unit，并返回 next_start 供继续读取。"
    )
    access_level: str = "readonly"
    args_schema: type[BaseModel] = ReadCorpusUnitInput

    async def _execute(
        self,
        unit_id: str,
        start: int = 0,
        max_chars: int = 12000,
    ) -> str:
        session = await create_session()
        try:
            unit = await corpus_repo.get_unit(session, unit_id)
            if unit is None:
                raise ToolExecutionError("语料单元不存在")
            document = await corpus_repo.get_document(session, unit.document_id)
            if document is None:
                raise ToolExecutionError("语料文档不存在")
            mounted_ids = set(
                await corpus_repo.list_project_library_ids(session, self.project_id)
            )
            document_library_ids = set(
                await corpus_repo.list_library_ids_for_document(session, document.id)
            )
            if not mounted_ids.intersection(document_library_ids):
                raise ToolExecutionError("该语料单元不属于当前项目已挂载的语料库")

            full_text = read_unit_text(document, unit)
            if start >= len(full_text) and full_text:
                raise ToolExecutionError("start 超出语料单元正文范围")
            end = min(len(full_text), start + max_chars)
            return json.dumps(
                {
                    "document_id": document.id,
                    "unit_id": unit.id,
                    "title": document.title,
                    "author": document.author,
                    "dynasty": document.dynasty,
                    "unit_title": unit.title,
                    "volume": unit.volume,
                    "unit_order": unit.order_index,
                    "text": full_text[start:end],
                    "start": start,
                    "next_start": end if end < len(full_text) else None,
                    "total_chars": len(full_text),
                    "truncated": end < len(full_text),
                },
                ensure_ascii=False,
            )
        finally:
            await session.close()
