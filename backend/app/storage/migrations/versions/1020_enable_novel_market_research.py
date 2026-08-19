"""enable novel market research for built-in agents

Revision ID: 1020
Revises: 1019
Create Date: 2026-08-19 23:00:00.000000
"""

from __future__ import annotations

import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import Connection


revision: str = "1020"
down_revision: Union[str, Sequence[str], None] = "1019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SKILL_ID = "builtin-skill--novel-project-research"
TOOL_CATEGORY = "market_research"


def _load_str_list(raw_value: object) -> list[str]:
    if isinstance(raw_value, list):
        return [str(item) for item in raw_value]
    if isinstance(raw_value, str):
        try:
            parsed = json.loads(raw_value)
        except json.JSONDecodeError:
            return []
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    return []


def _update_builtin_agents(bind: Connection, *, add: bool) -> None:
    rows = bind.execute(
        sa.text(
            "SELECT id, key, enabled_tool_categories, enabled_skills "
            "FROM agent_definitions "
            "WHERE source = 'builtin' AND key IN ('build', 'plan', 'explore')"
        )
    ).fetchall()
    for row in rows:
        categories = _load_str_list(row.enabled_tool_categories)
        skills = _load_str_list(row.enabled_skills)
        if add:
            if TOOL_CATEGORY not in categories:
                categories.append(TOOL_CATEGORY)
            if row.key == "build" and SKILL_ID not in skills:
                skills.append(SKILL_ID)
        else:
            categories = [item for item in categories if item != TOOL_CATEGORY]
            if row.key == "build":
                skills = [item for item in skills if item != SKILL_ID]
        bind.execute(
            sa.text(
                "UPDATE agent_definitions "
                "SET enabled_tool_categories = :categories, enabled_skills = :skills "
                "WHERE id = :id"
            ),
            {
                "id": row.id,
                "categories": json.dumps(categories, ensure_ascii=False),
                "skills": json.dumps(skills, ensure_ascii=False),
            },
        )


def upgrade() -> None:
    _update_builtin_agents(op.get_bind(), add=True)


def downgrade() -> None:
    _update_builtin_agents(op.get_bind(), add=False)
