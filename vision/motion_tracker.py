"""
motion_tracker.py

Detects the direction in which the user's hand moves.
"""

import time

from config import (
    HORIZONTAL_THRESHOLD,
    VERTICAL_THRESHOLD,
    GESTURE_COOLDOWN,
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_NONE,
)

from vision.smoothing import MovementSmoother


class MotionTracker:
    """
    Tracks hand movement and converts it into
    LEFT, RIGHT, JUMP, or ROLL actions.
    """

    def __init__(self):
        self.smoother = MovementSmoother()

        self.previous_position = None

        self.last_action_time = 0

    def update(self, position):
        """
        Process the current hand position.

        Args:
            position: (x, y) normalized hand position.

        Returns:
            One of the action constants.
        """

        if position is None:
            return ACTION_NONE

        x, y = position

        # Add current position to smoother
        self.smoother.update(x, y)

        smoothed_position = self.smoother.get_smoothed_position()

        if smoothed_position is None:
            return ACTION_NONE

        current_x, current_y = smoothed_position

        # First frame: nothing to compare with
        if self.previous_position is None:
            self.previous_position = (current_x, current_y)
            return ACTION_NONE

        previous_x, previous_y = self.previous_position

        # Calculate movement
        delta_x = current_x - previous_x
        delta_y = current_y - previous_y

        # Update previous position
        self.previous_position = (current_x, current_y)

        # Check cooldown
        current_time = time.time()

        if current_time - self.last_action_time < GESTURE_COOLDOWN:
            return ACTION_NONE

        # ----------------------------------------------------
        # Horizontal movement
        # ----------------------------------------------------

        if abs(delta_x) > HORIZONTAL_THRESHOLD / 1000:

            self.last_action_time = current_time

            if delta_x < 0:
                return ACTION_LEFT

            return ACTION_RIGHT

        # ----------------------------------------------------
        # Vertical movement
        # ----------------------------------------------------

        if abs(delta_y) > VERTICAL_THRESHOLD / 1000:

            self.last_action_time = current_time

            if delta_y < 0:
                return ACTION_JUMP

            return ACTION_ROLL

        return ACTION_NONE

    def reset(self):
        """
        Reset movement tracking.
        """

        self.smoother.reset()
        self.previous_position = None
        self.last_action_time = 0