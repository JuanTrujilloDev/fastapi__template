"""

Main entry point for the application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import sys


def main():
    """Run manage commands located in scripts directory."""

    if not len(sys.argv) > 1:
        raise ValueError("Please provide a command to run.")

    command = sys.argv[1]
    try:
        module = importlib.import_module(f"fastapi__template.scripts.{command}")
        module.main()
    except ModuleNotFoundError:
        raise ValueError(f"Command {command} not found.")
    except AttributeError:
        raise ValueError(f"Command {command} does not have a main function.")


if __name__ == "__main__":
    main()
