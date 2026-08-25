"""
game_launcher.py

Launches Subway Surfers in a dedicated Chrome window.
"""

import ctypes
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

    # ========================================================
    # FIND CHROME
    # ========================================================

    def find_chrome(self):

        paths = [

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

        for path in paths:

            if path and os.path.exists(path):

                return path

        return None

    # ========================================================
    # LAUNCH
    # ========================================================

    def launch_game(self):

        chrome = self.find_chrome()

        if chrome is None:

            raise FileNotFoundError(
                "Google Chrome was not found."
            )

        self.profile_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [

            chrome,

            f"--user-data-dir={self.profile_dir}",

            f"--app={self.game_url}",

            "--start-maximized",

            "--no-first-run",

            "--no-default-browser-check",

            "--disable-session-crashed-bubble",
        ]

        print(
            "Launching Subway Surfers..."
        )

        self.chrome_process = (
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        )

        time.sleep(4)

        print(
            "Subway Surfers launched."
        )

    # ========================================================
    # FIND GAME WINDOW
    # ========================================================

    def find_game_window(self):

        user32 = ctypes.windll.user32

        result = {
            "hwnd": None
        }

        CALLBACK = ctypes.WINFUNCTYPE(
            ctypes.c_bool,
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        def callback(hwnd, lparam):

            if not user32.IsWindowVisible(hwnd):

                return True

            length = (
                user32.GetWindowTextLengthW(hwnd)
            )

            if length <= 0:

                return True

            buffer = ctypes.create_unicode_buffer(
                length + 1
            )

            user32.GetWindowTextW(
                hwnd,
                buffer,
                length + 1
            )

            title = buffer.value.lower()

            if "subway surfers" in title:

                result["hwnd"] = hwnd

                return False

            return True

        user32.EnumWindows(
            CALLBACK(callback),
            0
        )

        return result["hwnd"]

    # ========================================================
    # FOCUS GAME
    # ========================================================

    def focus_game(self):

        hwnd = self.find_game_window()

        if hwnd is None:

            return False

        user32 = ctypes.windll.user32

        user32.ShowWindow(
            hwnd,
            3
        )

        user32.SetForegroundWindow(
            hwnd
        )

        return True

    # ========================================================
    # CLOSE
    # ========================================================

    def close_game(self):

        if self.chrome_process is None:

            return

        try:

            self.chrome_process.terminate()

        except Exception:

            pass

        self.chrome_process = None