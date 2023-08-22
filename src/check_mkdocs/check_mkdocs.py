import argparse
import os
import platform
import sys
import traceback

import yaml


def main(argv: None = None) -> int:
    """
    The main function is the entry point of the program.

    Parameters
    ----------
    argv : None, optional
        An optional argument representing the command-line arguments. Defaults
        to None if not provided.

    Returns
    -------
    int
        The return value of the function, which is an integer.

    Raises
    ------
    FileNotFoundError
        If the specified config file does not exist.

    Description
    -----------
    The main function creates an argument parser object using the
    `argparse.ArgumentParser()` class. It adds a positional argument
    `config_file` to the parser, which represents the path to the
    configuration file.
    The `nargs='?'` option specifies that the argument is optional and can be
    omitted.
    The `default='mkdocs.yml'` option specifies the default value of the
    argument if it is not provided.

    The function parses the command-line arguments using the
    `parser.parse_args(argv)` method, which returns an object containing the
    parsed arguments.

    The function retrieves the value of the `config_file` argument from the
    parsed arguments.

    If the specified config file does not exist, the function raises a
    `FileNotFoundError` with a descriptive error message.

    The function initializes a variable `retval` with value 0.

    The function attempts to open the config file in read mode using the
    `open(filename, 'r')` function.
    If successful, it reads the contents of the file and loads them as a YAML
    object using the `yaml.safe_load(f)` function.
    If an exception occurs during this process, the function prints an error
    message indicating the file name and the error.
    It also sets the value of `retval` to 1 to indicate an error.

    Finally, the function returns the value of `retval`.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", nargs="?", default="mkdocs.yml")
    args = parser.parse_args(argv)

    filename = args.config_file
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Config file '{filename}' not found. Please specify a config file."
        )

    retval = 0
    try:
        with open(filename, "r") as f:
            config = yaml.safe_load(f)

        # Check if 'site_name' key is present in the loaded YAML
        if "site_name" not in config:
            print(
                f"{filename}: Missing site_name field. This is a required "
                f"field. See: https://www.mkdocs.org/user-guide/configuration/"
            )
            retval = 1

    except Exception as e:
        retval = _generate_user_friendly_yaml_load_error(filename, e)
    return retval


def _generate_user_friendly_yaml_load_error(filename: str, e: Exception) -> int:
    """
    Generates a user-friendly error message for when there is an error loading
    a YAML file.

    Parameters
    ----------
    filename : str
        The name of the YAML file that failed to load.
    e : Exception
        The exception that was raised when trying to load the YAML file.

    Returns
    -------
    int
        The value 1 indicating that an error occurred.
    """

    impl = platform.python_implementation()
    version = sys.version.split()[0]
    print(f"{filename}: Error loading YAML with {impl} {version}: {e}")
    tb = "    " + traceback.format_exc().replace("\n", "\n    ")
    print(f"\n{tb}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
