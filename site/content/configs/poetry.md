+++
title = "poetry"
+++

# Default configuration for poetry

{{< bron-add bron "c/poetry/default.toml" >}}

While `poetry` is not the default package manager used with `bron` it does work. This configuration will add lockfile checking task to the `fonk` taskrunner. This task is added to the `all` alias.

## Source

{{< toml "c/poetry/default.toml" >}}
