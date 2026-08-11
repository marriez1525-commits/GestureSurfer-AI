"""
key_mapper.py

Maps game actions to keyboard keys.
"""

from config import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_HOVERBOARD,
)


class KeyMapper:

    def __init__(self):

        self.mapping = {

            ACTION_LEFT: "left",

            ACTION_RIGHT: "right",

            ACTION_JUMP: "up",

            ACTION_ROLL: "down",

            # Subway Surfers hoverboard key
            ACTION_HOVERBOARD: "space",
        }

    def get_key(self, action):

        return self.mapping.get(action)