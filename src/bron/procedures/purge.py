from pathlib import Path

from pytoml11 import dumps, load

from bron.config import load_config
from bron.logic.checker import run_document_check
from bron.logic.erase import erase
from bron.logic.update import construct_update_document
from bron.render import Printer


def purge_procedure(printer: Printer, project: Path, check: bool) -> int:
    doc = load(str(project))
    run_document_check(doc)
    config = load_config(doc)
    update = construct_update_document(printer, project, config)

    erase(doc, update)
    del doc["tool"]["bron"]

    new_pyproject = dumps(doc)
    old_pyproject = project.read_text()

    if new_pyproject == old_pyproject:
        printer.print("[bold blue]⛲ No changes to pyproject.toml")
        return 0

    if check:
        printer.print("[bold red]⛲ Would change pyproject.toml")
        return 1

    project.write_text(new_pyproject)
    printer.print("[bold blue]⛲ Purged bron from pyproject.toml")
    return 0
