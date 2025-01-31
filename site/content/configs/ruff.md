+++
title = "ruff"
+++

# Default configuration for ruff

{{< bron-add bron "c/ruff/default.toml" >}}

Part of the [default setup](/bootstrap/_index.md) this will configure `ruff` as formatter and linter. It will add a `ruff-format` and `ruff-check` command and `format` alias to the `fonk` taskrunner.

## Source

{{< toml "c/ruff/default.toml" >}}
