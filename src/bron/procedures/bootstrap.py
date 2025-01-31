import re
from pathlib import Path

from httpx import URL
from pytoml11 import String, dumps, load

from bron.logic.checker import run_document_check
from bron.logic.merge import MergeOptions, merge_pyproject, merge_regular
from bron.logic.resolve import resolve, resolve_relative_source
from bron.render import Printer


def bootstrap_procedure(printer: Printer, project: Path, source: str, bron_only: bool) -> int:
    src = URL(source) if re.match(r"https?://", source) else Path(source)
    doc = load(str(project))
    run_document_check(doc)
    relative_to, bootstrap_source = resolve(printer, project.parent, src)
    run_document_check(bootstrap_source)

    # We need to rewrite the urls/paths in the bootstrap source to be relative to their original file

    for new_source in bootstrap_source["tool"]["bron"]["sources"].value.values():
        if "url" in new_source:
            new_source["url"] = String(str(resolve_relative_source(relative_to, URL(new_source["url"].value))))
        elif "path" in new_source:
            original_path = Path(new_source["path"].value)
            resolved_path = resolve_relative_source(relative_to, original_path)

            # resolved_path will be absolute but it might be a path that is relative to the original file
            # in that case we will make it relative to the project root

            if (
                isinstance(resolved_path, Path)
                and resolved_path.is_absolute()
                and project.parent in resolved_path.parents
            ):
                new_source["path"] = String(str(resolved_path.relative_to(project.parent)))
            elif isinstance(resolved_path, URL):
                del new_source["path"]
                new_source["url"] = String(str(resolved_path))
            else:
                new_source["path"] = String(str(resolved_path))

    if bron_only:
        merge_regular(
            doc["tool"]["bron"],
            bootstrap_source["tool"]["bron"],
            ("tool", "bron"),
            MergeOptions(merge_arrays=False, merge_bron=True),
        )
    else:
        merge_pyproject(doc, bootstrap_source, MergeOptions(merge_arrays=False, merge_bron=True))

    new_pyproject = dumps(doc)
    project.write_text(new_pyproject)
    printer.print(f"[bold blue]⛲ Bootstrapped using {source}")
    return 0
