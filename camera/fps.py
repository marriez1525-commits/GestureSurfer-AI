"""
fps.py

Calculates the frames-per-second (FPS) of the
GestureSurfer AI application.
"""

import time


class FPSCounter:

    def __init__(self):
        self.previous_time = time.time()
        self.fps = 0

    def update(self):
        """
        Calculate the current FPS.
        """

        current_time = time.time()

        elapsed_time = current_time - self.previous_time

        if elapsed_time > 0:
            self.fps = 1 / elapsed_time

        self.previous_time = current_time

        return self.fps

    def get_fps(self):
        """
        Return the latest FPS value.
        """

        return self.fps