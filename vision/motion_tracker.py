"""
motion_tracker.py

Fast gesture detection for GestureSurfer AI.

Features:
- Fast response
- One swipe = one action
- Prevents duplicate actions
- Prevents return movement from becoming
  the opposite gesture
- Automatically re-arms after hand returns
  to the neutral zone
"""

import time

from config import (
    HORIZONTAL_THRESHOLD,
    VERTICAL_THRESHOLD,
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_NONE,
)

from vision.smoothing import MovementSmoother


class MotionTracker:

    def __init__(self):

        # Small amount of smoothing so gestures
        # remain responsive.
        self.smoother = MovementSmoother(
            max_points=2
        )

        # Current reference position
        self.start_x = None
        self.start_y = None

        # Current movement
        self.delta_x = 0.0
        self.delta_y = 0.0

        # Last action
        self.last_action = ACTION_NONE
        self.last_action_time = 0.0

        # ------------------------------------------------
        # Gesture state
        # ------------------------------------------------

        self.locked = False

        # ------------------------------------------------
        # Neutral zone
        #
        # Hand must come reasonably close to the
        # starting position before another gesture
        # is allowed.
        # ------------------------------------------------

        self.neutral_threshold = 0.055

        # ------------------------------------------------
        # Minimum time between actions
        # ------------------------------------------------

        self.cooldown = 0.10

        # ------------------------------------------------
        # Action display time
        # ------------------------------------------------

        self.action_display_time = 0.15

    # ====================================================
    # UPDATE
    # ====================================================

    def update(self, position):

        if position is None:

            return self.get_current_action()

        x, y = position

        # ------------------------------------------------
        # Smooth position
        # ------------------------------------------------

        self.smoother.update(x, y)

        smoothed = (
            self.smoother.get_smoothed_position()
        )

        if smoothed is None:

            return self.get_current_action()

        current_x, current_y = smoothed

        # ------------------------------------------------
        # First detected position
        # ------------------------------------------------

        if self.start_x is None:

            self.start_x = current_x
            self.start_y = current_y

            return ACTION_NONE

        # ------------------------------------------------
        # Calculate movement
        # ------------------------------------------------

        self.delta_x = (
            current_x - self.start_x
        )

        self.delta_y = (
            current_y - self.start_y
        )

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        # Config thresholds
        horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        # =================================================
        # LOCKED / RECOVERY STATE
        # =================================================

        if self.locked:

            distance = (
                self.delta_x ** 2
                +
                self.delta_y ** 2
            ) ** 0.5

            # ---------------------------------------------
            # Hand has returned near neutral
            # ---------------------------------------------

            if distance <= self.neutral_threshold:

                self.locked = False

                # Start a fresh movement reference
                self.start_x = current_x
                self.start_y = current_y

                self.delta_x = 0.0
                self.delta_y = 0.0

            # Ignore ALL movement while locked.
            return self.get_current_action()

        # =================================================
        # ACTION COOLDOWN
        # =================================================

        current_time = time.time()

        if (
            current_time - self.last_action_time
            < self.cooldown
        ):

            return self.get_current_action()

        # =================================================
        # HORIZONTAL SWIPE
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
        # VERTICAL SWIPE
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

    # ====================================================
    # TRIGGER ACTION
    # ====================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        # Immediately lock.
        #
        # This is the main protection against:
        #
        # RIGHT → RIGHT
        #
        # from one physical swipe.
        self.locked = True

    # ====================================================
    # DISPLAY ACTION
    # ====================================================

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

    # ====================================================
    # CURRENT POSITION
    # ====================================================

    def get_current_position(self):

        return (
            self.smoother.get_smoothed_position()
        )

    # ====================================================
    # DELTA
    # ====================================================

    def get_delta(self):

        return (
            self.delta_x,
            self.delta_y
        )

    # ====================================================
    # RESET
    # ====================================================

    def reset(self):

        self.smoother.reset()

        self.start_x = None
        self.start_y = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.locked = False