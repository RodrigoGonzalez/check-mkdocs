# check-mkdocs
Check if MkDocs is configured correctly

This is a simple .pre-commit-config.yaml hook to check if MkDocs
is configured correctly.

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

## Features

- Validates the MkDocs configuration file (default is `mkdocs.yml`).
- Builds the MkDocs project documentation via `mkdocs build`.
- Checks the built documentation via `mkdocs serve`.
- Can be used as a pre-commit hook.
- Optionally, it can generate a build of the MkDocs documentation.

Documentation: https://rodrigogonzalez.github.io/check-mkdocs/

## Pre-Commit Usage

Add this to your `.pre-commit-config.yaml`, where `mkdocs.yml`
is the name of your MkDocs YAML configuration file:

```yaml
repos:
    - repo: https://github.com/RodrigoGonzalez/check-mkdocs
      rev: v1.2.0
      hooks:
        - id: check-mkdocs
          name: check-mkdocs
          args: ["--config", "mkdocs.yml"]  # Optional, mkdocs.yml is the default
          # If you have additional plugins or libraries that are not included in check-mkdocs, add them here
          additional_dependencies: ['mkdocs-material']
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

## Known Issues

### Missing MkDocs Plugins

Given the enormous number of plugins available for MkDocs,
it's possible that some plugins are not included in this
tool. In this case you will see an error message similar to
this:

```shell
check-mkdocs.............................................................Failed
- hook id: check-mkdocs
- exit code: 1

Config value 'theme': Unrecognised theme name: 'material'. The available installed themes are: mkdocs, readthedocs
Config value 'markdown_extensions': Failed to load extension 'pymdownx.snippets'.
ModuleNotFoundError: No module named 'pymdownx'
Config value 'plugins': The "mkdocstrings" plugin is not installed

make: *** [pre-commit] Error 1
```

If you have additional plugins or libraries that are not
included in check-mkdocs, add them here:

```yaml
repos:
    - repo: https://github.com/RodrigoGonzalez/check-mkdocs
      hooks:
        - id: check-mkdocs
          # If you have additional plugins or libraries that are not included in check-mkdocs, add them here
          additional_dependencies: ['mkdocs-material', 'mkdocstrings']
```
