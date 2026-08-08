"""
key_mapper.py

Maps GestureSurfer AI actions to keyboard keys.
"""

from config import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_JUMP,
    KEY_ROLL,
)


class KeyMapper:
    """
    Converts game actions into keyboard key names.
    """

    def __init__(self):

        self.mapping = {
            ACTION_LEFT: KEY_LEFT,
            ACTION_RIGHT: KEY_RIGHT,
            ACTION_JUMP: KEY_JUMP,
            ACTION_ROLL: KEY_ROLL,
        }

    def get_key(self, action):
        """
        Return the keyboard key associated with an action.

        Example:
            LEFT  -> left
            RIGHT -> right
            JUMP  -> up
            ROLL  -> down
        """

        return self.mapping.get(action)

    def is_valid_action(self, action):
        """
        Check whether an action has a keyboard mapping.
        """

        return action in self.mapping

    def get_mapping(self):
        """
        Return the complete action-to-key mapping.
        """

        return self.mapping.copy()

    def update_mapping(self, action, key):
        """
        Change the keyboard key assigned to an action.
        """

        self.mapping[action] = key