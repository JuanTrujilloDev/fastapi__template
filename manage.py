"""

Main entry point for the application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import sys


def main():
    """Run manage commands located in scripts directory."""

    command = sys.argv[1]
    module = importlib.import_module(f"fastapi__template.scripts.{command}")
    module.main()


if __name__ == "__main__":
    main()
