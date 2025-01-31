+++
title = "Sources"
weight = 1
+++

# Sources

Sources are the starting point for your configuration. They can point to local files or remote URLs. Sources can also point to other sources, allowing you to build complex configurations from multiple files. Relative paths or urls are resolved relative to directory of the source file.

## Examples

### Local file

```toml
[bron.sources.local]
path = "config.toml"
```

### Remote URL

```toml
[bron.sources.remote]
url = "https://example.com/config.toml"
```

### Nested sources

```toml
[bron.sources.local]
path = "config.toml"
```

**config.toml**:
```toml
[bron.sources.nested]
path = "nested.toml"
```

