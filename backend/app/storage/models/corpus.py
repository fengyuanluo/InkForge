"""Corpus library persistence models."""

from datetime import UTC, datetime

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.core.ids import generate_id


def _now() -> datetime:
    return datetime.now(UTC)


class CorpusLibrary(SQLModel, table=True):
    __tablename__ = "corpus_libraries"

    id: str = Field(default_factory=generate_id, primary_key=True)
    name: str = Field(max_length=200, index=True)
    description: str | None = Field(default=None)
    tags_json: str = Field(default="[]")
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now, index=True)


class CorpusDocument(SQLModel, table=True):
    __tablename__ = "corpus_documents"

    id: str = Field(default_factory=generate_id, primary_key=True)
    content_hash: str = Field(max_length=64, unique=True)
    kind: str = Field(max_length=20, index=True)
    title: str = Field(max_length=500, index=True)
    author: str | None = Field(default=None, max_length=300, index=True)
    dynasty: str | None = Field(default=None, max_length=100, index=True)
    tags_json: str = Field(default="[]")
    metadata_json: str = Field(default="{}")
    managed_body_path: str = Field(max_length=1000)
    unit_count: int = Field(default=0, ge=0)
    char_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now, index=True)


class CorpusLibraryDocument(SQLModel, table=True):
    __tablename__ = "corpus_library_documents"

    library_id: str = Field(
        foreign_key="corpus_libraries.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    document_id: str = Field(
        foreign_key="corpus_documents.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    source_aliases_json: str = Field(default="[]")
    metadata_json: str = Field(default="{}")
    created_at: datetime = Field(default_factory=_now)


class CorpusUnit(SQLModel, table=True):
    __tablename__ = "corpus_units"
    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "external_id",
            name="uq_corpus_units_document_external_id",
        ),
        UniqueConstraint(
            "document_id",
            "order_index",
            name="uq_corpus_units_document_order",
        ),
    )

    id: str = Field(default_factory=generate_id, primary_key=True)
    document_id: str = Field(
        foreign_key="corpus_documents.id", ondelete="CASCADE", index=True
    )
    external_id: str = Field(max_length=300)
    kind: str = Field(max_length=20, index=True)
    order_index: int = Field(ge=0, index=True)
    title: str | None = Field(default=None, max_length=500)
    volume: str | None = Field(default=None, max_length=500)
    byte_offset: int = Field(ge=0)
    byte_length: int = Field(ge=0)
    char_count: int = Field(default=0, ge=0)
    text_hash: str = Field(max_length=64)
    metadata_json: str = Field(default="{}")
    created_at: datetime = Field(default_factory=_now)


class ProjectCorpusLibrary(SQLModel, table=True):
    __tablename__ = "project_corpus_libraries"

    project_id: str = Field(
        foreign_key="projects.id", ondelete="CASCADE", primary_key=True
    )
    library_id: str = Field(
        foreign_key="corpus_libraries.id", ondelete="CASCADE", primary_key=True
    )
    created_at: datetime = Field(default_factory=_now)


class CorpusDocumentIndexState(SQLModel, table=True):
    __tablename__ = "corpus_document_index_states"

    document_id: str = Field(
        foreign_key="corpus_documents.id",
        ondelete="CASCADE",
        primary_key=True,
    )
    status: str = Field(default="not_indexed", max_length=30, index=True)
    source_hash: str = Field(max_length=64)
    embedding_model_ref_id: str | None = Field(default=None, index=True)
    embedding_dimensions: int | None = Field(default=None)
    schema_version: int = Field(default=1, ge=1)
    job_id: str | None = Field(default=None, index=True)
    chunk_count: int = Field(default=0, ge=0)
    last_error: str | None = Field(default=None)
    indexed_at: datetime | None = Field(default=None)
    updated_at: datetime = Field(default_factory=_now, index=True)
