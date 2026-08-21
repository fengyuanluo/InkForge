# -*- coding: utf-8 -*-
"""Skill API Schemas。"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.api.schemas.skill_reference_doc import SkillReferenceDocResponse


class SkillCreate(BaseModel):
    name: str = Field(default="", description="技能名称")
    summary: str = Field(default="", description="技能简述")
    content: str = Field(default="", description="技能内容")
    metadata: dict[str, Any] = Field(default_factory=dict, description="扩展元数据")
    is_enabled: bool = Field(default=False, description="是否启用")


class SkillUpdate(BaseModel):
    name: str | None = Field(default=None, description="技能名称")
    summary: str | None = Field(default=None, description="技能简述")
    content: str | None = Field(default=None, description="技能内容")
    metadata: dict[str, Any] | None = Field(default=None, description="扩展元数据")
    is_enabled: bool | None = Field(default=None, description="是否启用")


class SkillResponse(BaseModel):
    id: str
    name: str
    summary: str
    content: str
    metadata: dict[str, Any]
    is_enabled: bool
    is_complete: bool
    source: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SkillListResponse(BaseModel):
    items: list[SkillResponse]
    total: int
    page: int
    page_size: int


class SkillImportResponse(BaseModel):
    skill: SkillResponse
    reference_docs: list[SkillReferenceDocResponse]
    is_recognized: bool
