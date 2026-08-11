"""
config.py

Central configuration file for GestureSurfer AI.

All important settings for the camera, hand tracking,
gesture detection, and game controls are stored here.
"""

# ============================================================
# CAMERA SETTINGS
# ============================================================

CAMERA_INDEX = 0

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Display camera feed
SHOW_CAMERA = True


# ============================================================
# HAND DETECTION SETTINGS
# ============================================================

# Maximum number of hands to detect
MAX_NUM_HANDS = 1

# Minimum confidence required to detect a hand
MIN_DETECTION_CONFIDENCE = 0.5

# Minimum confidence required to track a detected hand
MIN_TRACKING_CONFIDENCE = 0.45


# ============================================================
# GESTURE SETTINGS
# ============================================================

# Minimum horizontal movement required
# before we consider it a LEFT or RIGHT gesture.
HORIZONTAL_THRESHOLD = 40

# Minimum vertical movement required
# before we consider it an UP or DOWN gesture.
VERTICAL_THRESHOLD = 30

# Number of frames used for movement smoothing
SMOOTHING_FRAMES = 5

# Time in seconds before another game action
# can be triggered.
GESTURE_COOLDOWN = 0.30


# ============================================================
# GAME ACTIONS
# ============================================================

ACTION_LEFT = "LEFT"
ACTION_RIGHT = "RIGHT"
ACTION_JUMP = "JUMP"
ACTION_ROLL = "ROLL"
ACTION_NONE = "NONE"


# ============================================================
# KEYBOARD MAPPING
# ============================================================

# These are the keyboard keys that will eventually
# be sent to Subway Surfers.

KEY_LEFT = "left"
KEY_RIGHT = "right"
KEY_JUMP = "up"
KEY_ROLL = "down"


# ============================================================
# CALIBRATION
# ============================================================

# Number of seconds used for initial calibration
CALIBRATION_TIME = 3


# ============================================================
# DISPLAY / UI
# ============================================================

# Window title
WINDOW_TITLE = "GestureSurfer AI"

# Show hand landmarks on camera
SHOW_LANDMARKS = True

# Show current detected gesture
SHOW_GESTURE = True

# Show FPS
SHOW_FPS = True


# ============================================================
# DEBUGGING
# ============================================================

# Set to True while developing.
# Set to False when you want a cleaner final application.
DEBUG_MODE = True