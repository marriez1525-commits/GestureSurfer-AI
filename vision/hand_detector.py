"""
hand_detector.py

Detects hands and their 21 landmarks using MediaPipe.
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
    """
    Detects and tracks a hand using MediaPipe Hands.
    """

    def __init__(self):
        # MediaPipe modules
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Create the hand detection model
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

        self.landmarks = None
        self.hand_detected = False

    def process(self, frame):
        """
        Detect a hand in the supplied camera frame.

        Args:
            frame: OpenCV BGR image.

        Returns:
            frame: Processed frame.
            landmarks: Detected hand landmarks or None.
        """

        if frame is None:
            return None, None

        # OpenCV uses BGR.
        # MediaPipe expects RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame
        results = self.hands.process(rgb_frame)

        self.landmarks = None
        self.hand_detected = False

        # Check whether a hand was detected
        if results.multi_hand_landmarks:

            # We are using only one hand
            hand_landmarks = results.multi_hand_landmarks[0]

            self.landmarks = hand_landmarks.landmark
            self.hand_detected = True

            # Draw the hand skeleton
            if SHOW_LANDMARKS:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, self.landmarks

    def get_landmarks(self):
        """
        Return the currently detected landmarks.
        """

        return self.landmarks

    def is_hand_detected(self):
        """
        Return True if a hand is currently detected.
        """

        return self.hand_detected

    def close(self):
        """
        Release the MediaPipe hand detector.
        """

        self.hands.close()