"""
hand_detector.py

Real-time MediaPipe hand detection and tracking.
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
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,

            # Faster model
            model_complexity=0,

            # Detection confidence
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,

            # Tracking confidence
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,

        )

        self.landmarks = None
        self.last_landmarks = None

        self.hand_detected = False

        # Number of frames we allow MediaPipe
        # to temporarily lose the hand.
        self.missed_frames = 0

        self.max_missed_frames = 5

    def process(self, frame):

        if frame is None:
            return None, None

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Tell MediaPipe we won't modify the image
        rgb_frame.flags.writeable = False

        results = self.hands.process(rgb_frame)

        rgb_frame.flags.writeable = True

        # ==========================================
        # HAND FOUND
        # ==========================================

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            self.landmarks = hand.landmark

            self.last_landmarks = self.landmarks

            self.hand_detected = True

            self.missed_frames = 0

            # Draw landmarks
            if SHOW_LANDMARKS:

                self.mp_drawing.draw_landmarks(
                    frame,
                    hand,
                    self.mp_hands.HAND_CONNECTIONS
                )

            return frame, self.landmarks

        # ==========================================
        # TEMPORARY TRACKING LOSS
        # ==========================================

        self.missed_frames += 1

        if (
            self.last_landmarks is not None
            and self.missed_frames <= self.max_missed_frames
        ):

            self.landmarks = self.last_landmarks

            self.hand_detected = True

            return frame, self.landmarks

        # ==========================================
        # HAND REALLY LOST
        # ==========================================

        self.landmarks = None

        self.hand_detected = False

        return frame, None

    def get_landmarks(self):

        return self.landmarks

    def is_hand_detected(self):

        return self.hand_detected

    def close(self):

        self.hands.close()