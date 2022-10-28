import os
import sys

import logging
logger = logging.getLogger(__name__)


def const_from_env(const_name, default=''):
    """
    Get a constant value from environ. if it doesn't exist, print a warning and return the default value.
    """
    try:
        return os.environ[const_name]
    except KeyError:
        logger.warning(f"The environment variable {const_name} was not found. Defaulting to {default}.")
        return default

def const_from_env_must(const_name):
    """
    Get a constant value from environ. if it doesn't exist, exit.
    """
    try:
        return os.environ[const_name]
    except KeyError:
        logging.error(f"The environment variable {const_name} was not found.")
        sys.exit(1)