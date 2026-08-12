"""
hand_detector.py

Real-time MediaPipe hand detection and tracking.

Designed for fast gesture gameplay.

The detector tolerates a few temporary tracking
losses without immediately declaring that the
hand has disappeared.
"""

import cv2
import mediapipe as mp

from config import (
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    SHOW_LANDMARKS,
)


class HandDetector:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.mp_drawing = (
            mp.solutions.drawing_utils
        )

        # ---------------------------------------------
        # MediaPipe
        # ---------------------------------------------

        self.hands = self.mp_hands.Hands(

            static_image_mode=False,

            max_num_hands=MAX_NUM_HANDS,

            # Fast model
            model_complexity=0,

            min_detection_confidence=(
                MIN_DETECTION_CONFIDENCE
            ),

            min_tracking_confidence=(
                MIN_TRACKING_CONFIDENCE
            ),
        )

        # ---------------------------------------------
        # Current landmarks
        # ---------------------------------------------

        self.landmarks = None

        self.last_landmarks = None

        self.hand_detected = False

        # ---------------------------------------------
        # Tracking loss handling
        # ---------------------------------------------

        self.missed_frames = 0

        # Keep this relatively small.
        #
        # We don't want old hand positions to remain
        # active for too long.
        self.max_missed_frames = 3

    # =================================================
    # PROCESS FRAME
    # =================================================

    def process(self, frame):

        if frame is None:

            return None, None

        # ---------------------------------------------
        # BGR → RGB
        # ---------------------------------------------

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        rgb_frame.flags.writeable = False

        results = self.hands.process(
            rgb_frame
        )

        rgb_frame.flags.writeable = True

        # =================================================
        # HAND FOUND
        # =================================================

        if results.multi_hand_landmarks:

            hand = (
                results.multi_hand_landmarks[0]
            )

            self.landmarks = hand.landmark

            self.last_landmarks = (
                hand.landmark
            )

            self.hand_detected = True

            self.missed_frames = 0

            # ---------------------------------------------
            # Draw landmarks
            # ---------------------------------------------

            if SHOW_LANDMARKS:

                self.mp_drawing.draw_landmarks(

                    frame,

                    hand,

                    self.mp_hands.HAND_CONNECTIONS
                )

            return frame, self.landmarks

        # =================================================
        # TEMPORARY LOSS
        # =================================================

        self.missed_frames += 1

        if (
            self.last_landmarks is not None
            and
            self.missed_frames
            <= self.max_missed_frames
        ):

            # Keep the previous landmarks temporarily.
            #
            # This prevents a single bad MediaPipe
            # frame from breaking the gesture.
            self.landmarks = (
                self.last_landmarks
            )

            self.hand_detected = True

            return frame, self.landmarks

        # =================================================
        # REAL HAND LOSS
        # =================================================

        self.landmarks = None

        self.hand_detected = False

        return frame, None

    # =================================================
    # GET LANDMARKS
    # =================================================

    def get_landmarks(self):

        return self.landmarks

    # =================================================
    # HAND STATUS
    # =================================================

    def is_hand_detected(self):

        return self.hand_detected

    # =================================================
    # CLOSE
    # =================================================

    def close(self):

        self.hands.close()