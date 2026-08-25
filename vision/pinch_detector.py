"""
pinch_detector.py

Detects a thumb + index finger pinch.

A stable pinch triggers once.
The fingers must separate before another
pinch can trigger.
"""

import math
import time


class PinchDetector:

    def __init__(self):

        self.was_pinched = False

        self.pinch_start_time = None

        # How long the pinch must remain stable
        # before triggering.
        self.required_hold_time = 0.20

    def _distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2
            + (p1.y - p2.y) ** 2
        )

    def is_pinched(self, landmarks):

        if landmarks is None:
            return False

        if len(landmarks) < 21:
            return False

        thumb_tip = landmarks[4]

        index_tip = landmarks[8]

        wrist = landmarks[0]

        middle_mcp = landmarks[9]

        # Distance between thumb and index
        pinch_distance = self._distance(
            thumb_tip,
            index_tip
        )

        # Approximate hand size
        hand_size = self._distance(
            wrist,
            middle_mcp
        )

        if hand_size <= 0:
            return False

        # Normalize by hand size so the pinch works
        # at different distances from the camera.
        normalized_distance = (
            pinch_distance / hand_size
        )

        return normalized_distance < 0.35

    def just_pinched(self, landmarks):

        pinched = self.is_pinched(landmarks)

        current_time = time.time()

        # ------------------------------------------------
        # Pinch started
        # ------------------------------------------------

        if pinched and not self.was_pinched:

            self.pinch_start_time = current_time

            self.was_pinched = True

            return False

        # ------------------------------------------------
        # Pinch still held
        # ------------------------------------------------

        if pinched and self.was_pinched:

            if self.pinch_start_time is None:
                return False

            held_for = (
                current_time
                - self.pinch_start_time
            )

            if held_for >= self.required_hold_time:

                # Prevent repeated triggers
                self.pinch_start_time = None

                return True

            return False

        # ------------------------------------------------
        # Fingers separated
        # ------------------------------------------------

        if not pinched:

            self.was_pinched = False

            self.pinch_start_time = None

        return False

    def reset(self):

        self.was_pinched = False

        self.pinch_start_time = None