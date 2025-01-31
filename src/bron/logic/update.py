from collections import deque
from pathlib import Path

from httpx import URL
from pytoml11 import Table

from bron.config import Source, SyncConfig, load_config
from bron.logic.checker import run_document_check
from bron.logic.merge import MergeOptions, merge_pyproject
from bron.logic.resolve import resolve
from bron.render import Printer


def construct_update_document(printer: Printer, project: Path, config: SyncConfig) -> Table:
    sources: deque[tuple[Path | URL, Source]] = deque((project.parent, c) for c in config.sources)
    in_queue = {source.name for _, source in sources}
    docs: list[Table] = []

    while sources:
        relative_to, source = sources.popleft()
        new_relative_to, source_doc = resolve(printer, relative_to, source.location)
        run_document_check(source_doc)

        for extra_source in load_config(source_doc).sources:
            if extra_source.name not in in_queue:
                sources.append((new_relative_to, extra_source))
                in_queue.add(extra_source.name)

        docs.append(source_doc)

    update = Table({})
    for source_doc in docs[::-1]:
        merge_pyproject(update, source_doc, MergeOptions(merge_arrays=True, merge_bron=False))

    return update
