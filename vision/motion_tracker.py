"""
motion_tracker.py

GestureSurfer AI gesture detection.

Important behavior:

ONE swipe = ONE action.

After a gesture is detected, the tracker locks.
The hand can move back to its original position
without creating an opposite gesture.

The tracker unlocks only after the hand returns
close to the neutral position.
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
    GESTURE_COOLDOWN,
)

from vision.smoothing import MovementSmoother


class MotionTracker:

    def __init__(self):

        # ------------------------------------------
        # Smoothing
        # ------------------------------------------

        self.smoother = MovementSmoother(
            max_points=3
        )

        # ------------------------------------------
        # Neutral position
        # ------------------------------------------

        self.neutral_position = None

        # ------------------------------------------
        # Movement values
        # ------------------------------------------

        self.delta_x = 0.0
        self.delta_y = 0.0

        # ------------------------------------------
        # Action
        # ------------------------------------------

        self.last_action = ACTION_NONE
        self.last_action_time = 0

        # ------------------------------------------
        # Gesture lock
        # ------------------------------------------

        self.gesture_locked = False

        # ------------------------------------------
        # Recovery
        # ------------------------------------------

        # How close the hand must return to the
        # neutral position before another gesture
        # can be detected.
        self.recovery_threshold = 0.035

        # ------------------------------------------
        # Action display
        # ------------------------------------------

        self.action_display_time = 0.20

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, position):

        if position is None:

            return self.get_current_action()

        x, y = position

        # ------------------------------------------
        # Smooth position
        # ------------------------------------------

        self.smoother.update(x, y)

        smoothed = (
            self.smoother.get_smoothed_position()
        )

        if smoothed is None:

            return self.get_current_action()

        current_x, current_y = smoothed

        # ------------------------------------------
        # Establish neutral position
        # ------------------------------------------

        if self.neutral_position is None:

            self.neutral_position = (
                current_x,
                current_y
            )

            return ACTION_NONE

        neutral_x, neutral_y = (
            self.neutral_position
        )

        # ------------------------------------------
        # Calculate displacement from neutral
        # ------------------------------------------

        self.delta_x = (
            current_x - neutral_x
        )

        self.delta_y = (
            current_y - neutral_y
        )

        horizontal = abs(self.delta_x)
        vertical = abs(self.delta_y)

        horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

        # ==================================================
        # LOCKED STATE
        # ==================================================

        if self.gesture_locked:

            distance_from_neutral = (
                (self.delta_x ** 2)
                +
                (self.delta_y ** 2)
            ) ** 0.5

            # ------------------------------------------
            # Hand has returned close enough to neutral
            # ------------------------------------------

            if (
                distance_from_neutral
                <= self.recovery_threshold
            ):

                self.gesture_locked = False

                self.delta_x = 0.0
                self.delta_y = 0.0

                # New neutral position
                self.neutral_position = (
                    current_x,
                    current_y
                )

            # IMPORTANT:
            #
            # While locked, movement is ignored.
            #
            # Therefore:
            #
            # LEFT → return RIGHT
            #
            # does NOT create RIGHT.
            #
            # JUMP → move DOWN
            #
            # does NOT create ROLL.

            return self.get_current_action()

        # ==================================================
        # COOLDOWN
        # ==================================================

        current_time = time.time()

        if (
            current_time - self.last_action_time
            < GESTURE_COOLDOWN
        ):

            return self.get_current_action()

        # ==================================================
        # HORIZONTAL GESTURE
        # ==================================================

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

        # ==================================================
        # VERTICAL GESTURE
        # ==================================================

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

    # ==================================================
    # TRIGGER ACTION
    # ==================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        # Lock until hand returns to neutral.
        self.gesture_locked = True

    # ==================================================
    # CURRENT ACTION
    # ==================================================

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

    # ==================================================
    # CURRENT POSITION
    # ==================================================

    def get_current_position(self):

        return (
            self.smoother.get_smoothed_position()
        )

    # ==================================================
    # DELTA
    # ==================================================

    def get_delta(self):

        return (
            self.delta_x,
            self.delta_y
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.smoother.reset()

        self.neutral_position = None

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0

        self.gesture_locked = False