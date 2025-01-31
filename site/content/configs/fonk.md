+++
title = "fonk"
+++

# Default configuration for fonk

{{< bron-add fonk "c/fonk/default.toml" >}}

Part of the [default setup](/bootstrap/_index.md) this will configure `fonk` as taskrunner.
It will not add any commands, the they will be added by their respective tool configurations, e.g. `mypy` will add a `mypy` command and `typecheck` alias. The `fonk` configuration does add a `all` alias to run all commands that each configuration will add to. Lastly a default command is configured: run the `all` alias in `--fix` mode.

## Source

{{< toml "c/fonk/default.toml" >}}
