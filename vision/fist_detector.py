"""
fist_detector.py

Detects whether the hand is closed into a fist.
"""

class FistDetector:

    def __init__(self):

        self.was_fist = False

    def is_fist(self, landmarks):

        if landmarks is None:
            self.was_fist = False
            return False

        # Finger tip landmark indices
        tips = [8, 12, 16, 20]

        # Finger middle joint indices
        pips = [6, 10, 14, 18]

        folded = 0

        for tip, pip in zip(tips, pips):

            # For a fist, fingertips are lower than
            # their middle joints in image coordinates.
            if landmarks[tip].y > landmarks[pip].y:

                folded += 1

        # Four folded fingers = fist
        fist = folded >= 4

        return fist

    def just_made_fist(self, landmarks):

        fist = self.is_fist(landmarks)

        # Trigger only when changing from
        # open hand -> fist.
        just_made = (
            fist
            and not self.was_fist
        )

        self.was_fist = fist

        return just_made

    def reset(self):

        self.was_fist = False