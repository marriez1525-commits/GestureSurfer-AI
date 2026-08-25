"""
motion_tracker.py

Fast gesture tracking for GestureSurfer AI.

Behavior:

    LEFT  swipe -> LEFT once
    RIGHT swipe -> RIGHT once
    UP    swipe -> JUMP once
    DOWN  swipe -> ROLL once

After an action, the tracker enters recovery mode.
During recovery, opposite/return movement is ignored.

The tracker only becomes ready again after the hand
has slowed down and remained stable for several frames.
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

        # -------------------------------------------------
        # Light smoothing for fast gameplay
        # -------------------------------------------------

        self.smoother = MovementSmoother(
            max_points=2
        )

        # -------------------------------------------------
        # Previous palm position
        # -------------------------------------------------

        self.previous_x = None
        self.previous_y = None

        # -------------------------------------------------
        # Current frame movement
        # -------------------------------------------------

        self.delta_x = 0.0
        self.delta_y = 0.0

        # -------------------------------------------------
        # Last action
        # -------------------------------------------------

        self.last_action = ACTION_NONE
        self.last_action_time = 0.0

        # -------------------------------------------------
        # Gesture state
        # -------------------------------------------------

        self.recovery_mode = False

        # Number of stable/slow frames required before
        # another gesture is allowed.
        self.stable_frames_required = 4

        self.stable_frames = 0

        # -------------------------------------------------
        # Timing
        # -------------------------------------------------

        # Minimum time between intentional gestures.
        self.cooldown = 0.12

        # Keep action visible briefly.
        self.action_display_time = 0.16

        # -------------------------------------------------
        # Movement threshold
        # -------------------------------------------------

        self.motion_threshold = 0.006

        # -------------------------------------------------
        # Recovery threshold
        #
        # If frame-to-frame movement is below this,
        # we consider the hand to be slowing/stabilizing.
        # -------------------------------------------------

        self.recovery_motion_threshold = 0.010

        # -------------------------------------------------
        # Direction thresholds
        # -------------------------------------------------

        self.horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        self.vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, position):

        if position is None:

            return ACTION_NONE

        current_x, current_y = position

        # -------------------------------------------------
        # Smooth current position
        # -------------------------------------------------

        self.smoother.update(
            current_x,
            current_y
        )

        smoothed = (
            self.smoother.get_smoothed_position()
        )

        if smoothed is None:

            return ACTION_NONE

        current_x, current_y = smoothed

        # -------------------------------------------------
        # First frame
        # -------------------------------------------------

        if self.previous_x is None:

            self.previous_x = current_x
            self.previous_y = current_y

            return ACTION_NONE

        # -------------------------------------------------
        # Calculate frame-to-frame movement
        # -------------------------------------------------

        self.delta_x = (
            current_x - self.previous_x
        )

        self.delta_y = (
            current_y - self.previous_y
        )

        self.previous_x = current_x
        self.previous_y = current_y

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        # =================================================
        # RECOVERY MODE
        # =================================================

        if self.recovery_mode:

            # ---------------------------------------------
            # Ignore all movement while the hand is
            # returning/recovering.
            # ---------------------------------------------

            if (
                horizontal < self.recovery_motion_threshold
                and vertical < self.recovery_motion_threshold
            ):

                self.stable_frames += 1

            else:

                self.stable_frames = 0

            # ---------------------------------------------
            # Only re-arm after several stable frames.
            # ---------------------------------------------

            if (
                self.stable_frames
                >= self.stable_frames_required
            ):

                self.recovery_mode = False

                self.stable_frames = 0

                self.last_action = ACTION_NONE

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
        # IGNORE TINY MOVEMENT
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

        # Immediately enter recovery mode.
        self.recovery_mode = True

        self.stable_frames = 0

    # =====================================================
    # CURRENT DISPLAYED ACTION
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

        return (
            self.smoother.get_smoothed_position()
        )

    # =====================================================
    # MOVEMENT DELTA
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

        self.smoother.reset()

        self.previous_x = None
        self.previous_y = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.recovery_mode = False

        self.stable_frames = 0