from pathlib import Path

from pytoml11 import dumps, load

from bron.render import Printer


def remove_procedure(printer: Printer, project: Path, name: str) -> int:
    doc = load(str(project))

    if "tool" not in doc:
        return 2
    if "bron" not in doc["tool"]:
        return 2
    if "sources" not in doc["tool"]["bron"]:
        return 2
    if name not in doc["tool"]["bron"]["sources"]:
        return 2

    del doc["tool"]["bron"]["sources"][name]

    new_pyproject = dumps(doc)
    project.write_text(new_pyproject)
    printer.print(f"[bold blue]⛲ Removed {name}")
    return 0
