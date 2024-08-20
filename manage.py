"""

Main entry point for the application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import sys


def main():
    """Run manage commands located in scripts directory."""
    try:
        command = sys.argv[1]
        module = importlib.import_module(f"fastapi__template.scripts.{command}")
        module.main()
    except IndexError:
        print("Usage: manage.py <command>")
        sys.exit(1)
    except ModuleNotFoundError:
        print(f"Command '{command}' not found.")
        sys.exit(1)
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error running command '{command}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
