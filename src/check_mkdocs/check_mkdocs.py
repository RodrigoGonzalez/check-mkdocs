import argparse
import os
import platform
import subprocess
import sys
import tempfile
import time
import traceback

import yaml
from mkdocs.config import load_config
from mkdocs.exceptions import ConfigurationError


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
    `config` to the parser, which represents the path to the
    configuration file. The `nargs='?'` option specifies that the argument is
    optional and can be omitted.

    The `default='mkdocs.yml'` option specifies the default value of the
    argument if it is not provided.

    Additionally, it adds a keyword argument `--config` to the parser. This
    argument also represents the path to the configuration file. If both the
    positional and keyword arguments are provided, the keyword argument will
    take precedence.

    Another argument `--generate-build` is added to the parser. This argument
    is a flag to generate a build of the documentation. The default value is False.

    The function parses the command-line arguments using the
    `parser.parse_args(argv)` method, which returns an object containing the
    parsed arguments.

    The function retrieves the value of the `config` argument from the
    parsed arguments.

    If the specified config file does not exist, the function raises a
    `FileNotFoundError` with a descriptive error message.

    The function then attempts to open the config file in read mode using the
    `open(config_file, 'r')` function. If successful, it reads the contents of
    the file and loads them as a YAML object using the `yaml.safe_load(f)`
    function.

    The function checks if the 'site_name' key is present in the loaded YAML.
    If not, it prints an error message.

    The function then loads the configuration using the
    `load_config(config_file=config_file)` function. If there is an error in
    the configuration file, it prints an error message.

    The function then attempts to build the documentation using the
    `build(config)` function. If there is an error during the build process,
    it returns a user-friendly error message.

    The function then attempts to start the server using the
    `serve(config_file=config_file)` function. If there is an error during the
    server start process, it returns a user-friendly error message.

    Finally, the function returns 0 if all the above processes are successful.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        nargs="?",
        default="mkdocs.yml",
        help="Path to the configuration file. Default is 'mkdocs.yml'",
    )
    parser.add_argument(
        "--config",
        dest="config_opt",
        help=(
            "Path to the configuration file. Overrides the positional 'config' "
            "argument if provided."
        ),
    )
    parser.add_argument(
        "--generate-build",
        dest="generate_build",
        action="store_true",
        default=False,
        help="Flag to generate a build of the documentation in your project. Default is False.",
    )
    args = parser.parse_args(argv)

    config_file = args.config_opt or args.config

    if not os.path.exists(config_file):
        raise FileNotFoundError(
            f"Config file '{config_file}' not found. Please specify a " f"config file."
        )

    # Load the YAML to check initial errors
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        # Check if 'site_name' key is present in the loaded YAML
        if "site_name" not in config:
            print(
                f"{config_file}: Missing site_name field. This is a required "
                f"field. See: https://www.mkdocs.org/user-guide/configuration/"
            )

    except Exception as e:
        return _generate_user_friendly_error_message(config_file, "Error loading YAML", e)

    # Load the configuration
    try:
        config = load_config(config_file=config_file)
    except ConfigurationError as e:
        print(f"Error in configuration file: {e}")
        return _generate_user_friendly_error_message(config_file, "Error in configuration file", e)

    # Build the documentation
    try:
        print("Building the documentation...")
        if args.generate_build:
            subprocess.run(["mkdocs", "build", "--config-file", config_file], check=True)
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                subprocess.run(
                    ["mkdocs", "build", "--config-file", config_file, "--site-dir", temp_dir],
                    check=True,
                )
    except Exception as e:
        return _generate_user_friendly_error_message(
            config_file, "Error building the documentation", e
        )

    print("Trying to start the server...")
    # Start the server
    try:
        server_process = subprocess.Popen(
            ["mkdocs", "serve", "--config-file", config_file, "--no-livereload", "--dirty"]
        )
        time.sleep(5)  # wait for 5 seconds to let the server start
        print("Shutting down...")
        server_process.terminate()
        server_process.wait()
    except Exception as e:
        return _generate_user_friendly_error_message(config_file, "Error starting the server", e)

    return 0


def _generate_user_friendly_error_message(
    config_file: str, errror_message: str, e: Exception
) -> int:
    """
    Generates a user-friendly error message for when there is an error loading
    a YAML file.

    Parameters
    ----------
    config_file : str
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
    print(f"{config_file}: {errror_message} with {impl} {version}: {e}")
    tb = "    " + traceback.format_exc().replace("\n", "\n    ")
    print(f"\n{tb}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
