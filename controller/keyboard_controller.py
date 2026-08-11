"""
keyboard_controller.py

Sends keyboard input without unnecessarily slowing
down the vision/tracking loop.
"""

import pyautogui


class KeyboardController:

    def __init__(self):

        self.enabled = True

        # Safety setting
        pyautogui.PAUSE = 0

        # Prevent PyAutoGUI from triggering its
        # fail-safe unexpectedly during gameplay.
        pyautogui.FAILSAFE = True

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

        self.release_all()

    def is_enabled(self):

        return self.enabled

    def press(self, key):

        if not self.enabled:
            return False

        if key is None:
            return False

        try:

            pyautogui.press(
                key,
                _pause=False
            )

            return True

        except Exception as error:

            print(
                f"Keyboard error: {error}"
            )

            return False

    def hold(self, key, duration=0.05):

        if not self.enabled:
            return False

        if key is None:
            return False

        try:

            pyautogui.keyDown(key)

            # We intentionally don't add a long sleep here.
            # The vision loop must remain responsive.

            pyautogui.keyUp(key)

            return True

        except Exception as error:

            print(
                f"Keyboard error: {error}"
            )

            return False

    def release_all(self):

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