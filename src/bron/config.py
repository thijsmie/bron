from dataclasses import dataclass

from pytoml11 import Table


@dataclass
class Source:
    name: str
    url: str | None
    path: str | None


@dataclass
class SyncConfig:
    sources: list[Source]


def load_config(config: Table) -> SyncConfig:
    try:
        sources = []
        for name, source in config["tool"]["bron"]["source"].value.items():
            sources.append(
                Source(
                    name=name,
                    url=source["url"].value if "url" in source else None,
                    path=source["path"].value if "path" in source else None,
                )
            )
        return SyncConfig(sources=sources)
    except KeyError:
        return SyncConfig(sources=[])
