"""
fist_detector.py

Detects a fist and triggers HOVERBOARD only once.

A fist must be opened before another fist
can trigger the hoverboard again.
"""

from config import ACTION_HOVERBOARD


class FistDetector:

    def __init__(self):

        self.was_fist = False

        # Number of extended fingers required
        # to consider the hand NOT a fist.
        self.minimum_open_fingers = 2

    # =====================================================
    # FINGER CHECK
    # =====================================================

    def _is_fist(self, landmarks):

        if landmarks is None:
            return False

        if len(landmarks) < 21:
            return False

        # -------------------------------------------------
        # Finger tip and PIP positions
        # -------------------------------------------------

        fingers = [
            (8, 6),    # index
            (12, 10),  # middle
            (16, 14),  # ring
            (20, 18),  # pinky
        ]

        extended = 0

        for tip_id, pip_id in fingers:

            tip = landmarks[tip_id]
            pip = landmarks[pip_id]

            # Finger extended when tip is above PIP
            if tip.y < pip.y:

                extended += 1

        # -------------------------------------------------
        # Fist
        # -------------------------------------------------

        return (
            extended < self.minimum_open_fingers
        )

    # =====================================================
    # JUST MADE FIST
    # =====================================================

    def just_made_fist(self, landmarks):

        current_is_fist = (
            self._is_fist(landmarks)
        )

        # -----------------------------------------------
        # New fist
        # -----------------------------------------------

        if (
            current_is_fist
            and not self.was_fist
        ):

            self.was_fist = True

            return True

        # -----------------------------------------------
        # Hand opened again
        # -----------------------------------------------

        if not current_is_fist:

            self.was_fist = False

        return False

    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.was_fist = False