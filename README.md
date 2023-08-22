# check-mkdocs
Check if MkDocs is configured correctly

This is a simple .pre-commit-config.yaml hook to check if MkDocs
is configured correctly.

## Pre-Commit Usage

Add this to your `.pre-commit-config.yaml`, where `mkdocs.yml`
is the name of your MkDocs YAML configuration file:

```yaml
repos:
    - repo: https://github.com/RodrigoGonzalez/check-mkdocs
      rev: v1.0.0
      hooks:
        - id: check-mkdocs
          name: check-mkdocs
          args: [--config=mkdocs.yml]  # Optional, mkdocs.yml is the default
```

## Usage

To run this hook, you can use the following command:

```shell
check-mkdocs --config=mkdocs.yml
```

This works as well:

```shell
check-mkdocs mkdocs.yml
```

And if mkdocs.yml is the name of your MkDocs YAML
configuration file, this works too:

```shell
check-mkdocs
```
