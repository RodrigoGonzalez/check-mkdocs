# Welcome to Check MkDocs

This is a simple .pre-commit-config.yaml hook to check if MkDocs is configured correctly.

## Usage

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
    - repo: https://github.com/RodrigoGonzalez/check-mkdocs
      rev: v1.0.0
      hooks:
        - id: check-mkdocs
          name: check-mkdocs
          args: [--config-file=mkdocs.yml]  # Optional, mkdocs.yml is the default
```

:::check_mkdocs
