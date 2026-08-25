"""
game_launcher.py

Launches Subway Surfers in a dedicated Chrome window
and manages the game/camera window layout.

Windows-specific implementation.
"""

import ctypes
import os
import subprocess
import time
from pathlib import Path


# ============================================================
# WINDOWS CONSTANTS
# ============================================================

SW_MAXIMIZE = 3

HWND_TOPMOST = -1
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_SHOWWINDOW = 0x0040


# ============================================================
# GAME LAUNCHER
# ============================================================


class GameLauncher:

    def __init__(self, game_url):

        self.game_url = game_url

        self.chrome_process = None

        self.game_hwnd = None

        # Dedicated Chrome profile for this project.
        # This prevents us from interfering with the user's
        # normal Chrome windows.
        self.profile_dir = (
            Path(__file__).resolve().parent
            / "chrome_profile"
        )

    # ========================================================
    # FIND CHROME
    # ========================================================

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

    # ========================================================
    # LAUNCH GAME
    # ========================================================

    def launch_game(self):

        chrome_path = self.find_chrome()

        if chrome_path is None:

            raise FileNotFoundError(
                "Google Chrome was not found on this computer."
            )

        self.profile_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [

            chrome_path,

            # Dedicated browser profile
            f"--user-data-dir={self.profile_dir}",

            # Open our game as an app-like window
            f"--app={self.game_url}",

            # Maximize the game
            "--start-maximized",

            # Disable unnecessary browser UI
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

        # Give Chrome time to create the window.
        time.sleep(3)

        self.game_hwnd = self.find_game_window()

        if self.game_hwnd:

            self.maximize_game()

            print("Subway Surfers window found.")

        else:

            print(
                "Subway Surfers opened, "
                "but its window could not be located."
            )

    # ========================================================
    # FIND GAME WINDOW
    # ========================================================

    def find_game_window(self):

        if self.chrome_process is None:

            return None

        hwnd_result = {
            "hwnd": None
        }

        user32 = ctypes.windll.user32

        EnumWindowsProc = ctypes.WINFUNCTYPE(
            ctypes.c_bool,
            ctypes.c_void_p,
            ctypes.c_void_p
        )

        def callback(hwnd, lparam):

            process_id = ctypes.c_ulong()

            user32.GetWindowThreadProcessId(
                hwnd,
                ctypes.byref(process_id)
            )

            # Only look at windows belonging to our
            # dedicated Chrome process tree.
            #
            # Chrome may create child processes, so
            # title search is also used below.

            if user32.IsWindowVisible(hwnd):

                length = user32.GetWindowTextLengthW(hwnd)

                if length > 0:

                    buffer = ctypes.create_unicode_buffer(
                        length + 1
                    )

                    user32.GetWindowTextW(
                        hwnd,
                        buffer,
                        length + 1
                    )

                    title = buffer.value.lower()

                    if (
                        "subway"
                        in title
                    ):

                        hwnd_result["hwnd"] = hwnd

                        return False

            return True

        user32.EnumWindows(
            EnumWindowsProc(callback),
            0
        )

        return hwnd_result["hwnd"]

    # ========================================================
    # MAXIMIZE
    # ========================================================

    def maximize_game(self):

        if self.game_hwnd is None:

            return

        ctypes.windll.user32.ShowWindow(
            self.game_hwnd,
            SW_MAXIMIZE
        )

    # ========================================================
    # FOCUS GAME
    # ========================================================

    def focus_game(self):

        if self.game_hwnd is None:

            return

        user32 = ctypes.windll.user32

        user32.ShowWindow(
            self.game_hwnd,
            SW_MAXIMIZE
        )

        user32.SetForegroundWindow(
            self.game_hwnd
        )

    # ========================================================
    # MAKE CAMERA ALWAYS ON TOP
    # ========================================================

    def make_camera_topmost(
        self,
        camera_window_name
    ):

        user32 = ctypes.windll.user32

        hwnd = user32.FindWindowW(
            None,
            camera_window_name
        )

        if not hwnd:

            return False

        # Set topmost
        user32.SetWindowPos(
            hwnd,
            HWND_TOPMOST,
            0,
            0,
            0,
            0,
            SWP_NOSIZE
            | SWP_NOMOVE
            | SWP_SHOWWINDOW
        )

        # Get screen size
        screen_width = (
            user32.GetSystemMetrics(0)
        )

        screen_height = (
            user32.GetSystemMetrics(1)
        )

        # Camera overlay size
        camera_width = 360
        camera_height = 240

        # Small margin from edges
        margin = 15

        # Top-right position
        x = (
            screen_width
            - camera_width
            - margin
        )

        y = margin

        user32.SetWindowPos(
            hwnd,
            HWND_TOPMOST,
            x,
            y,
            camera_width,
            camera_height,
            SWP_SHOWWINDOW
        )

        return True

    # ========================================================
    # CLOSE GAME
    # ========================================================

    def close_game(self):

        if self.chrome_process is None:

            return

        print("Closing Subway Surfers...")

        try:

            self.chrome_process.terminate()

        except Exception:

            pass

        self.chrome_process = None