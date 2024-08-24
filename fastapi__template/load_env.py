"""

Load environment variables from .env file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from dotenv import load_dotenv


def load_env():
    """Load environment variables."""
    load_dotenv()
