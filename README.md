# 🏄‍♂️ GestureSurfer AI

An enterprise-grade, real-time computer vision platform and human-computer interface (HCI) engineered to convert high-speed physical hand kinetics into low-latency, hardware-level keypress events. Designed primarily for fast-paced, continuous-input environments like *Subway Surfers*, GestureSurfer AI bypasses physical peripheral devices by deploying a multi-threaded perception and vector-kinematics pipeline through standard consumer optical webcams.

---

## 🎯 Project Overview & Core Philosophy

Traditional interactive media relies heavily on physical input drivers—keyboards, mice, touchscreens, and game controllers. **GestureSurfer AI** decouples digital input from tactile hardware by utilizing real-time spatial analytics, deep learning feature extraction, and asynchronous key injection. 

By analyzing frame-by-frame anatomical landmark shifts, the platform projects 3D spatial velocity vector fields directly onto OS-level system inputs. The primary objective of GestureSurfer AI is to provide a zero-dependency, plug-and-play spatial tracking system capable of maintaining sub-15ms input latency on standard consumer-grade CPU runtimes without dedicated GPU acceleration.

---

## ✨ Advanced Architecture & Engineering Highlights

### 1. High-Fidelity 21-Point Landmark Detection
Utilizing lightweight single-shot detector frameworks via MediaPipe, the application identifies 21 individual hand joint coordinates ($X, Y, Z$) in real time. The model operates robustly under non-ideal real-world constraints, such as dynamic backlighting, varied skin tones, fast optical motion blur, and minor spatial occlusions.

### 2. Multi-Threaded Camera Ingestion Engine
To prevent thread starvation and visual lag during heavy frame-processing sequences, frame acquisition operates on a dedicated background thread (`camera_stream.py`). This guarantees an unblocked buffer queue for frame consumption, capping frame drops to near-zero even under resource-intensive OS scheduling.

### 3. Dynamic Kinetic Vector Engine
Static pose matching (e.g., rigid "fist" or "thumbs up" signs) is insufficient for high-speed, reaction-heavy games. GestureSurfer AI employs a dynamic displacement and velocity calculation engine:
* Computes temporal velocity vectors ($\Delta X / \Delta t$, $\Delta Y / \Delta t$) across palm centroids and index fingertips.
* Differentiates deliberate vector bursts (swipes) from ambient resting jitter and micro-movements using adaptive confidence thresholds.

### 4. Direct OS Input Injection & Non-Blocking Debouncing
Traditional virtual keystroke simulations often suffer from system polling delays or key-bounce loops. The application uses direct C-type low-level hooks (`pynput` / DirectInput wrappers) coupled with a thread-safe temporal cooldown manager (`INPUT_COOLDOWN_SEC`) to eliminate ghost inputs and double-triggers.

### 5. Real-Time Instrumentation & Telemetry HUD
The integrated rendering engine projects an interactive Heads-Up Display (HUD) directly over the camera feed. This overlay outputs live topological joint wireframes, spatial bounding boxes, directional vector trajectory indicators, and a real-time frame processing latency (FPS) counter for system calibration and debugging.

---

## 🏗️ System Architecture

```text
                                  [ PHYSICAL WEBCAM ]
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │ Multi-Threaded Frame Capture │
                            │    (camera_stream.py)        │
                            └──────────────┬───────────────┘
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │ Matrix Preprocessing Engine  │
                            │ (Horizontal Flip & RGB Conversion)
                            └──────────────┬───────────────┘
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │ MediaPipe Landmark Engine    │
                            │ (21-Point 3D Joint Tracking) │
                            └──────────────┬───────────────┘
                                           │
                                           ▼
                            ┌──────────────────────────────┐
                            │ Kinematic Vector Analytics   │
                            │ (Velocity & Vector Direction)│
                            └──────────────┬───────────────┘
                                           │
                     ┌─────────────────────┴─────────────────────┐
                     ▼                                           ▼
      ┌──────────────────────────────┐            ┌──────────────────────────────┐
      │ OS Key Event Dispatcher      │            │ Telemetry HUD Rendering      │
      │ (Low-Latency Input Injection)│            │ (Live Skeleton & Vector GUI) │
      └──────────────────────────────┘            └──────────────────────────────┘