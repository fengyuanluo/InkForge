import json
from pathlib import Path

import pytest

from app.corpus.package import (
    CorpusPackageError,
    iter_units,
    validate_package,
)


def write_package(
    root: Path,
    *,
    text: str = "  山有木兮木有枝  \n心悦君兮君不知  ",
    source: str | None = "sources/work.txt",
) -> Path:
    root.mkdir(parents=True)
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "openfic-corpus/v1",
                "name": "精品语料",
                "tags": ["poetry"],
                "metadata": {},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (root / "documents.jsonl").write_text(
        json.dumps(
            {
                "id": "work-1",
                "kind": "poetry",
                "title": "越人歌",
                "author": None,
                "dynasty": "先秦",
                "tags": ["诗歌"],
                "source": source,
                "metadata": {},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "units.jsonl").write_text(
        json.dumps(
            {
                "id": "poem-1",
                "document_id": "work-1",
                "kind": "poem",
                "order": 0,
                "title": "越人歌",
                "volume": None,
                "text": text,
                "metadata": {},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    if source is not None and source.startswith("sources/"):
        source_path = root / source
        source_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.write_text(text, encoding="utf-8")
    return root


def test_validate_package_preserves_literary_whitespace(tmp_path: Path) -> None:
    text = "  山有木兮木有枝  \r\n心悦君兮君不知  \n"
    package = validate_package(write_package(tmp_path / "corpus", text=text))

    unit = next(iter_units(package.root))

    assert package.unit_count == 1
    assert package.char_count == len("  山有木兮木有枝  \n心悦君兮君不知  ")
    assert unit.text == text


@pytest.mark.parametrize("source", ["../secret.txt", "/etc/passwd", "work.txt"])
def test_validate_package_rejects_invalid_source_paths(
    tmp_path: Path, source: str
) -> None:
    root = write_package(tmp_path / "corpus", source=source)

    with pytest.raises(CorpusPackageError, match="source"):
        validate_package(root)


def test_validate_package_rejects_source_symlink_escape(tmp_path: Path) -> None:
    root = write_package(tmp_path / "corpus", source=None)
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "work.txt").write_text("secret", encoding="utf-8")
    (root / "sources").symlink_to(outside, target_is_directory=True)
    payload = json.loads((root / "documents.jsonl").read_text(encoding="utf-8"))
    payload["source"] = "sources/work.txt"
    (root / "documents.jsonl").write_text(
        json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    with pytest.raises(CorpusPackageError, match="source"):
        validate_package(root)
