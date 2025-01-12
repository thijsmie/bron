from pathlib import Path

import httpx

from bron.config import Source


def resolve_by_url(project: Path, source: Source) -> str:
    response = httpx.get(source.url)
    response.raise_for_status()
    return response.text
