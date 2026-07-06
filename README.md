# 🏄‍♂️ GestureSurfer AI

GestureSurfer AI is an advanced, human-computer interaction (HCI) project designed to replace traditional hardware controls with seamless, real-time hand gestures. By integrating cutting-edge computer vision with lightweight machine learning pipelines, this application transforms a standard webcam into an intelligent motion-capture sensor. The system is specifically optimized to interface with *Subway Surfers*, translating intuitive, physical swiping motions into instant game commands with minimal latency. 

At its core, the project captures live video frames, isolates structural landmarks on the user's hand, and analyzes directional displacement metrics. When a rapid spatial shift is detected along the horizontal or vertical axes, the software bypasses standard input devices to inject native keyboard events directly into the operating system. This allows players to jump, duck, and switch lanes entirely hands-free, providing an immersive, touchless gaming experience that bridges the gap between digital environments and physical gestures.

---

## 🔥 Key Features

* **High-Precision 21-Point Landmark Tracking**
  The system utilizes a deep learning inference pipeline to map twenty-one distinct spatial coordinates across the palm and fingers. This ensures robust hand tracking, precise orientation tracking, and high fidelity even when the hand undergoes rapid movement or minor structural occlusions during intense gameplay.

* **Dynamic Velocity & Displacement Thresholding**
  To prevent accidental triggers from natural hand jitters, idling, or talking with your hands, the application features a custom displacement algorithm. It evaluates both the distance and the speed of a movement, executing a game command (like a jump or lane change) only when a gesture crosses a specific acceleration threshold.

* **Real-Time Visual HUD & Telemetry Overlay**
  The interactive user interface provides a live, low-latency Head-Up Display (HUD) layered over the webcam feed. This overlay draws a dynamic bounding box around the tracked hand, highlights active skeletal landmarks, and displays visual text alerts showing which gesture was detected and executed in real time.

* **Automatic Frame Normalization & Mirroring**
  Webcam feeds are inherently mirrored, which can distort directional controls. GestureSurfer AI automatically applies a horizontal flip to the incoming image matrices during the preprocessing phase. This guarantees that a physical swipe to your left accurately registers as a leftward move in the game environment.

* **Universal OS-Level Input Mapping**
  Instead of modifying game files or requiring complex browser extensions, the backend utilizes low-level input simulation. This design allows the script to remain entirely decoupled from the game itself, making it universally compatible with web-based versions, desktop executables, or third-party Android emulators.