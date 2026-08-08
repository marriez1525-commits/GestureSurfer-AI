"""
timer.py

Small timing utilities used throughout GestureSurfer AI.
"""

import time


class Timer:

    def __init__(self):

        self.start_time = None

    def start(self):
        """
        Start the timer.
        """

        self.start_time = time.time()

    def elapsed(self):
        """
        Return elapsed time in seconds.
        """

        if self.start_time is None:
            return 0

        return time.time() - self.start_time

    def reset(self):
        """
        Reset the timer.
        """

        self.start_time = time.time()

    def has_elapsed(self, seconds):
        """
        Check whether a specific amount of time has passed.
        """

        return self.elapsed() >= seconds