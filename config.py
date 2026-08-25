"""
config.py

Central configuration file for GestureSurfer AI.

All important settings for the camera, hand tracking,
gesture detection, game controls, and game launching
are stored here.
"""


# ============================================================
# CAMERA SETTINGS
# ============================================================

CAMERA_INDEX = 0

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

SHOW_CAMERA = True


# ============================================================
# HAND DETECTION SETTINGS
# ============================================================

MAX_NUM_HANDS = 1

MIN_DETECTION_CONFIDENCE = 0.5

MIN_TRACKING_CONFIDENCE = 0.45


# ============================================================
# GESTURE SETTINGS
# ============================================================

HORIZONTAL_THRESHOLD = 35

VERTICAL_THRESHOLD = 25

SMOOTHING_FRAMES = 3

GESTURE_COOLDOWN = 0.30


# ============================================================
# GAME ACTIONS
# ============================================================

ACTION_LEFT = "LEFT"

ACTION_RIGHT = "RIGHT"

ACTION_JUMP = "JUMP"

ACTION_ROLL = "ROLL"

ACTION_HOVERBOARD = "HOVERBOARD"

ACTION_NONE = "NONE"


# ============================================================
# KEYBOARD MAPPING
# ============================================================

KEY_LEFT = "left"

KEY_RIGHT = "right"

KEY_JUMP = "up"

KEY_ROLL = "down"

KEY_HOVERBOARD = "space"


# ============================================================
# CALIBRATION
# ============================================================

CALIBRATION_TIME = 3


# ============================================================
# DISPLAY / UI
# ============================================================

WINDOW_TITLE = "GestureSurfer AI"

SHOW_LANDMARKS = True

SHOW_GESTURE = True

SHOW_FPS = True


# ============================================================
# DEBUGGING
# ============================================================

DEBUG_MODE = True


# ============================================================
# SUBWAY SURFERS
# ============================================================

GAME_URL = "https://subwaysurfers.gg/"


# ============================================================
# CAMERA OVERLAY
# ============================================================

CAMERA_WINDOW_WIDTH = 360

CAMERA_WINDOW_HEIGHT = 240

CAMERA_MARGIN = 15