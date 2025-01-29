from pathlib import Path

from pytoml11 import dumps, load

from bron.render import Printer


def format_procedure(printer: Printer, project: Path, check: bool) -> int:
    doc = load(str(project))

    new_pyproject = dumps(doc)
    old_pyproject = project.read_text()

    if new_pyproject == old_pyproject:
        printer.print("[bold blue]⛲ No changes to pyproject.toml")
        return 0

    if check:
        printer.print("[bold red]⛲ Would format pyproject.toml")
        return 1

    project.write_text(new_pyproject)
    printer.print("[bold blue]⛲ Formatted pyproject.toml")
    return 0
