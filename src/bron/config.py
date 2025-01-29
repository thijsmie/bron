from dataclasses import dataclass
from pathlib import Path

from httpx import URL
from pytoml11 import Table

from bron.exceptions import BronConfigError


@dataclass
class Source:
    name: str
    location: URL | Path


@dataclass
class SyncConfig:
    sources: list[Source]


def load_config(config: Table) -> SyncConfig:
    sources: list[Source] = []

    for source in config.get("tool", {}).get("bron", {}).get("sources", Table({})).value.items():
        if "name" not in source:
            raise BronConfigError("Source must have a name")

        if "url" in source:
            sources.append(
                Source(
                    name=source["name"],
                    location=URL(source["url"].value),
                )
            )
        elif "path" in source:
            sources.append(
                Source(
                    name=source["name"],
                    location=Path(source["path"].value),
                )
            )
        else:
            raise BronConfigError(f"Source must have either a URL or a path, {source["name"]} does not")

    return SyncConfig(sources=sources)
