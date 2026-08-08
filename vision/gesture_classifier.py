"""
gesture_classifier.py

Converts detected hand movement into game actions.
"""

from config import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_NONE,
)


class GestureClassifier:
    """
    Converts movement information into a readable
    Subway Surfers action.
    """

    def __init__(self):
        self.current_action = ACTION_NONE

    def classify(self, movement):
        """
        Convert movement direction into a game action.

        Args:
            movement: Movement/action detected by MotionTracker.

        Returns:
            Game action.
        """

        if movement == ACTION_LEFT:
            self.current_action = ACTION_LEFT

        elif movement == ACTION_RIGHT:
            self.current_action = ACTION_RIGHT

        elif movement == ACTION_JUMP:
            self.current_action = ACTION_JUMP

        elif movement == ACTION_ROLL:
            self.current_action = ACTION_ROLL

        else:
            self.current_action = ACTION_NONE

        return self.current_action

    def get_action(self):
        """
        Return the most recently detected action.
        """

        return self.current_action

    def reset(self):
        """
        Reset the classifier.
        """

        self.current_action = ACTION_NONE