"""
smoothing.py

Smooths hand movement while keeping the controller responsive.
"""

from collections import deque


class MovementSmoother:

    def __init__(self, max_points=4):

        self.max_points = max_points

        self.x_history = deque(
            maxlen=max_points
        )

        self.y_history = deque(
            maxlen=max_points
        )

    def update(self, x, y):

        self.x_history.append(x)

        self.y_history.append(y)

    def get_smoothed_position(self):

        if not self.x_history:
            return None

        average_x = (
            sum(self.x_history)
            / len(self.x_history)
        )

        average_y = (
            sum(self.y_history)
            / len(self.y_history)
        )

        return average_x, average_y

    def reset(self):

        self.x_history.clear()

        self.y_history.clear()

    def get_latest_position(self):

        if not self.x_history:
            return None

        return (
            self.x_history[-1],
            self.y_history[-1]
        )