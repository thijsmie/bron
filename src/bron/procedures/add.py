import re
from pathlib import Path

from httpx import URL
from pytoml11 import String, Table, dumps, load

from bron.logic.checker import run_document_check
from bron.render import Printer


def add_procedure(printer: Printer, project: Path, name: str, source: str) -> int:
    src = URL(source) if re.match(r"https?://", source) else Path(source)
    doc = load(str(project))
    run_document_check(doc)

    if name in doc["tool"]["bron"]["sources"]:
        printer.print(f"[bold red]⛲ {name} already exists")
        return 1

    doc["tool"]["bron"]["sources"][name] = (
        Table({"url": String(source)}) if isinstance(src, URL) else Table({"path": String(source)})
    )

    new_pyproject = dumps(doc)
    project.write_text(new_pyproject)
    printer.print(f"[bold blue]⛲ Added {name}")
    return 0
