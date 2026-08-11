import time
import pyautogui

print("Keyboard test starting...")
print("You have 3 seconds to click Notepad.")
time.sleep(3)

print("Sending LEFT")
pyautogui.press("left")

time.sleep(1)

print("Sending RIGHT")
pyautogui.press("right")

time.sleep(1)

print("Sending UP")
pyautogui.press("up")

time.sleep(1)

print("Sending DOWN")
pyautogui.press("down")

print()
print("Keyboard test complete.")