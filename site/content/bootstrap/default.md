+++
title = "Defaults"
+++

# Bootstrapping defaults with bron

## Quickstart

{{< bron-bootstrap "b/default.toml" >}}

## Contents

This bootstrap will configure the following tools and their settings:

 - [fonk](/configs/fonk.md)
 - [uv](/configs/uv.md)
 - [bron](/configs/bron.md)
 - [ruff](/configs/ruff.md)
 - [mypy](/configs/mypy.md)
 - [pytest](/configs/pytest.md)

If you're still using poetry and not uv you can use the following bootstrap:

{{< bron-bootstrap "b/default-poetry.toml" >}}

## Source

Note that the `path` entries in the source will be rewritten upon bootstrapping to point to the correct location on the `bron.sh` website.

{{< toml "b/default.toml" >}}
