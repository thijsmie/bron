from collections import deque
from pathlib import Path

from pytoml11 import Table, dumps, load

from bron.config import load_config
from bron.procedures.merge import merge_pyproject
from bron.procedures.resolve import resolve
from bron.render import Printer


def sync(printer: Printer, project: Path, check: bool) -> int:
    doc = load(str(project))
    config = load_config(doc)

    sources = deque(config.sources)
    in_queue = {source.name for source in sources}
    docs: list[Table] = []

    while sources:
        source = sources.popleft()
        source_doc = resolve(project, source.location)

        for extra_source in load_config(source_doc).sources:
            if extra_source.name not in in_queue:
                sources.append(extra_source)
                in_queue.add(extra_source.name)

        docs.append(source_doc)

    update = Table({})
    for source_doc in docs[::-1]:
        merge_pyproject(update, source_doc, True)

    merge_pyproject(doc, update, False)

    new_pyproject = dumps(doc)
    old_pyproject = project.read_text()

    if new_pyproject == old_pyproject:
        printer.print("[bold blue]⛲ No changes to pyproject.toml")
        return 0

    if check:
        printer.print("[bold red]⛲ Would change pyproject.toml")
        return 1

    project.write_text(new_pyproject)
    printer.print("[bold blue]⛲ Synced pyproject.toml")
    return 0
