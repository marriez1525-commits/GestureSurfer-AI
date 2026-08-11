"""
motion_tracker.py

Detects intentional hand swipes.

Behavior:

LEFT:
    Swipe left  -> LEFT
    Return hand -> ignored

RIGHT:
    Swipe right -> RIGHT
    Return hand -> ignored

JUMP:
    Swipe up    -> JUMP
    Return hand -> ignored

ROLL:
    Swipe down  -> ROLL
    Return hand -> ignored

The tracker waits for the hand to return near
the center before accepting another gesture.
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

        # -------------------------------------------------
        # Current reference position
        # -------------------------------------------------

        self.start_x = None
        self.start_y = None

        # -------------------------------------------------
        # Movement values
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

        self.locked = False

        # -------------------------------------------------
        # IMPORTANT
        #
        # This is deliberately larger than before.
        # It allows the hand to naturally return to
        # its starting position.
        # -------------------------------------------------

        self.recovery_threshold = 0.08

        # Action display duration
        self.action_display_time = 0.20

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, position):

        if position is None:

            return self.get_current_action()

        x, y = position

        # -------------------------------------------------
        # Smooth hand position
        # -------------------------------------------------

        self.smoother.update(x, y)

        smoothed = (
            self.smoother.get_smoothed_position()
        )

        if smoothed is None:

            return self.get_current_action()

        current_x, current_y = smoothed

        # -------------------------------------------------
        # Establish starting position
        # -------------------------------------------------

        if self.start_x is None:

            self.start_x = current_x
            self.start_y = current_y

            return ACTION_NONE

        # -------------------------------------------------
        # Calculate movement from starting position
        # -------------------------------------------------

        self.delta_x = (
            current_x - self.start_x
        )

        self.delta_y = (
            current_y - self.start_y
        )

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        # -------------------------------------------------
        # Convert thresholds
        # -------------------------------------------------

        horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        # =================================================
        # RECOVERY MODE
        # =================================================

        if self.locked:

            distance = (
                self.delta_x ** 2
                +
                self.delta_y ** 2
            ) ** 0.5

            # ---------------------------------------------
            # Hand has returned close enough
            # ---------------------------------------------

            if distance <= self.recovery_threshold:

                self.locked = False

                # Start a NEW reference point here.
                self.start_x = current_x
                self.start_y = current_y

                self.delta_x = 0.0
                self.delta_y = 0.0

            # ---------------------------------------------
            # While recovering:
            #
            # DO NOT detect another gesture.
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
        # HORIZONTAL MOVEMENT
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
        # VERTICAL MOVEMENT
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

    # =====================================================
    # TRIGGER ACTION
    # =====================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        # Lock until hand returns.
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

        if elapsed < self.action_display_time:

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

        self.start_x = None
        self.start_y = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.locked = False