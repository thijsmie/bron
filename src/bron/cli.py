import sys

import rich

from bron.procedures.format import format_procedure
from bron.procedures.locate import get_pyproject_toml_path
from bron.procedures.sync import sync as sync_procedure
from bron.render import Printer, render_help


def app() -> None:
    runnable: str | None = None
    flags: set[str] = set()

    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            flag = arg[2:]
            if flag in flags:
                rich.print(f"[bold red]Flag {flag} already set.")
                sys.exit(2)
            elif flag in {"help", "check", "quiet"}:
                flags.add(flag)
            else:
                rich.print(f"[bold red]Unknown flag: {flag}")
                sys.exit(2)
        elif runnable is None:
            runnable = arg
        else:
            rich.print(f"[bold red]Unknown argument: {arg}")
            sys.exit(2)

    if runnable is None or "help" in flags:
        render_help()
        sys.exit(0)

    project = get_pyproject_toml_path()
    printer = Printer("quiet" in flags)

    if runnable == "sync":
        sys.exit(sync_procedure(printer, project, check="check" in flags))
    elif runnable == "format":
        sys.exit(format_procedure(printer, project, check="check" in flags))
    else:
        rich.print(f"[bold red]Unknown command: {runnable}")
        sys.exit(2)


if __name__ == "__main__":
    app()
