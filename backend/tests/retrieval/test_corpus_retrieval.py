import asyncio
from dataclasses import dataclass
from pathlib import Path

import pytest

from app.retrieval.engine import LanceDBRetrievalEngine
from app.retrieval.internal.query.ranking import rrf_merge
from app.retrieval.types import (
    FilterableField,
    FilterableFieldType,
    IndexChunk,
    RetrievalIndexContract,
)


@dataclass
class FakeEmbeddingResponse:
    embeddings: list[list[float]]
    model: str = "fake-embedding"
    usage: None = None


class FakeEmbeddingClient:
    config = type(
        "FakeEmbeddingConfig",
        (),
        {"model_id": "fake-embedding", "dimensions": 3},
    )()

    @staticmethod
    def _vector(text: str) -> list[float]:
        return [
            1.0 if "dragon" in text.lower() else 0.0,
            1.0 if "hero" in text.lower() else 0.0,
            0.2,
        ]

    async def embed(self, texts: list[str]) -> FakeEmbeddingResponse:
        return FakeEmbeddingResponse([self._vector(text) for text in texts])

    async def embed_single(self, text: str) -> list[float]:
        return self._vector(text)


def _contract() -> RetrievalIndexContract:
    return RetrievalIndexContract(
        embedding_model_ref_id="model-1",
        embedding_model_id_snapshot="fake-embedding",
        embedding_dimensions_snapshot=3,
        distance_metric="cosine",
        chunker_type="corpus_structure_aware",
        chunk_size=800,
        chunk_overlap=100,
        filterable_fields=[
            FilterableField(
                name="library_ids",
                field_type=FilterableFieldType.STRING_LIST,
            )
        ],
        fts_index_params={"language": "English"},
        schema_version=1,
    )


@pytest.mark.asyncio
async def test_concurrent_first_write_and_library_array_filter(tmp_path: Path) -> None:
    engine = LanceDBRetrievalEngine(
        base_dir=tmp_path / "lancedb",
        table_name="corpus",
        contract=_contract(),
    )
    client = FakeEmbeddingClient()

    await asyncio.gather(
        *[
            engine.index_chunks(
                [
                    IndexChunk(
                        document_id=f"document-{index}",
                        chunk_index=0,
                        raw_text=f"dragon passage {index}",
                        indexed_text=f"dragon passage {index}",
                        attributes={
                            "library_ids": ["library-a" if index % 2 == 0 else "library-b"]
                        },
                    )
                ],
                client,
            )
            for index in range(8)
        ]
    )
    await engine.finalize_chunk_index()

    results = await (
        engine.query("dragon", client)
        .hybrid()
        .filter_array_any("library_ids", ["library-a"])
        .limit(8)
        .run()
    )

    assert {result.document_id for result in results} == {
        "document-0",
        "document-2",
        "document-4",
        "document-6",
    }


def test_rrf_merge_applies_independent_weights() -> None:
    vector_rows = [
        {
            "chunk_id": "vector",
            "document_id": "d1",
            "chunk_index": 0,
            "text": "vector",
            "metadata": "{}",
            "_distance": 0.1,
        }
    ]
    bm25_rows = [
        {
            "chunk_id": "bm25",
            "document_id": "d2",
            "chunk_index": 0,
            "text": "bm25",
            "metadata": "{}",
            "_score": 1.0,
        }
    ]

    vector_first = rrf_merge(
        vector_rows,
        bm25_rows,
        60,
        vector_weight=0.9,
        bm25_weight=0.1,
    )
    bm25_first = rrf_merge(
        vector_rows,
        bm25_rows,
        60,
        vector_weight=0.1,
        bm25_weight=0.9,
    )

    assert vector_first["vector"]["rrf_score"] > vector_first["bm25"]["rrf_score"]
    assert bm25_first["bm25"]["rrf_score"] > bm25_first["vector"]["rrf_score"]
