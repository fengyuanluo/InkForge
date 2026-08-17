"""Corpus library API schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CorpusLibraryCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class CorpusLibraryUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    tags: list[str] | None = None


class CorpusLibraryResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    document_count: int = 0
    char_count: int = 0
    created_at: datetime
    updated_at: datetime


class CorpusLibraryListResponse(BaseModel):
    items: list[CorpusLibraryResponse]


class CorpusDocumentUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    author: str | None = Field(default=None, max_length=300)
    dynasty: str | None = Field(default=None, max_length=100)
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class CorpusDocumentResponse(BaseModel):
    id: str
    kind: str
    title: str
    author: str | None = None
    dynasty: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    library_ids: list[str] = Field(default_factory=list)
    source_aliases: list[str] = Field(default_factory=list)
    unit_count: int
    char_count: int
    index_status: str = "not_indexed"
    index_chunk_count: int = 0
    index_job_id: str | None = None
    index_error: str | None = None
    indexed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class CorpusDocumentListResponse(BaseModel):
    items: list[CorpusDocumentResponse]


class CorpusUnitBriefResponse(BaseModel):
    id: str
    document_id: str
    kind: str
    order: int
    title: str | None = None
    volume: str | None = None
    char_count: int
    metadata: dict[str, Any] = Field(default_factory=dict)


class CorpusUnitListResponse(BaseModel):
    items: list[CorpusUnitBriefResponse]


class CorpusUnitResponse(CorpusUnitBriefResponse):
    document_title: str
    author: str | None = None
    dynasty: str | None = None
    text: str


class CorpusImportFromRootRequest(BaseModel):
    path: str = Field(min_length=1, max_length=2000)
    library_id: str | None = None
    library_name: str | None = Field(default=None, max_length=200)


class CorpusImportResponse(BaseModel):
    library_id: str
    document_ids: list[str]
    imported_count: int
    deduplicated_count: int
    unit_count: int
    job_id: str


class CorpusProjectMountUpdateRequest(BaseModel):
    library_ids: list[str] = Field(default_factory=list)


class CorpusProjectMountResponse(BaseModel):
    project_id: str
    library_ids: list[str] = Field(default_factory=list)


class CorpusSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    project_id: str | None = None
    library_ids: list[str] = Field(default_factory=list)
    limit: int = Field(default=8, ge=1, le=8)


class CorpusSearchHitResponse(BaseModel):
    document_id: str
    unit_id: str
    chunk_index: int
    text: str
    context_text: str | None = None
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
    library_ids: list[str] = Field(default_factory=list)


class CorpusSearchResponse(BaseModel):
    items: list[CorpusSearchHitResponse]


class CorpusJobResponse(BaseModel):
    id: str
    status: str
    progress: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] = Field(default_factory=dict)
    error: dict[str, Any] = Field(default_factory=dict)
    attempt_count: int
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None


class CorpusJobListResponse(BaseModel):
    items: list[CorpusJobResponse]


class CorpusRebuildResponse(BaseModel):
    document_count: int
    job_id: str
