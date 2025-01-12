from pathlib import Path


def resolve_by_path(project: Path, source: Path) -> str:
    if not source.is_absolute():
        source = project.parent / source

    return source.read_text()
