# 🏄‍♂️ GestureSurfer AI

A high-performance computer vision application that transforms standard webcam input into real-time keyboard control for endless runner games like *Subway Surfers*. By capturing spatial hand dynamics and analyzing landmark coordinates at high frame rates, GestureSurfer AI enables seamless, hands-free gameplay with zero physical hardware dependencies.

---

## ✨ Features

- **21-Point Hand Tracking:** Leverages deep learning perception pipelines to track 21 key anatomical landmarks on the user's hand with high precision under varying light conditions.
- **Vector-Based Motion Engine:** Measures directional velocity and displacement across the Cartesian plane to distinguish intentional swipes from natural hand jitter or static poses.
- **Low-Latency Input Injection:** Ingests frame data, processes spatial vectors, and fires system-level keystrokes in real time for responsive controls.
- **Live Visual HUD:** Displays a transparent overlay featuring hand skeleton tracking, active gesture status, bounding boxes, and performance metrics for easy debugging and calibration.
- **Auto-Mirroring & Spatial Scaling:** Flips the camera feed horizontally for intuitive motion mapping and scales detection sensitivity dynamically based on hand distance from the camera.

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **Computer Vision:** OpenCV
- **Landmark Detection:** MediaPipe
- **Data Processing:** NumPy
- **System Input Injection:** PyAutoGUI / PyNput / DirectKeys

---

## 🎮 Gesture Mapping

| Physical Motion | Directional Vector | Game Action | Default Key |
| :--- | :--- | :--- | :--- |
| **Rapid Upward Swipe** | $+\Delta Y$ velocity spike | Jump | `Up Arrow` / `W` |
| **Rapid Downward Swipe** | $-\Delta Y$ velocity spike | Roll / Duck | `Down Arrow` / `S` |
| **Rapid Leftward Swipe** | $-\Delta X$ velocity spike | Move Left | `Left Arrow` / `A` |
| **Rapid Rightward Swipe** | $+\Delta X$ velocity spike | Move Right | `Right Arrow` / `D` |
| **Neutral / Open Palm** | Within baseline threshold | Idle | None |

---

## ⚙️ System Architecture

1. **Frame Capture:** OpenCV fetches raw camera feeds and passes frames to the preprocessing module.
2. **Preprocessing:** Image matrices are flipped horizontally and normalized for spatial consistency.
3. **Landmark Extraction:** MediaPipe isolates the primary hand bounding box and calculates 3D coordinates for 21 keypoints.
4. **Vector Analysis:** The gesture engine computes hand center movement, displacement rates, and temporal velocity thresholds.
5. **Event Dispatch:** Detected gesture triggers fire OS-level keyboard events while the HUD renders live status data to the user screen.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed on your system.
- A functional USB or integrated webcam.

### Installation

1. **Clone the repository:**
   ```bash
   git clone gesture-surfer-ai
   cd gesture-surfer-ai