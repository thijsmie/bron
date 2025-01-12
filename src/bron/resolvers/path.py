from pathlib import Path

from bron.config import Source


def resolve_by_path(project: Path, source: Source) -> str:
    p = Path(source.path)

    if not p.is_absolute():
        p = project.parent / p

    return p.read_text()
