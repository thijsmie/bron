from pathlib import Path

from httpx import URL, get
from pytoml11 import Table, loads

from bron.render import Printer


def _read_url_text(printer: Printer, url: URL) -> str:
    printer.print(f"[bright_black]Fetching remote {url}")
    response = get(url)
    response.raise_for_status()
    return response.text


def _read_path_text(printer: Printer, path: Path) -> str:
    printer.print(f"[bright_black]Fetching local {path}")
    return path.read_text()


def _parent_url(url: URL) -> URL:
    path = url.path.rsplit("/", 1)[0]
    return URL(
        scheme=url.scheme,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        path=path,
        query=url.query,
        fragment=url.fragment,
    )


def _read_source(printer: Printer, resolved_source: Path | URL) -> str:
    if isinstance(resolved_source, Path):
        return _read_path_text(printer, resolved_source)

    return _read_url_text(printer, resolved_source)


def parent_of(source: Path | URL) -> Path | URL:
    if isinstance(source, Path):
        return source.parent

    return _parent_url(source)


def resolve_relative_source(relative_to: Path | URL, source: Path | URL) -> Path | URL:
    if isinstance(source, Path) and source.is_absolute():
        return source

    if isinstance(source, URL) and source.is_absolute_url:
        return source

    if isinstance(source, URL) and isinstance(relative_to, URL):
        return relative_to.join(source)

    if isinstance(source, Path) and isinstance(relative_to, Path):
        return relative_to / source

    if isinstance(source, Path) and isinstance(relative_to, URL):
        return relative_to.join(str(source))

    if isinstance(source, URL) and isinstance(relative_to, Path):
        # Relative url but absolute path?
        # Bit of a weird case, but let's handle it
        return relative_to / source.path

    raise ValueError("Invalid source or relative_to")


def resolve(printer: Printer, relative_to: Path | URL, source: Path | URL) -> tuple[Path | URL, Table]:
    resolved_source = resolve_relative_source(relative_to, source)
    source_contents = _read_source(printer, resolved_source)
    return parent_of(resolved_source), loads(source_contents)
