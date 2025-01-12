from pathlib import Path

from pytoml11 import Table, dump, load, loads

from bron.config import load_config
from bron.procedures.merge import merge_pyproject
from bron.resolvers.path import resolve_by_path
from bron.resolvers.url import resolve_by_url


def sync(project: Path) -> None:
    doc = load(str(project))
    config = load_config(doc)

    update = Table({})

    for source in config.sources:
        if source.url:
            source_doc = loads(resolve_by_url(project, source.url))
        elif source.path:
            source_doc = loads(resolve_by_path(project, Path(source.path)))
        else:
            raise ValueError("Source must have either a URL or a path")

        merge_pyproject(update, source_doc)

    merge_pyproject(doc, update)
    dump(doc, str(project))
