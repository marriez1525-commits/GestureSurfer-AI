"""
helpers.py

General helper functions for GestureSurfer AI.
"""

import time


def clamp(value, minimum, maximum):
    """
    Keep a number between minimum and maximum.
    """

    return max(
        minimum,
        min(value, maximum)
    )


def current_time():
    """
    Return the current Unix timestamp.
    """

    return time.time()


def format_action(action):
    """
    Format an action for displaying in the UI.
    """

    if action is None:
        return "NONE"

    return str(action).upper()


def is_valid_action(action, valid_actions):
    """
    Check whether an action exists in a list of valid actions.
    """

    return action in valid_actions