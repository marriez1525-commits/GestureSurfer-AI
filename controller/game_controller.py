"""
game_controller.py

Connects detected game actions with the keyboard controller.
"""

from controller.keyboard_controller import KeyboardController
from controller.key_mapper import KeyMapper

from config import ACTION_NONE


class GameController:
    """
    Main controller responsible for converting game actions
    into keyboard input.
    """

    def __init__(self):

        self.keyboard = KeyboardController()

        self.key_mapper = KeyMapper()

        self.last_action = ACTION_NONE

    def execute(self, action):
        """
        Execute a game action.

        Example:

            LEFT
              ↓
            left key

            RIGHT
              ↓
            right key

            JUMP
              ↓
            up key

            ROLL
              ↓
            down key
        """

        if action is None:
            return False

        if action == ACTION_NONE:
            return False

        # Find keyboard key
        key = self.key_mapper.get_key(action)

        if key is None:
            return False

        # Send keyboard input
        success = self.keyboard.press(key)

        if success:
            self.last_action = action

        return success

    def enable(self):
        """
        Enable game control.
        """

        self.keyboard.enable()

    def disable(self):
        """
        Disable game control.
        """

        self.keyboard.disable()

        self.keyboard.release_all()

    def is_enabled(self):
        """
        Check whether game control is enabled.
        """

        return self.keyboard.is_enabled()

    def get_last_action(self):
        """
        Return the last successfully executed action.
        """

        return self.last_action

    def stop(self):
        """
        Safely stop the controller.
        """

        self.keyboard.release_all()

        self.keyboard.disable()