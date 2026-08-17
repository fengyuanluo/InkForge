"""OpenFic corpus package v1 validation and conservative TXT conversion."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import unicodedata
from typing import Any, Literal
from uuid import uuid4
from zipfile import ZipFile

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.settings import settings


SCHEMA_VERSION = "openfic-corpus/v1"
DOCUMENT_KINDS = frozenset({"novel", "poetry", "generic"})
UNIT_KINDS = frozenset({"chapter", "poem", "ci", "section", "text"})
REQUIRED_PACKAGE_FILES = frozenset({"manifest.json", "documents.jsonl", "units.jsonl"})
TXT_MAX_BYTES = 100 * 1024 * 1024

_CHAPTER_HEADING = re.compile(
    r"^\s*(?:第[零〇一二三四五六七八九十百千万0-9]{1,12}[章节回卷部集篇]"
    r"(?:[\s:：._-]+.{0,80})?|chapter\s+[0-9]{1,8}(?:[\s:._-]+.{0,80})?)\s*$",
    re.IGNORECASE,
)
_MOJIBAKE_MARKERS = ("锟斤拷", "鐨勫", "銆€", "浣犲ソ", "鏂囧瓧", "ï¿½")


class CorpusPackageError(ValueError):
    """Raised when an import source violates the corpus package contract."""


class CorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["openfic-corpus/v1"]
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def _clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value


class CorpusPackageDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=300)
    kind: Literal["novel", "poetry", "generic"]
    title: str = Field(min_length=1, max_length=500)
    author: str | None = Field(default=None, max_length=300)
    dynasty: str | None = Field(default=None, max_length=100)
    tags: list[str] = Field(default_factory=list)
    source: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("id", "title")
    @classmethod
    def _clean_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("value must not be blank")
        return value


class CorpusPackageUnit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=300)
    document_id: str = Field(min_length=1, max_length=300)
    kind: Literal["chapter", "poem", "ci", "section", "text"]
    order: int = Field(ge=0)
    title: str | None = Field(default=None, max_length=500)
    volume: str | None = Field(default=None, max_length=500)
    text: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("id", "document_id")
    @classmethod
    def _clean_identifier(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("value must not be blank")
        return value

    @field_validator("text")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value


class ValidatedCorpusPackage(BaseModel):
    root: Path
    manifest: CorpusManifest
    documents: list[CorpusPackageDocument]
    unit_count: int
    char_count: int


def normalize_unit_text(text: str) -> str:
    """Normalize line endings and Unicode without rewriting literary content."""
    normalized = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return normalized.strip("\n")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CorpusPackageError(f"无法读取合法 UTF-8 JSON: {path.name}: {exc}") from exc


def _iter_jsonl(path: Path) -> Iterator[tuple[int, Any]]:
    try:
        stream = path.open("r", encoding="utf-8")
    except OSError as exc:
        raise CorpusPackageError(f"无法读取 {path.name}: {exc}") from exc
    with stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                yield line_number, json.loads(line)
            except json.JSONDecodeError as exc:
                raise CorpusPackageError(
                    f"{path.name}:{line_number} 不是合法 JSON: {exc.msg}"
                ) from exc


def _validate_source_path(root: Path, source: str | None) -> None:
    if source is None:
        return
    pure = PurePosixPath(source)
    if pure.is_absolute() or ".." in pure.parts or not pure.parts:
        raise CorpusPackageError(f"非法 source 路径: {source}")
    if pure.parts[0] != "sources":
        raise CorpusPackageError(f"source 必须位于 sources/ 下: {source}")
    target = (root / Path(*pure.parts)).resolve()
    sources_root = root / "sources"
    if not target.is_relative_to(sources_root) or not target.is_file():
        raise CorpusPackageError(f"source 文件不存在: {source}")


def validate_package(root: Path) -> ValidatedCorpusPackage:
    root = root.resolve()
    if not root.is_dir():
        raise CorpusPackageError(f"语料包目录不存在: {root}")
    missing = sorted(name for name in REQUIRED_PACKAGE_FILES if not (root / name).is_file())
    if missing:
        raise CorpusPackageError(f"语料包缺少文件: {', '.join(missing)}")
    escaped = sorted(
        name
        for name in REQUIRED_PACKAGE_FILES
        if not (root / name).resolve().is_relative_to(root)
    )
    if escaped:
        raise CorpusPackageError(f"语料包文件路径越界: {', '.join(escaped)}")

    try:
        manifest = CorpusManifest.model_validate(_read_json(root / "manifest.json"))
    except Exception as exc:
        if isinstance(exc, CorpusPackageError):
            raise
        raise CorpusPackageError(f"manifest.json 无效: {exc}") from exc

    documents: list[CorpusPackageDocument] = []
    document_ids: set[str] = set()
    for line_number, payload in _iter_jsonl(root / "documents.jsonl"):
        try:
            document = CorpusPackageDocument.model_validate(payload)
        except Exception as exc:
            raise CorpusPackageError(f"documents.jsonl:{line_number} 无效: {exc}") from exc
        if document.id in document_ids:
            raise CorpusPackageError(f"documents.jsonl:{line_number} document id 重复: {document.id}")
        _validate_source_path(root, document.source)
        document_ids.add(document.id)
        documents.append(document)
    if not documents:
        raise CorpusPackageError("documents.jsonl 至少需要一个文档")

    document_position = {document.id: index for index, document in enumerate(documents)}
    seen_unit_ids: dict[str, set[str]] = {document.id: set() for document in documents}
    seen_orders: dict[str, set[int]] = {document.id: set() for document in documents}
    counts = {document.id: 0 for document in documents}
    last_document_position = -1
    last_order = -1
    active_document_id: str | None = None
    unit_count = 0
    char_count = 0
    for line_number, payload in _iter_jsonl(root / "units.jsonl"):
        try:
            unit = CorpusPackageUnit.model_validate(payload)
        except Exception as exc:
            raise CorpusPackageError(f"units.jsonl:{line_number} 无效: {exc}") from exc
        position = document_position.get(unit.document_id)
        if position is None:
            raise CorpusPackageError(
                f"units.jsonl:{line_number} 引用了未知 document_id: {unit.document_id}"
            )
        if position < last_document_position:
            raise CorpusPackageError(
                "units.jsonl 必须按 documents.jsonl 的文档顺序分组，且同一文档不能分散"
            )
        if active_document_id != unit.document_id:
            active_document_id = unit.document_id
            last_document_position = position
            last_order = -1
        if unit.order <= last_order:
            raise CorpusPackageError(
                f"units.jsonl:{line_number} 同一文档的 order 必须严格递增"
            )
        if unit.id in seen_unit_ids[unit.document_id]:
            raise CorpusPackageError(f"units.jsonl:{line_number} unit id 重复: {unit.id}")
        if unit.order in seen_orders[unit.document_id]:
            raise CorpusPackageError(f"units.jsonl:{line_number} unit order 重复: {unit.order}")
        normalized = normalize_unit_text(unit.text)
        if not normalized:
            raise CorpusPackageError(f"units.jsonl:{line_number} text 不能为空")
        seen_unit_ids[unit.document_id].add(unit.id)
        seen_orders[unit.document_id].add(unit.order)
        counts[unit.document_id] += 1
        unit_count += 1
        char_count += len(normalized)
        last_order = unit.order

    empty_documents = [document.id for document in documents if counts[document.id] == 0]
    if empty_documents:
        raise CorpusPackageError(f"文档没有任何 unit: {', '.join(empty_documents[:10])}")
    return ValidatedCorpusPackage(
        root=root,
        manifest=manifest,
        documents=documents,
        unit_count=unit_count,
        char_count=char_count,
    )


def iter_units(root: Path) -> Iterator[CorpusPackageUnit]:
    for line_number, payload in _iter_jsonl(root / "units.jsonl"):
        try:
            yield CorpusPackageUnit.model_validate(payload)
        except Exception as exc:
            raise CorpusPackageError(f"units.jsonl:{line_number} 无效: {exc}") from exc


def _safe_extract_zip(source: Path, destination: Path) -> Path:
    with ZipFile(source) as archive:
        members = archive.infolist()
        if sum(member.file_size for member in members) > settings.corpus_upload_max_bytes:
            raise CorpusPackageError("ZIP 解压后大小超过服务器限制")
        for member in members:
            pure = PurePosixPath(member.filename)
            if pure.is_absolute() or ".." in pure.parts:
                raise CorpusPackageError(f"ZIP 包含非法路径: {member.filename}")
            mode = member.external_attr >> 16
            if mode and (mode & 0o170000) == 0o120000:
                raise CorpusPackageError(f"ZIP 不允许符号链接: {member.filename}")
        archive.extractall(destination)

    candidates = [destination]
    children = [item for item in destination.iterdir() if item.name != "__MACOSX"]
    if len(children) == 1 and children[0].is_dir():
        candidates.insert(0, children[0])
    for candidate in candidates:
        if all((candidate / name).is_file() for name in REQUIRED_PACKAGE_FILES):
            return candidate
    raise CorpusPackageError("ZIP 根目录未找到 manifest.json、documents.jsonl、units.jsonl")


def _decode_txt(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        if "\ufffd" in text or sum(text.count(marker) for marker in _MOJIBAKE_MARKERS) >= 2:
            raise CorpusPackageError("TXT 疑似乱码，请在外部修复编码后制作标准语料包")
        return text
    raise CorpusPackageError("TXT 仅支持 UTF-8 或可严格解码的 GB18030")


def _split_txt(text: str) -> tuple[str, list[tuple[str, str]]]:
    normalized = normalize_unit_text(text)
    lines = normalized.splitlines(keepends=True)
    headings: list[tuple[int, str]] = []
    offset = 0
    for line in lines:
        title = line.strip()
        if len(title) <= 120 and _CHAPTER_HEADING.fullmatch(title):
            headings.append((offset, title))
        offset += len(line)

    if len(headings) < 2:
        if len(normalized) > 200_000:
            raise CorpusPackageError(
                "TXT 章节结构识别置信度不足；请在外部清洗并转换为 openfic-corpus/v1 标准包"
            )
        return "generic", [("正文", normalized)]

    units: list[tuple[str, str]] = []
    for index, (start, title) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(normalized)
        segment = normalized[start:end]
        first_newline = segment.find("\n")
        content = segment[first_newline + 1 :] if first_newline >= 0 else ""
        content = normalize_unit_text(content)
        if len(content) < 20:
            raise CorpusPackageError(
                "TXT 章节结构识别置信度不足；请在外部清洗并转换为 openfic-corpus/v1 标准包"
            )
        units.append((title, content))
    return "novel", units


def _convert_txt_to_package(source: Path, destination: Path) -> Path:
    if source.stat().st_size > TXT_MAX_BYTES:
        raise CorpusPackageError("TXT 便捷导入上限为 100MB；大语料请使用标准语料包")
    text = _decode_txt(source.read_bytes())
    kind, units = _split_txt(text)
    title = source.stem.strip() or "TXT 语料"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": SCHEMA_VERSION,
                "name": title,
                "description": "",
                "tags": [],
                "metadata": {"import_format": "txt"},
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    document_id = "txt-document"
    (destination / "documents.jsonl").write_text(
        json.dumps(
            {
                "id": document_id,
                "kind": kind,
                "title": title,
                "author": None,
                "dynasty": None,
                "tags": [],
                "source": "sources/original.txt",
                "metadata": {"original_filename": source.name},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    with (destination / "units.jsonl").open("w", encoding="utf-8") as stream:
        for index, (unit_title, unit_text) in enumerate(units):
            stream.write(
                json.dumps(
                    {
                        "id": f"unit-{index + 1}",
                        "document_id": document_id,
                        "kind": "chapter" if kind == "novel" else "text",
                        "order": index,
                        "title": unit_title,
                        "volume": None,
                        "text": unit_text,
                        "metadata": {},
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    sources = destination / "sources"
    sources.mkdir()
    shutil.copy2(source, sources / "original.txt")
    return destination


@contextmanager
def prepared_package(source: Path) -> Iterator[ValidatedCorpusPackage]:
    """Yield a validated package directory and remove temporary extraction files."""
    source = source.resolve()
    if not source.exists():
        raise CorpusPackageError(f"导入源不存在: {source}")
    staging_root = settings.corpus_dir / "staging"
    staging_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f"import-{uuid4().hex[:8]}-", dir=staging_root))
    try:
        if source.is_dir():
            root = source
        elif source.suffix.lower() == ".zip":
            root = _safe_extract_zip(source, temporary)
        elif source.suffix.lower() == ".txt":
            root = _convert_txt_to_package(source, temporary / "package")
        else:
            raise CorpusPackageError("仅支持标准语料包目录、.zip 或 .txt")
        yield validate_package(root)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
