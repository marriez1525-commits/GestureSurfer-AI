"""
camera.py

Handles webcam initialization and frame capture
for GestureSurfer AI.
"""

import cv2

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
)


class Camera:
    """
    Manages the webcam and provides frames to the
    computer vision system.
    """

    def __init__(self):
        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():
            raise RuntimeError(
                "Could not open the webcam. "
                "Please check that your camera is connected."
            )

        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    def read(self):
        """
        Capture one frame from the webcam.

        Returns:
            frame: The captured camera frame.
        """

        success, frame = self.camera.read()

        if not success:
            return None

        # Mirror the camera like a normal webcam
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        """
        Release the webcam.
        """

        if self.camera is not None:
            self.camera.release()

    def is_opened(self):
        """
        Check whether the camera is currently available.
        """

        return self.camera.isOpened()