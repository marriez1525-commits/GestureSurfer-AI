# 🏄‍♂️ GestureSurfer AI

GestureSurfer AI is a computer vision and machine learning framework designed to turn a standard webcam into a touchless, motion-capture gaming controller. By tracking real-time spatial hand telemetry, the application translates physical hand gestures into hardware-level keyboard inputs, allowing users to control fast-paced endless runner games like *Subway Surfers* entirely hands-free.

---

## 🚀 Key Features

* **21-Point Hand Telemetry:** Utilizes an advanced perception model to map 21 distinct anatomical landmarks across the hand (fingertips, knuckles, and wrist joints) for stable tracking in diverse environmental lighting.
* **Ultra-Low Latency Execution:** Built on a concurrent data-processing loop that ingests frames, runs neural inference, and injects OS-level keypresses with sub-millisecond execution times to eliminate input lag.
* **Intelligent Anti-Jitter Filtering:** Measures acceleration and spatial displacement across a virtual Cartesian grid, filtering out micro-tremors and accidental movements to trigger inputs *only* on deliberate swipes.
* **Interactive HUD Overlay:** Features a live Head-Up Display (HUD) mapped onto the video capture window, rendering a real-time digital skeleton over the user's hand alongside active action cues (e.g., `[TRIGGER: JUMP]`).
* **Adaptive Mirroring & Distance Scaling:** Automatically mirrors the video feed for intuitive directional mapping and dynamically adjusts tracking thresholds based on the user's distance from the camera.

---

## 🛠️ Technical Architecture

The application relies on a modular Python pipeline optimized for real-time edge processing:

* **Computer Vision & Tracking:** `OpenCV` (Video ingestion and image preprocessing) and `MediaPipe` (Hand landmark inference)
* **Input Injection:** `PyAutoGUI` / Native OS integration for direct, hardware-level keystroke emulation
* **Mathematical Optimization:** `NumPy` for high-speed spatial coordinate and velocity vector calculations

---

## 🎮 Gesture Mapping Matrix

The application maps specific physical hand movements to native Windows keyboard controls to navigate games seamlessly:

| Physical Gesture | Detected Action | Emulated Keypress | Gameplay Result |
| :--- | :--- | :--- | :--- |
| **Rapid Upward Swipe** | High Velocity Y-Axis Displacement | `Up Arrow` | **Jump** |
| **Rapid Downward Swipe** | Low Velocity Y-Axis Displacement | `Down Arrow` | **Duck / Roll** |
| **Rapid Leftward Swipe** | High Velocity X-Axis Displacement | `Left Arrow` | **Move Left Lane** |
| **Rapid Rightward Swipe** | Low Velocity X-Axis Displacement | `Right Arrow` | **Move Right Lane** |

---

## 🛣️ Development Roadmap

Future iterations of GestureSurfer AI aim to expand accessibility, multi-app compatibility, and performance:

* **Dynamic Game Profiles:** Custom mapping configurations for various arcade, racing, and simulation titles.
* **Dual-Hand Tracking:** Multi-hand processing to support compound gestures and complex action mapping (e.g., shooting and moving simultaneously).
* **Static Gesture Shortcuts:** Integration of posture recognition (like a fist or peace sign) to trigger secondary in-game items, menus, or power-ups.
* **Cross-Platform Support:** Expanding high-performance native input simulation to macOS and Linux environments.

---

## 📄 License & Purpose

This project is developed exclusively for educational, academic, and research purposes in human-computer interaction (HCI).