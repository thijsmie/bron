from pathlib import Path

from httpx import URL
from pytoml11 import Item, String, Table

from bron.exceptions import BronError


def _check_subtable(document: Table, key: str) -> None:
    if key not in document:
        document[key] = Table({})
    elif not isinstance(document[key], Table):
        raise BronError(f"[{key}] is not a table")


def _check_is_url(value: Item, source: int) -> None:
    if not isinstance(value, String):
        raise BronError(f"[tool.bron.sources.{source}.url] is not a string")
    try:
        URL(value.value)
    except ValueError:
        raise BronError(f"[tool.bron.sources.{source}.url] is not a valid URL")


def _check_is_path(value: Item, source: str) -> None:
    if not isinstance(value, String):
        raise BronError(f"[tool.bron.sources.{source}.path] is not a string")
    try:
        Path(value.value)
    except (FileNotFoundError, ValueError):
        raise BronError(f"[tool.bron.sources.{source}.path] does not exist")


def run_document_check(document: Item) -> None:
    if not isinstance(document, Table):
        raise BronError("Document is not a table")

    _check_subtable(document, "tool")
    _check_subtable(document["tool"], "bron")
    _check_subtable(document["tool"]["bron"], "sources")

    for source_name, source in document["tool"]["bron"]["sources"].value.items():
        _check_subtable(document["tool"]["bron"]["sources"], source_name)

        if "url" in source:
            _check_is_url(source["url"], source_name)
        elif "path" in source:
            _check_is_path(source["path"], source_name)
        else:
            raise BronError(f"[tool.bron.sources.{source_name}] must have either a url or a path")
