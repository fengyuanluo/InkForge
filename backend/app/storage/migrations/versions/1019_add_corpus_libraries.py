"""add corpus libraries

Revision ID: 1019
Revises: 1018
Create Date: 2026-08-17 18:00:00.000000
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1019"
down_revision: Union[str, Sequence[str], None] = "1018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "corpus_libraries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("tags_json", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_corpus_libraries_name", "corpus_libraries", ["name"])
    op.create_index(
        "ix_corpus_libraries_updated_at", "corpus_libraries", ["updated_at"]
    )

    op.create_table(
        "corpus_documents",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("author", sa.String(length=300), nullable=True),
        sa.Column("dynasty", sa.String(length=100), nullable=True),
        sa.Column("tags_json", sa.String(), nullable=False),
        sa.Column("metadata_json", sa.String(), nullable=False),
        sa.Column("managed_body_path", sa.String(length=1000), nullable=False),
        sa.Column("unit_count", sa.Integer(), nullable=False),
        sa.Column("char_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("unit_count >= 0"),
        sa.CheckConstraint("char_count >= 0"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("content_hash"),
    )
    for name, columns in (
        ("ix_corpus_documents_kind", ["kind"]),
        ("ix_corpus_documents_title", ["title"]),
        ("ix_corpus_documents_author", ["author"]),
        ("ix_corpus_documents_dynasty", ["dynasty"]),
        ("ix_corpus_documents_updated_at", ["updated_at"]),
    ):
        op.create_index(name, "corpus_documents", columns)

    op.create_table(
        "corpus_library_documents",
        sa.Column("library_id", sa.String(), nullable=False),
        sa.Column("document_id", sa.String(), nullable=False),
        sa.Column("source_aliases_json", sa.String(), nullable=False),
        sa.Column("metadata_json", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"], ["corpus_documents.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["library_id"], ["corpus_libraries.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("library_id", "document_id"),
    )

    op.create_table(
        "corpus_units",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("document_id", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(length=300), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("volume", sa.String(length=500), nullable=True),
        sa.Column("byte_offset", sa.Integer(), nullable=False),
        sa.Column("byte_length", sa.Integer(), nullable=False),
        sa.Column("char_count", sa.Integer(), nullable=False),
        sa.Column("text_hash", sa.String(length=64), nullable=False),
        sa.Column("metadata_json", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("order_index >= 0"),
        sa.CheckConstraint("byte_offset >= 0"),
        sa.CheckConstraint("byte_length >= 0"),
        sa.CheckConstraint("char_count >= 0"),
        sa.ForeignKeyConstraint(
            ["document_id"], ["corpus_documents.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "document_id",
            "external_id",
            name="uq_corpus_units_document_external_id",
        ),
        sa.UniqueConstraint(
            "document_id",
            "order_index",
            name="uq_corpus_units_document_order",
        ),
    )
    op.create_index("ix_corpus_units_document_id", "corpus_units", ["document_id"])
    op.create_index("ix_corpus_units_kind", "corpus_units", ["kind"])
    op.create_index("ix_corpus_units_order_index", "corpus_units", ["order_index"])

    op.create_table(
        "project_corpus_libraries",
        sa.Column("project_id", sa.String(), nullable=False),
        sa.Column("library_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["library_id"], ["corpus_libraries.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "library_id"),
    )

    op.create_table(
        "corpus_document_index_states",
        sa.Column("document_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("source_hash", sa.String(length=64), nullable=False),
        sa.Column("embedding_model_ref_id", sa.String(), nullable=True),
        sa.Column("embedding_dimensions", sa.Integer(), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(), nullable=True),
        sa.Column("chunk_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.String(), nullable=True),
        sa.Column("indexed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("schema_version >= 1"),
        sa.CheckConstraint("chunk_count >= 0"),
        sa.ForeignKeyConstraint(
            ["document_id"], ["corpus_documents.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("document_id"),
    )
    for name, columns in (
        ("ix_corpus_document_index_states_status", ["status"]),
        (
            "ix_corpus_document_index_states_embedding_model_ref_id",
            ["embedding_model_ref_id"],
        ),
        ("ix_corpus_document_index_states_job_id", ["job_id"]),
        ("ix_corpus_document_index_states_updated_at", ["updated_at"]),
    ):
        op.create_index(name, "corpus_document_index_states", columns)


def downgrade() -> None:
    op.drop_table("corpus_document_index_states")
    op.drop_table("project_corpus_libraries")
    op.drop_table("corpus_units")
    op.drop_table("corpus_library_documents")
    op.drop_table("corpus_documents")
    op.drop_table("corpus_libraries")
