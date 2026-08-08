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
        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )

        # Try to reduce camera buffering.
        # This helps reduce delay during fast movements.
        self.camera.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )

        # Request a reasonable frame rate.
        self.camera.set(
            cv2.CAP_PROP_FPS,
            30
        )

    def read(self):
        """
        Capture one frame from the webcam.
        """

        success, frame = self.camera.read()

        if not success:
            return None

        # Mirror webcam.
        # This makes movement feel natural.
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
        Check whether the camera is available.
        """

        return self.camera.isOpened()