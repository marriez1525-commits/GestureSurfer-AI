"""
game_launcher.py

Launches Subway Surfers in Chrome.
"""

import os
import subprocess
import time
from pathlib import Path


class GameLauncher:

    def __init__(self, game_url):

        self.game_url = game_url
        self.chrome_process = None

        self.profile_dir = (
            Path(__file__).resolve().parent
            / "chrome_profile"
        )

    def find_chrome(self):

        possible_paths = [

            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),

            os.path.expandvars(
                r"%LocalAppData%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        for path in possible_paths:

            if path and os.path.exists(path):
                return path

        return None

    def launch_game(self):

        chrome_path = self.find_chrome()

        if chrome_path is None:

            raise FileNotFoundError(
                "Google Chrome was not found."
            )

        self.profile_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [
            chrome_path,

            f"--user-data-dir={self.profile_dir}",

            f"--app={self.game_url}",

            "--start-maximized",

            "--disable-session-crashed-bubble",

            "--no-first-run",

            "--no-default-browser-check",
        ]

        print("Starting Subway Surfers...")

        self.chrome_process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Give Chrome time to open.
        time.sleep(4)

        print("Subway Surfers launched.")

    def close_game(self):

        if self.chrome_process is None:
            return

        try:

            self.chrome_process.terminate()

        except Exception:

            pass

        self.chrome_process = None