from pathlib import Path


def get_pyproject_toml_path() -> Path:
    directory = Path().resolve()

    while directory != directory.parent:
        pyproject_toml = directory / "pyproject.toml"
        if pyproject_toml.exists():
            return pyproject_toml
        directory = directory.parent

    raise FileNotFoundError("pyproject.toml not found")
