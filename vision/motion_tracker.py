"""
motion_tracker.py

Fast swipe-based gesture tracker for GestureSurfer AI.

Gestures:
    Swipe LEFT  -> LEFT
    Swipe RIGHT -> RIGHT
    Swipe UP    -> JUMP
    Swipe DOWN  -> ROLL

The tracker detects the direction of the hand's recent movement
instead of treating the return movement as a new gesture.

One physical swipe produces one action.
"""

import time
from collections import deque

from config import (
    HORIZONTAL_THRESHOLD,
    VERTICAL_THRESHOLD,
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
    ACTION_NONE,
)


class MotionTracker:

    def __init__(self):

        # -------------------------------------------------
        # Recent palm positions
        # -------------------------------------------------

        self.positions = deque(maxlen=5)

        # -------------------------------------------------
        # Current movement
        # -------------------------------------------------

        self.delta_x = 0.0
        self.delta_y = 0.0

        # -------------------------------------------------
        # Last detected action
        # -------------------------------------------------

        self.last_action = ACTION_NONE
        self.last_action_time = 0.0

        # -------------------------------------------------
        # Prevent duplicate detection
        # -------------------------------------------------

        self.locked = False

        # -------------------------------------------------
        # Timing
        # -------------------------------------------------

        self.cooldown = 0.10

        self.action_display_time = 0.16

        # -------------------------------------------------
        # Minimum movement required
        # -------------------------------------------------

        self.horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        self.vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        # -------------------------------------------------
        # Minimum movement between frames
        # -------------------------------------------------

        self.motion_threshold = 0.008

        # -------------------------------------------------
        # How much the hand must slow down before
        # another gesture can be detected.
        # -------------------------------------------------

        self.rearm_threshold = 0.012

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, position):

        if position is None:

            return ACTION_NONE

        current_x, current_y = position

        # -------------------------------------------------
        # Store current position
        # -------------------------------------------------

        self.positions.append(
            (current_x, current_y)
        )

        # Need enough positions to calculate movement
        if len(self.positions) < 2:

            return ACTION_NONE

        # -------------------------------------------------
        # Calculate movement between recent positions
        # -------------------------------------------------

        previous_x, previous_y = self.positions[-2]

        self.delta_x = (
            current_x - previous_x
        )

        self.delta_y = (
            current_y - previous_y
        )

        # -------------------------------------------------
        # Movement magnitude
        # -------------------------------------------------

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        # =================================================
        # LOCKED
        # =================================================

        if self.locked:

            # Wait until the hand movement becomes small.
            #
            # IMPORTANT:
            # We do NOT require the hand to return to
            # the original position.
            #
            # This prevents:
            #
            # LEFT -> return movement -> RIGHT
            #
            # and:
            #
            # JUMP -> hand comes down -> ROLL

            if (
                horizontal < self.rearm_threshold
                and vertical < self.rearm_threshold
            ):

                self.locked = False

            return self.get_current_action()

        # =================================================
        # COOLDOWN
        # =================================================

        current_time = time.time()

        if (
            current_time - self.last_action_time
            < self.cooldown
        ):

            return self.get_current_action()

        # =================================================
        # IGNORE VERY SMALL MOVEMENT
        # =================================================

        if (
            horizontal < self.motion_threshold
            and vertical < self.motion_threshold
        ):

            return self.get_current_action()

        # =================================================
        # HORIZONTAL SWIPE
        # =================================================

        if (
            horizontal >= self.horizontal_threshold
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
            vertical >= self.vertical_threshold
            and vertical > horizontal
        ):

            if self.delta_y < 0:

                action = ACTION_JUMP

            else:

                action = ACTION_ROLL

            self.trigger_action(action)

            return action

        return self.get_current_action()

    # =====================================================
    # TRIGGER ACTION
    # =====================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        # Lock immediately.
        self.locked = True

    # =====================================================
    # DISPLAY ACTION
    # =====================================================

    def get_current_action(self):

        if self.last_action == ACTION_NONE:

            return ACTION_NONE

        elapsed = (
            time.time()
            - self.last_action_time
        )

        if elapsed <= self.action_display_time:

            return self.last_action

        return ACTION_NONE

    # =====================================================
    # CURRENT POSITION
    # =====================================================

    def get_current_position(self):

        if not self.positions:

            return None

        return self.positions[-1]

    # =====================================================
    # CURRENT MOVEMENT
    # =====================================================

    def get_delta(self):

        return (
            self.delta_x,
            self.delta_y
        )

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.positions.clear()

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.locked = False