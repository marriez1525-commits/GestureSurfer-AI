"""
keyboard_controller.py

Sends keyboard input to the operating system.

The game does not need to know that the input came
from a hand gesture.
"""

import time

import pyautogui


class KeyboardController:
    """
    Controls keyboard input for GestureSurfer AI.
    """

    def __init__(self):

        self.enabled = True

        # Small delay between repeated actions
        self.action_delay = 0.05

    def enable(self):
        """
        Enable keyboard control.
        """

        self.enabled = True

    def disable(self):
        """
        Disable keyboard control.
        """

        self.enabled = False

    def is_enabled(self):
        """
        Check whether keyboard control is enabled.
        """

        return self.enabled

    def press(self, key):
        """
        Press and release a keyboard key.

        Args:
            key: Keyboard key name.
        """

        if not self.enabled:
            return False

        if key is None:
            return False

        try:

            pyautogui.press(key)

            time.sleep(self.action_delay)

            return True

        except Exception as error:

            print(
                f"Keyboard error: {error}"
            )

            return False

    def hold(self, key, duration=0.1):
        """
        Hold a key for a short amount of time.
        """

        if not self.enabled:
            return False

        if key is None:
            return False

        try:

            pyautogui.keyDown(key)

            time.sleep(duration)

            pyautogui.keyUp(key)

            return True

        except Exception as error:

            print(
                f"Keyboard error: {error}"
            )

            return False

    def release_all(self):
        """
        Release common movement keys.

        Useful when stopping the controller.
        """

        keys = [
            "left",
            "right",
            "up",
            "down",
        ]

        for key in keys:

            try:
                pyautogui.keyUp(key)

            except Exception:
                pass