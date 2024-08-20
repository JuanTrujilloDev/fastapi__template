"""

Load environment variables from .env file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os
import sys

from dotenv import load_dotenv


def load_env():
    """Load environment variables."""
    test_args = ["tests", "test", "pytest", "coverage", "test-cov"]
    if any(arg in list(sys.modules.keys()) for arg in test_args):
        test_dotenv = os.path.join(os.path.dirname(__file__), ("env_files/.env.test"))
        load_dotenv(test_dotenv)
    else:
        load_dotenv()
