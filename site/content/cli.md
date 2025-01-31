+++
title = "Command Line Interface"
+++

# The command line interface

The `bron` command line interface is the main entry point for interacting with bron. It provides a number of subcommands for managing your project configuration and syncing your tools.

## Subcommands

### `bron bootstrap`

The `bootstrap` subcommand copies sources from a local path or url into your `pyproject.toml` file. By default it will then run a sync, you can supress this with a `--no-sync`. For more info see {{< ref "bootstrap/_index.md" >}}.

Example:

```bash
bron bootstrap --bron-only https://example.com/config.toml
```

### `bron sync`

The `sync` subcommand synchronizes your project configuration with the sources in your `pyproject.toml` file. It will be the most used command in your workflow.

Example:

```bash
bron sync
```

### `bron purge`

The `purge` subcommand removes all sources from your `pyproject.toml` file, including all configuration that still matches those sources. This allows you to easily view what you've added as custom option or configuration that has been removed upstream. You're then in the ideal spot to "re-bootstrap" your project.

Example:

```bash
bron purge
```

### `bron list`

The `list` subcommand lists the sources in your `pyproject.toml` file.

Example:

```bash
bron list
```

### `bron add`

The `add` subcommand adds a source to your `pyproject.toml` file. Mostly for scripting purposes, since editing the toml file by hand is probably more convenient.

Example:

```bash
bron add ruff https://example.com/ruff.toml
bron add mypy ./mypy.toml
```

### `bron remove`

The `remove` subcommand removes a source from your `pyproject.toml` file. Mostly for scripting purposes, since editing the toml file by hand is probably more convenient.

Example:

```bash
bron remove ruff
bron remove mypy
```

### `bron format`

The `format` subcommand formats the configuration in your `pyproject.toml` file.

Example:

```bash
bron format
```
