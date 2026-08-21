from __future__ import annotations

import importlib
import json

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, text


migration = importlib.import_module(
    "app.storage.migrations.versions.1021_add_skill_metadata"
)


def test_migration_adds_metadata_to_existing_skills(monkeypatch) -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE skills (id TEXT PRIMARY KEY)"))
        connection.execute(text("INSERT INTO skills (id) VALUES ('skill-1')"))

        operations = Operations(MigrationContext.configure(connection))
        monkeypatch.setattr(migration, "op", operations)
        migration.upgrade()

        columns = {
            row["name"]
            for row in connection.execute(text("PRAGMA table_info(skills)")).mappings()
        }
        metadata = connection.execute(
            text("SELECT metadata FROM skills WHERE id = 'skill-1'")
        ).scalar_one()

        assert "metadata" in columns
        assert json.loads(metadata) == {}

    engine.dispose()
