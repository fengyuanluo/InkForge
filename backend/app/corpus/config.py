"""Corpus retrieval settings and model client construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.encryption import EncryptionService
from app.models.clients.embedding_client import (
    EmbeddingClient,
    EmbeddingClientLike,
    EmbeddingConfig,
)
from app.models.clients.rerank_client import RerankClient, RerankConfig
from app.models.entities.model import Model
from app.models.repos import model_provider_repo, model_repo
from app.models.services.model_provider_service import ModelProviderService
from app.settings import settings
from app.storage.repos import setting_repo


SETTING_KEY_CORPUS_EMBEDDING_MODEL = "corpus_embedding_model"
SETTING_KEY_CORPUS_RERANK_ENABLED = "corpus_rerank_enabled"
SETTING_KEY_CORPUS_RERANK_MODEL = "corpus_rerank_model"
SETTING_KEY_CORPUS_INDEX_CONCURRENCY = "corpus_index_concurrency"

DEFAULT_CORPUS_RERANK_ENABLED = False
DEFAULT_CORPUS_INDEX_CONCURRENCY = 1
MAX_CORPUS_INDEX_CONCURRENCY = 4


@dataclass(frozen=True)
class CorpusRetrievalConfig:
    embedding_model_ref_id: str
    rerank_enabled: bool
    rerank_model_ref_id: str
    index_concurrency: int


def _bool(raw: str | None, default: bool = False) -> bool:
    if raw is None:
        return default
    return raw.strip().lower() in {"true", "1", "yes", "on"}


def _int(raw: str | None, default: int) -> int:
    try:
        return int(raw or "")
    except ValueError:
        return default


async def get_corpus_retrieval_config(session: AsyncSession) -> CorpusRetrievalConfig:
    rows = await setting_repo.get_all(session)
    raw = {row.key: row.value for row in rows}
    concurrency = _int(
        raw.get(SETTING_KEY_CORPUS_INDEX_CONCURRENCY),
        DEFAULT_CORPUS_INDEX_CONCURRENCY,
    )
    return CorpusRetrievalConfig(
        embedding_model_ref_id=(raw.get(SETTING_KEY_CORPUS_EMBEDDING_MODEL) or "").strip(),
        rerank_enabled=_bool(
            raw.get(SETTING_KEY_CORPUS_RERANK_ENABLED),
            DEFAULT_CORPUS_RERANK_ENABLED,
        ),
        rerank_model_ref_id=(raw.get(SETTING_KEY_CORPUS_RERANK_MODEL) or "").strip(),
        index_concurrency=max(1, min(concurrency, MAX_CORPUS_INDEX_CONCURRENCY)),
    )


async def resolve_corpus_embedding_model(
    session: AsyncSession, model_ref_id: str
) -> Model:
    if not model_ref_id:
        raise ValueError("未配置语料库 Embedding 模型")
    model = await model_repo.get_by_id(session, model_ref_id)
    if model is None or model.task_type != "embedding" or model.dimensions is None:
        raise ValueError("语料库 Embedding 模型不存在、类型错误或缺少 dimensions")
    return model


async def _provider_credentials(session: AsyncSession, model: Model) -> tuple[str, str, str]:
    provider = await model_provider_repo.get_by_id(session, model.provider_id)
    if provider is None:
        raise ValueError(f"模型关联的 provider 不存在: {model.provider_id}")
    provider_service = ModelProviderService(EncryptionService(settings.encryption_key))
    return (
        provider.provider_type,
        provider.url,
        provider_service.get_decrypted_api_key(provider) or "",
    )


async def build_corpus_embedding_client(
    session: AsyncSession, model: Model
) -> EmbeddingClientLike:
    provider_type, base_url, api_key = await _provider_credentials(session, model)
    return cast(
        EmbeddingClientLike,
        EmbeddingClient(
            EmbeddingConfig(
                provider_type=provider_type,
                base_url=base_url,
                api_key=api_key,
                model_id=model.model_id,
                dimensions=model.dimensions,
            )
        )
    )


async def build_corpus_rerank_client(
    session: AsyncSession, model_ref_id: str
) -> RerankClient | None:
    if not model_ref_id:
        return None
    model = await model_repo.get_by_id(session, model_ref_id)
    if model is None or model.task_type != "rerank":
        return None
    provider_type, base_url, api_key = await _provider_credentials(session, model)
    return RerankClient(
        RerankConfig(
            provider_type=provider_type,
            base_url=base_url,
            api_key=api_key,
            model_id=model.model_id,
        )
    )
