from pathlib import Path

from pytoml11 import load

from bron.config import load_config
from bron.render import Printer


def list_procedure(printer: Printer, project: Path) -> int:
    doc = load(str(project))
    config = load_config(doc)

    for source in config.sources:
        printer.print(f"[bold blue]{source.name}: {source.location}")

    return 0
