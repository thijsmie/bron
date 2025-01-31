import sys
from argparse import ArgumentError, ArgumentParser, ArgumentTypeError
from typing import Literal, NamedTuple

import rich
from rich.markup import escape

from bron.exceptions import BronError
from bron.logic.locate import get_pyproject_toml_path
from bron.procedures.add import add_procedure
from bron.procedures.bootstrap import bootstrap_procedure
from bron.procedures.format import format_procedure
from bron.procedures.list import list_procedure
from bron.procedures.purge import purge_procedure
from bron.procedures.remove import remove_procedure
from bron.procedures.sync import sync_procedure
from bron.render import Printer, render_help


class _Namespace(NamedTuple):
    command: Literal["sync", "format", "bootstrap", "add", "remove", "list", "purge"]
    help: bool
    check: bool
    quiet: bool
    source: str
    bron_only: bool
    name: str
    no_sync: bool


def _make_cli_parser() -> ArgumentParser:
    p = ArgumentParser(add_help=False, exit_on_error=False)
    p.add_argument("--help", action="store_true")
    p.add_argument("--quiet", action="store_true")

    sub = p.add_subparsers(dest="command")
    sync = sub.add_parser("sync")
    sync.add_argument("--check", action="store_true")

    format_cmd = sub.add_parser("format")
    format_cmd.add_argument("--check", action="store_true")

    purge = sub.add_parser("purge")
    purge.add_argument("--check", action="store_true")

    bootstrap = sub.add_parser("bootstrap")
    bootstrap.add_argument("source")
    bootstrap.add_argument("--bron-only", action="store_true")
    bootstrap.add_argument("--no-sync", action="store_true")

    add = sub.add_parser("add")
    add.add_argument("name")
    add.add_argument("source")

    remove = sub.add_parser("remove")
    remove.add_argument("name")

    sub.add_parser("list")

    return p


def _run_procedure(printer: Printer, args: _Namespace) -> int:
    project = get_pyproject_toml_path()

    match args.command:
        case "sync":
            code = sync_procedure(printer, project, check=args.check)
        case "format":
            code = format_procedure(printer, project, check=args.check)
        case "bootstrap":
            code = bootstrap_procedure(printer, project, args.source, args.bron_only)
            if code == 0 and not args.no_sync:
                code = sync_procedure(printer, project, check=False)
        case "purge":
            code = purge_procedure(printer, project, check=args.check)
        case "add":
            code = add_procedure(printer, project, args.name, args.source)
        case "remove":
            code = remove_procedure(printer, project, args.name)
        case "list":
            code = list_procedure(printer, project)

    return code


def app() -> None:
    try:
        args: _Namespace = _make_cli_parser().parse_args()  # type: ignore
    except ArgumentError as e:
        rich.print(f"[bold red]{e}")
        sys.exit(2)
    except ArgumentTypeError as e:
        rich.print(f"[bold red]{e}")
        sys.exit(2)

    if args.help or not args.command:
        render_help()
        sys.exit(0)

    printer = Printer(args.quiet)

    try:
        code = _run_procedure(printer, args)
    except BronError as e:
        printer.print(f"[bold red]{escape(str(e))}")
        sys.exit(1)

    sys.exit(code)


if __name__ == "__main__":
    app()
