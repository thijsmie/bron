from bron.procedures.locate import get_pyproject_toml_path
from bron.procedures.sync import sync as sync_procedure


def app() -> None:
    pyproject = get_pyproject_toml_path()
    sync_procedure(pyproject)


if __name__ == "__main__":
    app()
