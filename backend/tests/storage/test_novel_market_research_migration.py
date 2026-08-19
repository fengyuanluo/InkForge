from __future__ import annotations

import importlib
import json

from sqlalchemy import create_engine, text


migration = importlib.import_module(
    "app.storage.migrations.versions.1020_enable_novel_market_research"
)


def test_migration_updates_only_existing_builtin_agents() -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE agent_definitions ("
                "id TEXT PRIMARY KEY, key TEXT, source TEXT, "
                "enabled_tool_categories TEXT, enabled_skills TEXT)"
            )
        )
        connection.execute(
            text(
                "INSERT INTO agent_definitions "
                "(id, key, source, enabled_tool_categories, enabled_skills) VALUES "
                "('1', 'build', 'builtin', '[\"chapter_read\"]', '[]'), "
                "('2', 'plan', 'builtin', '[\"plan\"]', '[]'), "
                "('3', 'explore', 'custom', '[\"chapter_read\"]', '[]')"
            )
        )

        migration._update_builtin_agents(connection, add=True)

        rows = {
            row["key"]: row
            for row in connection.execute(
                text(
                    "SELECT key, enabled_tool_categories, enabled_skills "
                    "FROM agent_definitions"
                )
            ).mappings()
        }
        assert json.loads(rows["build"]["enabled_tool_categories"]) == [
            "chapter_read",
            "market_research",
        ]
        assert json.loads(rows["build"]["enabled_skills"]) == [
            "builtin-skill--novel-project-research"
        ]
        assert json.loads(rows["plan"]["enabled_tool_categories"]) == [
            "plan",
            "market_research",
        ]
        assert json.loads(rows["explore"]["enabled_tool_categories"]) == [
            "chapter_read"
        ]

        migration._update_builtin_agents(connection, add=False)
        build = (
            connection.execute(
                text(
                    "SELECT enabled_tool_categories, enabled_skills "
                    "FROM agent_definitions WHERE key = 'build'"
                )
            )
            .mappings()
            .one()
        )
        assert json.loads(build["enabled_tool_categories"]) == ["chapter_read"]
        assert json.loads(build["enabled_skills"]) == []

    engine.dispose()
