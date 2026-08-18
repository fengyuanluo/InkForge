#!/usr/bin/env python3
"""Validate an OpenFic corpus v1 directory or ZIP using only the standard library."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile
from typing import Any, Iterator
from zipfile import ZipFile


SCHEMA_VERSION = "openfic-corpus/v1"
DOCUMENT_KINDS = {"novel", "poetry", "generic"}
UNIT_KINDS = {"chapter", "poem", "ci", "section", "text"}
REQUIRED = {"manifest.json", "documents.jsonl", "units.jsonl"}


class PackageError(ValueError):
    pass


def _object(value: Any, location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PackageError(f"{location}: expected JSON object")
    return value


def _text(value: Any, location: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise PackageError(f"{location}: expected non-empty string")
    return value


def _string_list(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise PackageError(f"{location}: expected string array")
    return value


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError(f"{path.name}: invalid UTF-8 JSON: {exc}") from exc


def _jsonl(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    try:
        stream = path.open("r", encoding="utf-8")
    except OSError as exc:
        raise PackageError(f"{path.name}: {exc}") from exc
    with stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                yield number, _object(json.loads(line), f"{path.name}:{number}")
            except json.JSONDecodeError as exc:
                raise PackageError(f"{path.name}:{number}: invalid JSON: {exc.msg}") from exc


@contextmanager
def _package_root(source: Path) -> Iterator[Path]:
    if source.is_dir():
        yield source.resolve()
        return
    if source.suffix.lower() != ".zip" or not source.is_file():
        raise PackageError("source must be a package directory or .zip")
    with tempfile.TemporaryDirectory(prefix="openfic-corpus-validate-") as temp:
        root = Path(temp)
        with ZipFile(source) as archive:
            for member in archive.infolist():
                pure = PurePosixPath(member.filename)
                if pure.is_absolute() or ".." in pure.parts:
                    raise PackageError(f"unsafe ZIP path: {member.filename}")
                mode = member.external_attr >> 16
                if mode and (mode & 0o170000) == 0o120000:
                    raise PackageError(f"ZIP symlink is not allowed: {member.filename}")
            archive.extractall(root)
        children = [item for item in root.iterdir() if item.name != "__MACOSX"]
        candidates = ([children[0]] if len(children) == 1 and children[0].is_dir() else []) + [root]
        package = next(
            (candidate for candidate in candidates if all((candidate / name).is_file() for name in REQUIRED)),
            None,
        )
        if package is None:
            raise PackageError("ZIP root does not contain the required package files")
        yield package


def validate(root: Path) -> dict[str, Any]:
    missing = sorted(name for name in REQUIRED if not (root / name).is_file())
    if missing:
        raise PackageError(f"missing files: {', '.join(missing)}")
    manifest = _object(_read_json(root / "manifest.json"), "manifest.json")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise PackageError(f"manifest.json: schema_version must be {SCHEMA_VERSION}")
    name = _text(manifest.get("name"), "manifest.json.name")
    _string_list(manifest.get("tags", []), "manifest.json.tags")
    if not isinstance(manifest.get("metadata", {}), dict):
        raise PackageError("manifest.json.metadata: expected object")

    documents: list[str] = []
    document_sources: list[str] = []
    for number, item in _jsonl(root / "documents.jsonl"):
        location = f"documents.jsonl:{number}"
        document_id = _text(item.get("id"), f"{location}.id")
        assert document_id is not None
        if document_id in documents:
            raise PackageError(f"{location}: duplicate document id {document_id}")
        if item.get("kind") not in DOCUMENT_KINDS:
            raise PackageError(f"{location}.kind: unsupported value")
        _text(item.get("title"), f"{location}.title")
        _text(item.get("author"), f"{location}.author", optional=True)
        _text(item.get("dynasty"), f"{location}.dynasty", optional=True)
        _string_list(item.get("tags", []), f"{location}.tags")
        if not isinstance(item.get("metadata", {}), dict):
            raise PackageError(f"{location}.metadata: expected object")
        source = _text(item.get("source"), f"{location}.source", optional=True)
        if source:
            pure = PurePosixPath(source)
            if pure.is_absolute() or ".." in pure.parts or not pure.parts or pure.parts[0] != "sources":
                raise PackageError(f"{location}.source: must be a safe path below sources/")
            if not (root / Path(*pure.parts)).is_file():
                raise PackageError(f"{location}.source: file not found")
            document_sources.append(source)
        documents.append(document_id)
    if not documents:
        raise PackageError("documents.jsonl: at least one document is required")

    positions = {document_id: index for index, document_id in enumerate(documents)}
    unit_ids = {document_id: set() for document_id in documents}
    orders = {document_id: set() for document_id in documents}
    counts = {document_id: 0 for document_id in documents}
    chars = 0
    last_position = -1
    active_document: str | None = None
    last_order = -1
    for number, item in _jsonl(root / "units.jsonl"):
        location = f"units.jsonl:{number}"
        unit_id = _text(item.get("id"), f"{location}.id")
        document_id = _text(item.get("document_id"), f"{location}.document_id")
        assert unit_id is not None and document_id is not None
        position = positions.get(document_id)
        if position is None:
            raise PackageError(f"{location}: unknown document_id {document_id}")
        if position < last_position:
            raise PackageError("units.jsonl: units must be grouped in documents.jsonl order")
        if active_document != document_id:
            active_document = document_id
            last_position = position
            last_order = -1
        order = item.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 0:
            raise PackageError(f"{location}.order: expected non-negative integer")
        if order <= last_order or order in orders[document_id]:
            raise PackageError(f"{location}.order: must be unique and strictly increasing")
        if unit_id in unit_ids[document_id]:
            raise PackageError(f"{location}: duplicate unit id {unit_id}")
        if item.get("kind") not in UNIT_KINDS:
            raise PackageError(f"{location}.kind: unsupported value")
        text = _text(item.get("text"), f"{location}.text")
        if not isinstance(item.get("metadata", {}), dict):
            raise PackageError(f"{location}.metadata: expected object")
        unit_ids[document_id].add(unit_id)
        orders[document_id].add(order)
        counts[document_id] += 1
        chars += len(text or "")
        last_order = order
    empty = [document_id for document_id, count in counts.items() if count == 0]
    if empty:
        raise PackageError(f"documents without units: {', '.join(empty[:10])}")
    return {
        "schema_version": SCHEMA_VERSION,
        "name": name,
        "documents": len(documents),
        "units": sum(counts.values()),
        "characters": chars,
        "source_files": len(set(document_sources)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="package directory or ZIP")
    args = parser.parse_args()
    try:
        with _package_root(args.source) as root:
            summary = validate(root)
    except (PackageError, OSError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"valid": True, **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
