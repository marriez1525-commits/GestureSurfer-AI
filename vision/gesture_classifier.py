"""
gesture_classifier.py

Converts movement information into game actions.
"""

from config import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_NONE,
)


class GestureClassifier:

    def __init__(self):

        self.last_action = ACTION_NONE

    def classify(self, movement):

        if movement is None:
            return ACTION_NONE

        valid_actions = (
            ACTION_LEFT,
            ACTION_RIGHT,
            ACTION_JUMP,
            ACTION_ROLL,
        )

        if movement in valid_actions:

            self.last_action = movement

            return movement

        return ACTION_NONE

    def reset(self):

        self.last_action = ACTION_NONE

    def get_last_action(self):

        return self.last_action