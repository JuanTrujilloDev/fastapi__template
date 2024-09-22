"""

Load environment variables from .env file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os

from dotenv import load_dotenv


def load_env():
    """Load environment variables."""
    env_path = os.path.join(os.path.dirname(__file__), "env_files/.env")
    env_path = os.path.abspath(env_path)
    load_dotenv(env_path)
