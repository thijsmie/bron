import typer
from pathlib import Path
from pytoml11 import dump, load
from tomly.procedures.merge import merge_pyproject

app = typer.Typer()


@app.command()
def format(directory: Path = Path('.')) -> None:
    print(f"Formatting {directory}!")


@app.command()
def sync(directory: Path = Path('.')) -> None:
    print(f"Syncing {directory}!")


@app.command()
def merge(base: Path, update: Path, output: Path) -> None:
    base_item = load(str(base))
    update_item = load(str(update))
    merged_item = merge_pyproject(base_item, update_item)
    dump(merged_item, str(output))


if __name__ == "__main__":
    app()
