"""
Handle initializer error.

This file contains a decorator to handle initializer errors such as module not found
or error registering an app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from typing import Any, Callable, Dict


def handle_initializer_error(
    func: Callable[..., Dict[str, Any]],
) -> Callable[..., Dict[str, Any]]:
    """
    Handle initializer error.

    This decorator handles initializer errors such
    as module not found or error registering an app.
    """

    def wrapper(*args, **kwargs) -> dict:
        """Wrapper."""
        try:
            return func(*args, **kwargs)
        except ModuleNotFoundError as e:
            raise ValueError(f"App module {args[1]} not found {e}.") from e
        except Exception as e:
            raise ValueError(f"Error registering app {args[1]} {e}.") from e

    return wrapper
