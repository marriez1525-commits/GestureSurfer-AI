"""
motion_tracker.py

Stable hand movement detection for GestureSurfer AI.

Detects:
    LEFT
    RIGHT
    JUMP
    ROLL
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

    def __init__(self):

        self.smoother = MovementSmoother()

        # Position where a movement begins
        self.start_position = None

        # Last detected action
        self.last_action = ACTION_NONE

        # Time when action was detected
        self.last_action_time = 0

    def update(self, position):

        if position is None:
            return ACTION_NONE

        x, y = position

        # Add new position
        self.smoother.update(x, y)

        # Get smoothed position
        current_position = self.smoother.get_smoothed_position()

        if current_position is None:
            return ACTION_NONE

        current_x, current_y = current_position

        # --------------------------------------------------
        # Establish starting position
        # --------------------------------------------------

        if self.start_position is None:

            self.start_position = (
                current_x,
                current_y
            )

            return ACTION_NONE

        start_x, start_y = self.start_position

        # --------------------------------------------------
        # Calculate total movement
        # --------------------------------------------------

        delta_x = current_x - start_x
        delta_y = current_y - start_y

        horizontal = abs(delta_x)
        vertical = abs(delta_y)

        # Convert threshold to MediaPipe's 0-1 scale
        horizontal_threshold = HORIZONTAL_THRESHOLD / 1000
        vertical_threshold = VERTICAL_THRESHOLD / 1000

        current_time = time.time()

        # --------------------------------------------------
        # Cooldown
        # --------------------------------------------------

        if current_time - self.last_action_time < GESTURE_COOLDOWN:

            return self.last_action

        # --------------------------------------------------
        # Horizontal movement
        # --------------------------------------------------

        if (
            horizontal >= horizontal_threshold
            and horizontal > vertical
        ):

            self.last_action_time = current_time

            if delta_x < 0:

                self.last_action = ACTION_LEFT

            else:

                self.last_action = ACTION_RIGHT

            # Start a new movement from current position
            self.start_position = (
                current_x,
                current_y
            )

            return self.last_action

        # --------------------------------------------------
        # Vertical movement
        # --------------------------------------------------

        if (
            vertical >= vertical_threshold
            and vertical > horizontal
        ):

            self.last_action_time = current_time

            if delta_y < 0:

                self.last_action = ACTION_JUMP

            else:

                self.last_action = ACTION_ROLL

            # Start a new movement
            self.start_position = (
                current_x,
                current_y
            )

            return self.last_action

        # --------------------------------------------------
        # No new movement
        # --------------------------------------------------

        self.last_action = ACTION_NONE

        return ACTION_NONE

    def reset(self):

        self.smoother.reset()

        self.start_position = None

        self.last_action = ACTION_NONE

        self.last_action_time = 0

    def get_current_position(self):

        return self.smoother.get_smoothed_position()