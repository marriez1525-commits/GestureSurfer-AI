"""
config.py

Central configuration for GestureSurfer AI.
"""

# ============================================================
# CAMERA
# ============================================================

CAMERA_INDEX = 0

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

SHOW_CAMERA = True


# ============================================================
# HAND DETECTION
# ============================================================

MAX_NUM_HANDS = 1

MIN_DETECTION_CONFIDENCE = 0.5

MIN_TRACKING_CONFIDENCE = 0.45


# ============================================================
# GESTURE DETECTION
# ============================================================

# Lower values because movement is measured across
# several recent frames.
HORIZONTAL_THRESHOLD = 28

VERTICAL_THRESHOLD = 20

SMOOTHING_FRAMES = 2

GESTURE_COOLDOWN = 0.10


# ============================================================
# ACTIONS
# ============================================================

ACTION_LEFT = "LEFT"

ACTION_RIGHT = "RIGHT"

ACTION_JUMP = "JUMP"

ACTION_ROLL = "ROLL"

ACTION_HOVERBOARD = "HOVERBOARD"

ACTION_NONE = "NONE"


# ============================================================
# KEYBOARD
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
# UI
# ============================================================

WINDOW_TITLE = "GestureSurfer AI"

SHOW_LANDMARKS = True

SHOW_GESTURE = True

SHOW_FPS = True


# ============================================================
# DEBUG
# ============================================================

DEBUG_MODE = True


# ============================================================
# GAME
# ============================================================

GAME_URL = "https://subwaysurfers.gg/"


# ============================================================
# CAMERA OVERLAY
# ============================================================

CAMERA_WINDOW_WIDTH = 360

CAMERA_WINDOW_HEIGHT = 240

CAMERA_MARGIN = 15