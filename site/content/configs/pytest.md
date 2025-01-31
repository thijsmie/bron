+++
title = "pytest"
+++

# Default configuration for pytest

{{< bron-add bron "c/pytest/default.toml" >}}

Part of the [default setup](/bootstrap/_index.md) this will configure `pytest` as test runner. It will add a `pytest` command and `test` alias to the `fonk` taskrunner. It will also add the plugin `pytest-cov` to generate coverage reports.

## Source

{{< toml "c/pytest/default.toml" >}}
