from pathlib import Path

import httpx


def resolve_by_url(project: Path, source: str) -> str:
    response = httpx.get(source)
    response.raise_for_status()
    return response.text
