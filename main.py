import ctypes
import time

import cv2
import pyautogui

from camera.camera import Camera
from camera.fps import FPSCounter

from vision.hand_detector import HandDetector
from vision.landmark_tracker import LandmarkTracker
from vision.motion_tracker import MotionTracker
from vision.gesture_classifier import GestureClassifier
from vision.fist_detector import FistDetector
from vision.pinch_detector import PinchDetector

from controller.game_controller import GameController
from launcher.game_launcher import GameLauncher

from config import (
    ACTION_NONE,
    ACTION_HOVERBOARD,
    GAME_URL,
)


CAMERA_WINDOW = "GestureSurfer AI"
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 210
CAMERA_MARGIN = 20

HWND_TOPMOST = -1
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SW_SHOWNOACTIVATE = 4


def position_camera_top_right():
    """Forces the OpenCV camera window to stay pinned at the top right of the screen."""
    user32 = ctypes.windll.user32

    hwnd = user32.FindWindowW(None, CAMERA_WINDOW)
    if not hwnd:
        return False

    screen_width = user32.GetSystemMetrics(0)

    # Calculate top-right coordinates
    x = screen_width - CAMERA_WIDTH - CAMERA_MARGIN
    y = CAMERA_MARGIN

    user32.ShowWindow(hwnd, SW_SHOWNOACTIVATE)
    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        x,
        y,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        SWP_NOACTIVATE | SWP_SHOWWINDOW,
    )
    return True


def main():
    print()
    print("=" * 60)
    print("                GESTURESURFER AI")
    print("=" * 60)

    print("\nStarting camera system...")

    camera = Camera()
    detector = HandDetector()
    landmark_tracker = LandmarkTracker()
    motion_tracker = MotionTracker()
    gesture_classifier = GestureClassifier()
    fist_detector = FistDetector()
    pinch_detector = PinchDetector()
    game_controller = GameController()
    fps_counter = FPSCounter()

    controller_enabled = True
    game_controller.enable()

    # Disable PyAutoGUI fail-safe pause for faster clicks
    pyautogui.FAILSAFE = False

    # OpenCV Window setup
    cv2.namedWindow(CAMERA_WINDOW, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(CAMERA_WINDOW, cv2.WND_PROP_TOPMOST, 1)
    cv2.resizeWindow(CAMERA_WINDOW, CAMERA_WIDTH, CAMERA_HEIGHT)

    game_launcher = GameLauncher(GAME_URL)

    try:
        game_launcher.launch_game()
    except Exception as error:
        print(f"\nGame launch error: {error}")

    game_found = False
    game_focus_done = False

    try:
        while True:
            frame = camera.read()

            if frame is None:
                continue

            frame, landmarks = detector.process(frame)
            action = ACTION_NONE

            if landmarks is not None:
                landmark_tracker.update(landmarks)
                palm_position = landmark_tracker.get_palm_center()
                movement = motion_tracker.update(palm_position)

                action = gesture_classifier.classify(movement)

                # Check fist
                if fist_detector.just_made_fist(landmarks):
                    action = ACTION_HOVERBOARD

                # Check pinch
                elif pinch_detector.just_pinched(landmarks):
                    action = "CONTINUE"

                # Execute actions
                if controller_enabled and action != ACTION_NONE:
                    if action == "CONTINUE":
                        # Click the middle of the screen to activate/continue the web game canvas
                        screen_w, screen_h = pyautogui.size()
                        pyautogui.click(screen_w // 2, screen_h // 2)
                        print("Action executed: CONTINUE (Mouse Click)")
                    else:
                        success = game_controller.execute(action)
                        if success:
                            print(f"Action executed: {action}")

            else:
                gesture_classifier.reset()
                fist_detector.reset()
                pinch_detector.reset()

            fps = fps_counter.update()

            # Drawing HUD status on overlay
            hand_text = "HAND: ON" if detector.is_hand_detected() else "HAND: LOST"
            hand_color = (0, 255, 0) if detector.is_hand_detected() else (0, 0, 255)

            cv2.putText(frame, f"FPS: {fps:.0f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, hand_text, (10, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, hand_color, 2)
            cv2.putText(frame, f"ACTION: {action}", (10, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
            cv2.putText(frame, "FIST = HOVERBOARD", (10, 92), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, "PINCH = CONTINUE", (10, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            cv2.imshow(CAMERA_WINDOW, frame)

            # Keep camera anchored top-right and on top of browser
            position_camera_top_right()

            if not game_found:
                game_found = game_launcher.is_game_available()

            if game_found and not game_focus_done:
                time.sleep(0.5)
                if game_launcher.focus_game():
                    game_focus_done = True

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    except KeyboardInterrupt:
        pass
    finally:
        game_controller.stop()
        detector.close()
        camera.release()
        cv2.destroyAllWindows()
        game_launcher.close_game()


if __name__ == "__main__":
    main()