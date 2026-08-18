"""Database access for managed corpus libraries."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.storage.models.corpus import (
    CorpusDocument,
    CorpusDocumentIndexState,
    CorpusLibrary,
    CorpusLibraryDocument,
    CorpusUnit,
    ProjectCorpusLibrary,
)


async def create_library(session: AsyncSession, library: CorpusLibrary) -> CorpusLibrary:
    session.add(library)
    await session.flush()
    await session.refresh(library)
    return library


async def get_library(session: AsyncSession, library_id: str) -> CorpusLibrary | None:
    result = await session.execute(
        select(CorpusLibrary).where(col(CorpusLibrary.id) == library_id)
    )
    return result.scalar_one_or_none()


async def list_libraries(session: AsyncSession) -> list[CorpusLibrary]:
    result = await session.execute(
        select(CorpusLibrary).order_by(
            col(CorpusLibrary.updated_at).desc(),
            col(CorpusLibrary.id).asc(),
        )
    )
    return list(result.scalars().all())


async def update_library(session: AsyncSession, library: CorpusLibrary) -> CorpusLibrary:
    library.updated_at = datetime.now(UTC)
    session.add(library)
    await session.flush()
    await session.refresh(library)
    return library


async def delete_library_row(session: AsyncSession, library: CorpusLibrary) -> None:
    await session.delete(library)
    await session.flush()


async def count_library_documents(session: AsyncSession, library_id: str) -> int:
    result = await session.execute(
        select(func.count())
        .select_from(CorpusLibraryDocument)
        .where(col(CorpusLibraryDocument.library_id) == library_id)
    )
    return int(result.scalar_one())


async def count_library_characters(session: AsyncSession, library_id: str) -> int:
    result = await session.execute(
        select(func.coalesce(func.sum(col(CorpusDocument.char_count)), 0))
        .select_from(CorpusLibraryDocument)
        .join(
            CorpusDocument,
            col(CorpusDocument.id) == col(CorpusLibraryDocument.document_id),
        )
        .where(col(CorpusLibraryDocument.library_id) == library_id)
    )
    return int(result.scalar_one())


async def create_document(session: AsyncSession, document: CorpusDocument) -> CorpusDocument:
    session.add(document)
    await session.flush()
    await session.refresh(document)
    return document


async def get_document(session: AsyncSession, document_id: str) -> CorpusDocument | None:
    result = await session.execute(
        select(CorpusDocument).where(col(CorpusDocument.id) == document_id)
    )
    return result.scalar_one_or_none()


async def get_document_by_hash(
    session: AsyncSession, content_hash: str
) -> CorpusDocument | None:
    result = await session.execute(
        select(CorpusDocument).where(col(CorpusDocument.content_hash) == content_hash)
    )
    return result.scalar_one_or_none()


async def list_all_documents(session: AsyncSession) -> list[CorpusDocument]:
    result = await session.execute(
        select(CorpusDocument).order_by(
            col(CorpusDocument.created_at).asc(),
            col(CorpusDocument.id).asc(),
        )
    )
    return list(result.scalars().all())


async def list_documents_by_ids(
    session: AsyncSession, document_ids: list[str]
) -> list[CorpusDocument]:
    if not document_ids:
        return []
    result = await session.execute(
        select(CorpusDocument).where(col(CorpusDocument.id).in_(document_ids))
    )
    by_id = {document.id: document for document in result.scalars().all()}
    return [by_id[document_id] for document_id in document_ids if document_id in by_id]


async def list_library_documents(
    session: AsyncSession, library_id: str
) -> list[tuple[CorpusDocument, CorpusLibraryDocument, CorpusDocumentIndexState | None]]:
    result = await session.execute(
        select(CorpusDocument, CorpusLibraryDocument, CorpusDocumentIndexState)
        .join(
            CorpusLibraryDocument,
            col(CorpusLibraryDocument.document_id) == col(CorpusDocument.id),
        )
        .outerjoin(
            CorpusDocumentIndexState,
            col(CorpusDocumentIndexState.document_id) == col(CorpusDocument.id),
        )
        .where(col(CorpusLibraryDocument.library_id) == library_id)
        .order_by(col(CorpusLibraryDocument.created_at).asc())
    )
    rows: list[
        tuple[CorpusDocument, CorpusLibraryDocument, CorpusDocumentIndexState | None]
    ] = []
    for document, link, index_state in result.all():
        rows.append((document, link, index_state))
    return rows


async def update_document(session: AsyncSession, document: CorpusDocument) -> CorpusDocument:
    document.updated_at = datetime.now(UTC)
    session.add(document)
    await session.flush()
    await session.refresh(document)
    return document


async def delete_document_row(session: AsyncSession, document: CorpusDocument) -> None:
    await session.execute(
        delete(CorpusDocumentIndexState).where(
            col(CorpusDocumentIndexState.document_id) == document.id
        )
    )
    await session.execute(
        delete(CorpusUnit).where(col(CorpusUnit.document_id) == document.id)
    )
    await session.delete(document)
    await session.flush()


async def create_units(session: AsyncSession, units: list[CorpusUnit]) -> None:
    if not units:
        return
    session.add_all(units)
    await session.flush()


async def get_unit(session: AsyncSession, unit_id: str) -> CorpusUnit | None:
    result = await session.execute(select(CorpusUnit).where(col(CorpusUnit.id) == unit_id))
    return result.scalar_one_or_none()


async def list_document_units(
    session: AsyncSession, document_id: str
) -> list[CorpusUnit]:
    result = await session.execute(
        select(CorpusUnit)
        .where(col(CorpusUnit.document_id) == document_id)
        .order_by(col(CorpusUnit.order_index).asc(), col(CorpusUnit.id).asc())
    )
    return list(result.scalars().all())


async def get_library_document_link(
    session: AsyncSession, library_id: str, document_id: str
) -> CorpusLibraryDocument | None:
    result = await session.execute(
        select(CorpusLibraryDocument).where(
            col(CorpusLibraryDocument.library_id) == library_id,
            col(CorpusLibraryDocument.document_id) == document_id,
        )
    )
    return result.scalar_one_or_none()


async def save_library_document_link(
    session: AsyncSession, link: CorpusLibraryDocument
) -> CorpusLibraryDocument:
    session.add(link)
    await session.flush()
    await session.refresh(link)
    return link


async def list_library_ids_for_document(
    session: AsyncSession, document_id: str
) -> list[str]:
    result = await session.execute(
        select(col(CorpusLibraryDocument.library_id))
        .where(col(CorpusLibraryDocument.document_id) == document_id)
        .order_by(col(CorpusLibraryDocument.library_id).asc())
    )
    return list(result.scalars().all())


async def list_document_ids_for_library(
    session: AsyncSession, library_id: str
) -> list[str]:
    result = await session.execute(
        select(col(CorpusLibraryDocument.document_id)).where(
            col(CorpusLibraryDocument.library_id) == library_id
        )
    )
    return list(result.scalars().all())


async def unlink_library_documents(session: AsyncSession, library_id: str) -> None:
    await session.execute(
        delete(CorpusLibraryDocument).where(
            col(CorpusLibraryDocument.library_id) == library_id
        )
    )
    await session.flush()


async def document_membership_count(session: AsyncSession, document_id: str) -> int:
    result = await session.execute(
        select(func.count())
        .select_from(CorpusLibraryDocument)
        .where(col(CorpusLibraryDocument.document_id) == document_id)
    )
    return int(result.scalar_one())


async def get_index_state(
    session: AsyncSession, document_id: str
) -> CorpusDocumentIndexState | None:
    result = await session.execute(
        select(CorpusDocumentIndexState).where(
            col(CorpusDocumentIndexState.document_id) == document_id
        )
    )
    return result.scalar_one_or_none()


async def save_index_state(
    session: AsyncSession, state: CorpusDocumentIndexState
) -> CorpusDocumentIndexState:
    state.updated_at = datetime.now(UTC)
    session.add(state)
    await session.flush()
    await session.refresh(state)
    return state


async def has_ready_index_state(session: AsyncSession) -> bool:
    result = await session.execute(
        select(func.count())
        .select_from(CorpusDocumentIndexState)
        .where(col(CorpusDocumentIndexState.status) == "ready")
    )
    return int(result.scalar_one()) > 0


async def mark_all_index_states_needs_rebuild(session: AsyncSession) -> None:
    states = list((await session.execute(select(CorpusDocumentIndexState))).scalars().all())
    now = datetime.now(UTC)
    for state in states:
        state.status = "needs_rebuild"
        state.job_id = None
        state.updated_at = now
        session.add(state)
    await session.flush()


async def delete_project_mounts_for_library(
    session: AsyncSession, library_id: str
) -> None:
    await session.execute(
        delete(ProjectCorpusLibrary).where(
            col(ProjectCorpusLibrary.library_id) == library_id
        )
    )
    await session.flush()


async def list_project_library_ids(session: AsyncSession, project_id: str) -> list[str]:
    result = await session.execute(
        select(col(ProjectCorpusLibrary.library_id))
        .where(col(ProjectCorpusLibrary.project_id) == project_id)
        .order_by(col(ProjectCorpusLibrary.created_at).asc())
    )
    return list(result.scalars().all())


async def replace_project_libraries(
    session: AsyncSession, project_id: str, library_ids: list[str]
) -> None:
    await session.execute(
        delete(ProjectCorpusLibrary).where(
            col(ProjectCorpusLibrary.project_id) == project_id
        )
    )
    session.add_all(
        [
            ProjectCorpusLibrary(project_id=project_id, library_id=library_id)
            for library_id in library_ids
        ]
    )
    await session.flush()
