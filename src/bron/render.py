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
    commands.add_row(
        " [bold]•[/] [cyan]bootstrap[/] <source>", "[italic]Bootstrap your bron configuration with predefined sources."
    )
    commands.add_row(
        " [bold]•[/] [cyan]purge[/]",
        "[italic]Purge bron from your pyproject.toml including all matching upstream configuration.",
    )
    commands.add_row(" [bold]•[/] [cyan]add[/] <name> <source>", "[italic]Add a new source to your bron configuration.")
    commands.add_row(" [bold]•[/] [cyan]remove[/] <name>", "[italic]Remove a source from your bron configuration.")
    commands.add_row(" [bold]•[/] [cyan]list[/]", "[italic]List all sources in your bron configuration.")

    flags = Table(
        "[bold green]Flags:",
        "",
        box=None,
        pad_edge=False,
        header_style="",
    )

    flags.add_row(
        " [bold]•[/] [yellow]--check",
        "[italic] (only for format/sync) Run in check mode, e.g. yield exit code 1 if changes would be made.",
    )
    flags.add_row(
        " [bold]•[/] [yellow]--quiet",
        "[italic] Suppress all output.",
    )
    flags.add_row(
        " [bold]•[/] [yellow]--help",
        "[italic] Print this help and exit.",
    )
    flags.add_row(
        " [bold]•[/] [yellow]--bron-only",
        "[italic] (only for bootstrapping) Only merge the bron section of the bootstrap source.",
    )
    flags.add_row(
        " [bold]•[/] [yellow]--no-sync",
        "[italic] (only for bootstrapping) Do not sync after bootstrapping.",
    )

    help_data = Group(
        Markdown("*Sync your `pyproject.toml` with upstream sources*"),
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
