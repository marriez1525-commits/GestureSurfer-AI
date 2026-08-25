"""
motion_tracker.py

Fast swipe detector for GestureSurfer AI.

One intentional movement = one action.

The detector:
- Uses several recent frames
- Detects cumulative movement
- Responds quickly
- Prevents duplicate actions
- Ignores return movement
- Re-arms after the hand becomes stable
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

        # Recent palm positions
        self.positions = deque(
            maxlen=5
        )

        # Current movement
        self.delta_x = 0.0
        self.delta_y = 0.0

        # Last action
        self.last_action = ACTION_NONE
        self.last_action_time = 0.0

        # Recovery state
        self.recovery_mode = False

        # Number of stable frames before
        # accepting another gesture
        self.stable_frames = 0

        self.stable_frames_required = 3

        # Small movement = hand is stable
        self.stable_threshold = 0.008

        # Fast cooldown
        self.cooldown = 0.10

        # How long action remains visible
        self.action_display_time = 0.14

        # Normalized thresholds
        self.horizontal_threshold = (
            HORIZONTAL_THRESHOLD / 1000.0
        )

        self.vertical_threshold = (
            VERTICAL_THRESHOLD / 1000.0
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, position):

        if position is None:

            return ACTION_NONE

        current_x, current_y = position

        # ----------------------------------------------------
        # Store position
        # ----------------------------------------------------

        self.positions.append(
            (current_x, current_y)
        )

        if len(self.positions) < 3:

            return ACTION_NONE

        # ----------------------------------------------------
        # Recent movement
        # ----------------------------------------------------

        oldest_x, oldest_y = (
            self.positions[0]
        )

        newest_x, newest_y = (
            self.positions[-1]
        )

        self.delta_x = (
            newest_x - oldest_x
        )

        self.delta_y = (
            newest_y - oldest_y
        )

        horizontal = abs(self.delta_x)

        vertical = abs(self.delta_y)

        # ====================================================
        # RECOVERY MODE
        # ====================================================

        if self.recovery_mode:

            # Current frame movement
            previous_x, previous_y = (
                self.positions[-2]
            )

            frame_dx = (
                newest_x - previous_x
            )

            frame_dy = (
                newest_y - previous_y
            )

            frame_speed = max(
                abs(frame_dx),
                abs(frame_dy)
            )

            if frame_speed < self.stable_threshold:

                self.stable_frames += 1

            else:

                self.stable_frames = 0

            # Re-arm after hand becomes stable
            if (
                self.stable_frames
                >= self.stable_frames_required
            ):

                self.recovery_mode = False

                self.stable_frames = 0

                self.positions.clear()

                self.positions.append(
                    (newest_x, newest_y)
                )

                self.delta_x = 0.0
                self.delta_y = 0.0

                self.last_action = ACTION_NONE

            return self.get_current_action()

        # ====================================================
        # COOLDOWN
        # ====================================================

        current_time = time.time()

        if (
            current_time
            - self.last_action_time
            < self.cooldown
        ):

            return self.get_current_action()

        # ====================================================
        # IGNORE TINY MOVEMENT
        # ====================================================

        if (
            horizontal
            < self.horizontal_threshold
            and
            vertical
            < self.vertical_threshold
        ):

            return self.get_current_action()

        # ====================================================
        # HORIZONTAL
        # ====================================================

        if (
            horizontal
            >= self.horizontal_threshold
            and horizontal > vertical
        ):

            if self.delta_x < 0:

                action = ACTION_LEFT

            else:

                action = ACTION_RIGHT

            self.trigger_action(action)

            return action

        # ====================================================
        # VERTICAL
        # ====================================================

        if (
            vertical
            >= self.vertical_threshold
            and vertical > horizontal
        ):

            if self.delta_y < 0:

                action = ACTION_JUMP

            else:

                action = ACTION_ROLL

            self.trigger_action(action)

            return action

        return self.get_current_action()

    # ========================================================
    # TRIGGER
    # ========================================================

    def trigger_action(self, action):

        self.last_action = action

        self.last_action_time = time.time()

        self.recovery_mode = True

        self.stable_frames = 0

    # ========================================================
    # DISPLAY ACTION
    # ========================================================

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

    # ========================================================
    # POSITION
    # ========================================================

    def get_current_position(self):

        if not self.positions:

            return None

        return self.positions[-1]

    # ========================================================
    # DELTA
    # ========================================================

    def get_delta(self):

        return (
            self.delta_x,
            self.delta_y
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.positions.clear()

        self.delta_x = 0.0
        self.delta_y = 0.0

        self.last_action = ACTION_NONE

        self.last_action_time = 0.0

        self.recovery_mode = False

        self.stable_frames = 0