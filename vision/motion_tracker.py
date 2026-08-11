"""
motion_tracker.py

One physical swipe = one game action.

After an action is detected, the tracker enters
RECOVERY mode.

During recovery, movement in the opposite direction
is ignored.

The tracker becomes ready again only after the hand
returns close to the neutral position.
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

        # Neutral hand position
        self.neutral_x = None
        self.neutral_y = None

        # Current movement
        self.delta_x = 0.0
        self.delta_y = 0.0

        # Last action
        self.last_action = ACTION_NONE
        self.last_action_time = 0.0

        # ---------------------------------------------
        # Recovery lock
        # ---------------------------------------------

        self.locked = False

        # Distance required to return to neutral
        self.recovery_threshold = 0.035

        # How long action stays visible
        self.action_display_time = 0.20

    # =================================================
    # UPDATE
    # =================================================

    def update(self, position):

        if position is None:

            return self.get_current_action()

        x, y = position

        # ---------------------------------------------
        # Smooth hand position
        # ---------------------------------------------

        self.smoother.update(x, y)

        smoothed = (
            self.smoother.get_smoothed_position()
        )

        if smoothed is None:

            return self.get_current_action()

        current_x, current_y = smoothed

        # ---------------------------------------------
        # First position = neutral
        # ---------------------------------------------

        if self.neutral_x is None:

            self.neutral_x = current_x
            self.neutral_y = current_y

            return ACTION_NONE

        # ---------------------------------------------
        # Movement from neutral
        # ---------------------------------------------

        self.delta_x = (
            current_x - self.neutral_x
        )

        self.delta_y = (
            current_y - self.neutral_y
        )

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        # Convert config values to normalized values
        horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        # =================================================
        # RECOVERY / LOCKED MODE
        # =================================================

        if self.locked:

            distance = (
                self.delta_x ** 2
                +
                self.delta_y ** 2
            ) ** 0.5

            # ---------------------------------------------
            # Hand returned to neutral
            # ---------------------------------------------

            if distance <= self.recovery_threshold:

                self.locked = False

                self.neutral_x = current_x
                self.neutral_y = current_y

                self.delta_x = 0.0
                self.delta_y = 0.0

            # ---------------------------------------------
            # IMPORTANT:
            #
            # Ignore ALL movement while recovering.
            # ---------------------------------------------

            return self.get_current_action()

        # =================================================
        # COOLDOWN
        # =================================================

        current_time = time.time()

        if (
            current_time - self.last_action_time
            < GESTURE_COOLDOWN
        ):

            return self.get_current_action()

        # =================================================
        # HORIZONTAL GESTURE
        # =================================================

        if (
            horizontal >= horizontal_threshold
            and horizontal > vertical
        ):

            if self.delta_x < 0:

                action = ACTION_LEFT

            else:

                action = ACTION_RIGHT

            self.trigger_action(action)

            return action

        # =================================================
        # VERTICAL GESTURE
        # =================================================

        if (
            vertical >= vertical_threshold
            and vertical > horizontal
        ):

            if self.delta_y < 0:

                action = ACTION_JUMP

            else:

                action = ACTION_ROLL

            self.trigger_action(action)

            return action

        return self.get_current_action()

    # =================================================
    # TRIGGER ACTION
    # =================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        # LOCK immediately after one gesture
        self.locked = True

    # =================================================
    # DISPLAY ACTION
    # =================================================

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

    # =================================================
    # POSITION
    # =================================================

    def get_current_position(self):

        return (
            self.smoother.get_smoothed_position()
        )

    # =================================================
    # DELTA
    # =================================================

    def get_delta(self):

        return (
            self.delta_x,
            self.delta_y
        )

    # =================================================
    # RESET
    # =================================================

    def reset(self):

        self.smoother.reset()

        self.neutral_x = None
        self.neutral_y = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.locked = False