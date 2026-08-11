"""
game_controller.py

Converts detected gestures into keyboard actions.

Designed so that one detected gesture produces
one keyboard press instead of repeated presses.
"""

import time

from controller.keyboard_controller import KeyboardController
from controller.key_mapper import KeyMapper

from config import ACTION_NONE


class GameController:

    def __init__(self):

        self.keyboard = KeyboardController()

        self.key_mapper = KeyMapper()

        self.last_action = ACTION_NONE

        self.last_execution_time = 0

        # Prevent very fast repeated keyboard presses.
        self.action_interval = 0.35

    def execute(self, action):

        # ----------------------------------------------
        # Controller must be enabled
        # ----------------------------------------------

        if not self.keyboard.is_enabled():
            return False

        # ----------------------------------------------
        # Ignore empty actions
        # ----------------------------------------------

        if action is None:
            return False

        if action == ACTION_NONE:
            return False

        current_time = time.time()

        # ----------------------------------------------
        # Prevent duplicate actions
        # ----------------------------------------------

        elapsed = (
            current_time
            - self.last_execution_time
        )

        if elapsed < self.action_interval:
            return False

        # ----------------------------------------------
        # Convert gesture to keyboard key
        # ----------------------------------------------

        key = self.key_mapper.get_key(action)

        if key is None:
            return False

        # ----------------------------------------------
        # Send ONE keyboard press
        # ----------------------------------------------

        success = self.keyboard.press(key)

        if success:

            self.last_action = action

            self.last_execution_time = current_time

        return success

    def enable(self):

        self.keyboard.enable()

        # Reset timing when controller is enabled.
        self.last_execution_time = 0

        self.last_action = ACTION_NONE

    def disable(self):

        self.keyboard.disable()

        self.last_action = ACTION_NONE

        self.last_execution_time = 0

    def is_enabled(self):

        return self.keyboard.is_enabled()

    def get_last_action(self):

        return self.last_action

    def stop(self):

        self.keyboard.release_all()

        self.keyboard.disable()

        self.last_action = ACTION_NONE

        self.last_execution_time = 0