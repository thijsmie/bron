+++
title = "uv"
+++

# Default configuration for uv

{{< bron-add bron "c/uv/locktask.toml" >}}

Part of the [default setup](/bootstrap/_index.md). This will add a `uv-lock` task to the `fonk` taskrunner. This task checks if the `uv.lock` file is up to date with your `pyproject.toml` file. In `--fix` mode it will update the `uv.lock` file if needed.

## Source

{{< toml "c/uv/locktask.toml" >}}
