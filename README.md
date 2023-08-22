# check-mkdocs
Check if MkDocs is configured correctly

This is a simple .pre-commit-config.yaml hook to check if MkDocs
is configured correctly.

## Features

- Validates the MkDocs configuration file (default is `mkdocs.yml`).
- Builds the MkDocs project documentation via `mkdocs build`.
- Checks the built documentation via `mkdocs serve`.
- Can be used as a pre-commit hook.
- Optionally, it can generate a build of the MkDocs documentation.

## Pre-Commit Usage

Add this to your `.pre-commit-config.yaml`, where `mkdocs.yml`
is the name of your MkDocs YAML configuration file:

```yaml
repos:
    - repo: https://github.com/RodrigoGonzalez/check-mkdocs
      rev: v1.1.3
      hooks:
        - id: check-mkdocs
          name: check-mkdocs
          args: [--config=mkdocs.yml]  # Optional, mkdocs.yml is the default
```

## Command-Line Usage

To run this hook, you can use the following command:

```shell
check-mkdocs --config=mkdocs.yml
```

This works as well:

```shell
check-mkdocs mkdocs.yml
```

And if `mkdocs.yml` is the name of your MkDocs YAML
configuration file, this works too:

```shell
check-mkdocs
```

These commands will validate the MkDocs configuration
file, build the project documentation, and start the
server. If there's an error in any of these steps, the
tool will print an error message and return an error code.

### The `--generate-build` Argument

The `--generate-build` argument is a command-line flag that
you can use to instruct the check_mkdocs tool to generate a
build of the MkDocs documentation. This argument is
optional, and its default value is False, which means that
by default, the tool will not generate a build.

When you provide this argument, the tool will call the
build function from mkdocs.commands.build with the loaded
configuration. This function will build the project
documentation and place the built documentation in the
`site_dir` directory specified in the configuration. If the
`site_dir` directory is not specified in the configuration,
the tool will use the MkDocs default location as the
`site_dir` (i.e., `site/`).

Here's how you can use this argument:

```shell
check-mkdocs --config=mkdocs.yml --generate-build
```

This command will validate the MkDocs configuration file,
build the project documentation, and start the server. If
there's an error in any of these steps, the tool will print
an error message and return an error code.

## Installation via Pip

You can install this tool via pip:

```shell
pip install check-mkdocs
```

### Local Installation

This tool is packaged with Poetry. To install it, you can clone the
repository and use Poetry to install the dependencies:

```shell
git clone https://github.com/RodrigoGonzalez/check-mkdocs.git
cd check-mkdocs
poetry install
```
