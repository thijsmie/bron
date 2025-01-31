+++
title = "nosync"
+++

# NoSync directives

Want to avoid syncing some entries in your configuration? You can do that by using the `nosync` directive. It can be applied to individual entries or entire sections.

## Example

### Base configuration

```toml
one = "one" 

# nosync
two = "two"

[section.one]
three = "three"

# nosync
[section.two]
four = "four"
```

### Upstream

```toml
one = "onehundred"
two = "twohundred"

[section.one]
three = "threehundred"

[section.two]
four = "fourhundred"
```

### Result

```toml

one = "onehundred"

# nosync
two = "two"

[section.one]
three = "threehundred"

# nosync
[section.two]
four = "four"
```
