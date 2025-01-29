from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


class Printer:
    def __init__(self, quiet: bool) -> None:
        self.quiet = quiet
        self.console = Console()

    def print(self, message: str) -> None:
        if not self.quiet:
            self.console.print(message)


def render_help() -> None:
    console = Console()

    commands = Table(
        "[bold green]Commands:",
        "",
        box=None,
        pad_edge=False,
        header_style="",
    )

    commands.add_row(" [bold]•[/] [cyan]sync[/]", "[italic]Synchronise your pyproject.toml with your bron sources.")
    commands.add_row(" [bold]•[/] [cyan]format[/]", "[italic]Format your pyproject.toml.")

    flags = Table(
        "[bold green]Flags:",
        "",
        box=None,
        pad_edge=False,
        header_style="",
    )

    flags.add_row(
        " [bold]•[/] [yellow]--check",
        "[italic] Run sync/format in check mode, e.g. yield exit code 1 if changes would be made.",
    )
    flags.add_row(
        " [bold]•[/] [yellow]--help",
        "[italic] Print this help and exit.",
    )

    help_data = Group(
        Markdown("*Sync your `pyproject.toml` with upstream sources*"),
        "",
        "[bold green]Usage:[/][cyan] bron sync/format [/][yellow]\\[--check]",
        "",
        commands,
        "",
        flags,
        "",
    )

    console.print(
        Panel(
            help_data,
            title=("[bold cyan]⛲ Bron ⛲"),
            expand=True,
        )
    )
