"""
motion_tracker.py

Smooth hand movement detection for GestureSurfer AI.
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

        self.smoother = MovementSmoother(
            max_points=3
        )

        self.start_position = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE
        self.last_action_time = 0

        self.action_display_time = 0.25

    def update(self, position):

        if position is None:
            return self.get_current_action()

        x, y = position

        # Smooth hand position
        self.smoother.update(x, y)

        smoothed = self.smoother.get_smoothed_position()

        if smoothed is None:
            return self.get_current_action()

        current_x, current_y = smoothed

        # First detected position
        if self.start_position is None:

            self.start_position = (
                current_x,
                current_y
            )

            return ACTION_NONE

        start_x, start_y = self.start_position

        # Calculate movement
        self.delta_x = current_x - start_x
        self.delta_y = current_y - start_y

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        current_time = time.time()

        # Prevent actions from firing too quickly
        if (
            current_time - self.last_action_time
            < GESTURE_COOLDOWN
        ):
            return self.get_current_action()

        # -----------------------------------------
        # LEFT / RIGHT
        # -----------------------------------------

        if (
            horizontal >= horizontal_threshold
            and horizontal > vertical
        ):

            if self.delta_x < 0:

                action = ACTION_LEFT

            else:

                action = ACTION_RIGHT

            self.last_action = action
            self.last_action_time = current_time

            # Reset starting point after gesture
            self.start_position = (
                current_x,
                current_y
            )

            return action

        # -----------------------------------------
        # UP / DOWN
        # -----------------------------------------

        if (
            vertical >= vertical_threshold
            and vertical > horizontal
        ):

            if self.delta_y < 0:

                action = ACTION_JUMP

            else:

                action = ACTION_ROLL

            self.last_action = action
            self.last_action_time = current_time

            self.start_position = (
                current_x,
                current_y
            )

            return action

        return self.get_current_action()

    def get_current_action(self):

        if self.last_action == ACTION_NONE:
            return ACTION_NONE

        elapsed = (
            time.time()
            - self.last_action_time
        )

        if elapsed < self.action_display_time:
            return self.last_action

        return ACTION_NONE

    def get_current_position(self):

        return self.smoother.get_smoothed_position()

    def get_delta(self):

        return self.delta_x, self.delta_y

    def reset(self):

        self.smoother.reset()

        self.start_position = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0