from pathlib import Path

from httpx import URL, get
from pytoml11 import Table, loads


def _read_url_text(url: URL) -> str:
    response = get(url)
    response.raise_for_status()
    return response.text


def _resolve(relative_to: Path | URL, source: Path | URL) -> str:
    if isinstance(source, Path) and source.is_absolute():
        return source.read_text()

    if isinstance(source, URL) and source.is_absolute_url:
        return _read_url_text(source)

    if isinstance(source, URL) and isinstance(relative_to, URL):
        return _read_url_text(relative_to.join(source))

    if isinstance(source, Path) and isinstance(relative_to, Path):
        return (relative_to.parent / source).read_text()

    if isinstance(source, Path) and isinstance(relative_to, URL):
        return _read_url_text(relative_to.join(str(source)))

    if isinstance(source, URL) and isinstance(relative_to, Path):
        # Relative url but absolute path?
        # Bit of a weird case, but let's handle it
        return (relative_to / str(source)).read_text()

    raise ValueError("Invalid source or relative_to")


def resolve(project: Path, source: Path | URL) -> Table:
    return loads(_resolve(project, source))
