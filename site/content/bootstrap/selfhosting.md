+++
title = "Selfhosting"
+++

# Hosting your own bron bootstrap

While bron can be used with what we offer on this site, you probably want to host your own configuration. Any toml file can be used as the source of your configuration, as long as you have a resolvable url or path to it. 

## Using a master project

If you have a project that you want to use as the master configuration, you can use the `--bron-only` flag to only copy the bron configuration. This will copy the configuration from the source directly to your pyproject.toml file including all the sources contained within. For example if we have a repo `thijsmie/project` with the following structure:

 - 📁 configs
    - 📄 uv.toml
    - 📄 ruff.toml
 - 📄 pyproject.toml

And the following content is present in `pyproject.toml`:

```toml
[tool.bron.sources.ruff]
path = "./configs/ruff.toml"

[tool.bron.sources.uv]
path = "./configs/uv.toml"
```

We can configure a new project with the following command:

```bash
uvx bron bootstrap --bron-only https://github.com/thijsmie/project/blob/main/pyproject.toml
```

Our new project will now contain the following configuration:

```toml
[tool.bron.sources.ruff]
url = "https://github.com/thijsmie/project/blob/main/configs/ruff.toml"

[tool.bron.sources.uv]
url = "https://github.com/thijsmie/project/blob/main/configs/uv.toml"
```

## Using a github gist

You can also maintain a [github gist](https://gist.github.com/) with your configuration. This is a great way to share your configuration with others. Say you have a gist with the following `config.toml` content:

```toml
[dependency-groups]
dev = ["ruff"]

[tool.ruff]
line-length = 120
target-version = "py313"
```

You can use the following command to your project with this configuration:

```bash
uvx bron add gist https://gist.githubusercontent.com/{user}/{gist_hash}/raw/config.toml
```

## Put it on a network drive

In corporate environments it's common to have a network drive where you can store your configuration. You can use the following command to add a network drive as a source:

```bash
uvx bron add network-drive N://server/share/config.toml
```

## Any internet accessible url

Any internet accessible url can be used as a source. This includes urls to raw files on github, gitlab, bitbucket, etc. That is how you can use this website as a bootstrap source, but you can also use it to host your own configuration. 

```bash
uvx bron bootstrap https://example.com/bootstrap.toml
```

## Contribute your config to the bron community

Is your configuration generic/common or interesting enough to share with the bron community? You can contribute it to the bron repository by creating a pull request with your configuration in the `site/assets/{b,c}` directories. Then add a description in the `site/content/bootstrap` and/or `site/content/configs` directories. We will review your configuration and add it to the site if it's useful for the community.
