"""

Function utility methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from functools import wraps


def call_func_once(func):
    """
    Makes sure that the function is called only once.
    """
    func.has_been_called = False

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if func.has_been_called:
            pass
        else:
            func.has_been_called = True
            return await func(*args, **kwargs)

    return wrapper
