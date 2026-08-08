"""
smoothing.py

Smooths hand movement so small camera-detection
jitters do not accidentally trigger game actions.
"""

from collections import deque


class MovementSmoother:
    """
    Keeps recent hand positions and calculates
    a smoothed position.
    """

    def __init__(self, max_points=3):
        self.max_points = max_points

        self.x_history = deque(maxlen=max_points)
        self.y_history = deque(maxlen=max_points)

    def update(self, x, y):
        """
        Add a new hand position.
        """

        self.x_history.append(x)
        self.y_history.append(y)

    def get_smoothed_position(self):
        """
        Return the average of recent positions.
        """

        if not self.x_history or not self.y_history:
            return None

        average_x = sum(self.x_history) / len(self.x_history)
        average_y = sum(self.y_history) / len(self.y_history)

        return average_x, average_y

    def reset(self):
        """
        Clear all stored positions.
        """

        self.x_history.clear()
        self.y_history.clear()

    def is_ready(self):
        """
        Check whether enough positions have been collected
        for stable movement detection.
        """

        return len(self.x_history) >= 2