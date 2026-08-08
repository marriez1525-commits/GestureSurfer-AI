"""
hand_detector.py

Detects and tracks hands using MediaPipe.
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
    Real-time hand detector for GestureSurfer AI.
    """

    def __init__(self):

        # MediaPipe modules
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Create MediaPipe hand model
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,

            max_num_hands=MAX_NUM_HANDS,

            model_complexity=0,

            min_detection_confidence=MIN_DETECTION_CONFIDENCE,

            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )

        self.landmarks = None

        self.hand_detected = False

        # Keep the last valid landmarks.
        # This helps when MediaPipe briefly misses a frame.
        self.last_landmarks = None

        # Number of frames for which we tolerate
        # a temporary tracking failure.
        self.missed_frames = 0

        self.max_missed_frames = 3

    def process(self, frame):
        """
        Detect a hand in the camera frame.

        Returns:
            frame
            landmarks
        """

        if frame is None:
            return None, None

        # OpenCV uses BGR.
        # MediaPipe requires RGB.
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Improve performance by telling MediaPipe
        # that the image will not be modified.
        rgb_frame.flags.writeable = False

        results = self.hands.process(rgb_frame)

        rgb_frame.flags.writeable = True

        # --------------------------------------------------
        # Hand detected
        # --------------------------------------------------

        if results.multi_hand_landmarks:

            hand_landmarks = results.multi_hand_landmarks[0]

            self.landmarks = hand_landmarks.landmark

            self.last_landmarks = self.landmarks

            self.hand_detected = True

            self.missed_frames = 0

            # Draw landmarks
            if SHOW_LANDMARKS:

                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

            return frame, self.landmarks

        # --------------------------------------------------
        # Hand temporarily lost
        # --------------------------------------------------

        self.missed_frames += 1

        if (
            self.last_landmarks is not None
            and self.missed_frames <= self.max_missed_frames
        ):

            # Temporarily keep using the previous landmarks.
            self.landmarks = self.last_landmarks

            self.hand_detected = True

            return frame, self.landmarks

        # --------------------------------------------------
        # Hand genuinely lost
        # --------------------------------------------------

        self.landmarks = None

        self.hand_detected = False

        return frame, None

    def get_landmarks(self):
        """
        Return current hand landmarks.
        """

        return self.landmarks

    def is_hand_detected(self):
        """
        Return whether a hand is currently available.
        """

        return self.hand_detected

    def close(self):
        """
        Close MediaPipe.
        """

        self.hands.close()