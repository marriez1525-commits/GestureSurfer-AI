# 🏄‍♂️ GestureSurfer AI

GestureSurfer AI is a computer vision and machine learning framework designed to turn standard webcams into touchless, motion-capture gaming controllers. By tracking real-time spatial hand telemetry, the application translates physical gestures into hardware-level keyboard inputs. This allows users to control fast-paced endless runner games like *Subway Surfers* entirely hands-free.

The system bridges the physical and digital worlds by replacing traditional keyboard arrays with a dynamic, low-latency gesture execution pipeline.

---

## 🚀 Core Features

### 🎯 21-Point Hand Telemetry Matrix
Utilizes a deep-learning perception model to map 21 distinct anatomical landmarks across the hand (fingertips, knuckles, and wrist joints). This ensure robust tracking stability under varying lighting conditions and complex background environments.

### 🏎️ Ultra-Low Latency Execution Engine
Built on a concurrent data-processing loop that ingests frames, runs neural inference, and injects OS-level keypresses with sub-millisecond execution times, preventing input lag during high-stakes gameplay.

### 🧠 Velocity Vectoring & Anti-Jitter Filtering
Implements dynamic tracking that measures acceleration and spatial displacement across a virtual Cartesian grid. The system intelligently filters out micro-tremors, passive drifting, and accidental hand movements, triggering inputs *only* on deliberate, high-velocity gestures.

### 🖥️ High-Tech HUD Overlay
Features an interactive, live feedback Head-Up Display (HUD) mapped directly onto the video capture window. It renders a real-time digital skeleton over the user's hand and displays active visual cues (e.g., `[TRIGGER: JUMP]`) for instant calibration.

### 🔄 Adaptive Mirroring & Distance Scaling
Automatically mirrors the incoming webcam feed to make directional movements feel natural and intuitive. The tracking thresholds automatically adapt based on the user's distance from the camera, eliminating the need to overextend or strain during gestures.

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