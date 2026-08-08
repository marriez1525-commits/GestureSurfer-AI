"""
logger.py

Simple logging system for GestureSurfer AI.
"""

import logging


def setup_logger():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    return logging.getLogger("GestureSurferAI")


logger = setup_logger()


def info(message):
    """
    Display an informational message.
    """

    logger.info(message)


def warning(message):
    """
    Display a warning.
    """

    logger.warning(message)


def error(message):
    """
    Display an error.
    """

    logger.error(message)