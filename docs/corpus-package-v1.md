# InkForge Corpus Package v1

The standard package is a directory, or a ZIP containing that directory:

```text
manifest.json
documents.jsonl
units.jsonl
sources/          # optional original files
```

## Manifest

```json
{
  "schema_version": "openfic-corpus/v1",
  "name": "Library name",
  "description": "Optional description",
  "tags": ["fiction"],
  "metadata": {}
}
```

## Documents

`documents.jsonl` contains one JSON object per line:

```json
{"id":"book-1","kind":"novel","title":"Title","author":"Author","dynasty":null,"tags":[],"source":"sources/book-1.txt","metadata":{}}
```

`kind` is `novel`, `poetry`, or `generic`. `source` is optional and, when set,
must be a relative path below `sources/`.

## Units

`units.jsonl` contains the searchable units. Units must be grouped in the same
document order as `documents.jsonl`; each document's `order` must be unique and
strictly increasing.

```json
{"id":"chapter-1","document_id":"book-1","kind":"chapter","order":0,"title":"Chapter 1","volume":null,"text":"...","metadata":{}}
```

`kind` is `chapter`, `poem`, `ci`, `section`, or `text`. All files must use
UTF-8. Prepare complex cleanup, encoding repair, metadata extraction, and
structure parsing before creating the package.

Validate a package without starting InkForge:

```bash
python tools/validate_corpus_package.py /path/to/package-or.zip
```
