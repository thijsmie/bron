---
title: Introduction
type: docs
---

# Introduction

`bron` is a tool to synchronise settings between all your projects that have a `pyproject.toml` file. This helps a lot if you use common python tooling like `ruff`, `mypy`, `pyright` and others that keep their settings in a `pyproject.toml` file. `bron` will keep all these settings in sync between all your projects in the multi-repo setup.

## Quickstart

Bootstrap common configuration into your `pyproject.toml` file if your project is setup to use `uv`:

{{< bron-bootstrap "b/default.toml" >}}

Syncronize your settings:

```bash
uvx bron sync
```

Check if your settings are in sync (for your CI pipeline):

```bash
uvx bron sync --check
```

Run all the tools with taskrunner [`fonk`](https://github.com/thijsmie/fonk):

```bash
uvx fonk
```
