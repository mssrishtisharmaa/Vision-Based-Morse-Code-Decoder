# Vision-Based Morse Code Decoder

A real-time computer vision system that uses eye blinks as an input mechanism to generate and decode Morse code through a webcam.

The system combines OpenCV, MediaPipe FaceMesh, facial landmark tracking, and Eye Aspect Ratio (EAR)-based blink detection to create a hands-free communication interface.

## Features

* Real-time webcam-based eye tracking
* Facial landmark detection using MediaPipe FaceMesh
* Eye Aspect Ratio (EAR)-based blink detection
* Blink-duration-based classification
* Short blink classified as a dot (`.`)
* Long blink classified as a dash (`-`)
* Real-time Morse code generation
* Morse code to text decoding
* Hand-presence-based detection toggle
* Live camera feedback
* Modular Python architecture

## How It Works

The system processes the webcam stream through the following stages:

```text
Webcam Capture
      |
      |
Frame Processing
      |
      |
MediaPipe FaceMesh
      |
      |
Eye Landmark Detection
      |
      |
Eye Aspect Ratio Calculation
      |
      |
Blink Detection
      |
      |
Blink Duration Classification
      |
      |
Morse Symbol Generation
      |
      |
Morse Sequence
      |
      |
Morse Decoder
      |
      |
Text Output
```

### 1. Facial Landmark Detection

The webcam captures video frames that are processed using MediaPipe FaceMesh to identify facial landmarks.

The system focuses on landmarks surrounding both eyes.

### 2. Eye Aspect Ratio

The project calculates the Eye Aspect Ratio (EAR) using six landmarks around each eye.

When the eye closes, the vertical distance between the eyelids decreases, resulting in a lower EAR value.

The EAR is calculated independently for both eyes and then averaged to obtain the final eye-closure signal.

### 3. Blink Detection

The calculated EAR is compared against a configurable threshold.

```text
EAR below threshold
        |
        |
Eye considered closed
        |
        |
Closure duration measured
```

The system uses the duration of the eye closure to determine the corresponding Morse symbol.

### 4. Blink Classification

Blink duration is used to classify Morse symbols.

```text
Short blink  = .
Long blink   = -
```

Examples:

```text
.-     = A
-...   = B
...    = S
---    = O
```

### 5. Morse Decoding

The generated Morse sequence is matched against a Morse-code lookup table and converted into its corresponding character.

Timing gaps between blinks are used to determine when a Morse sequence should be decoded.

## Project Structure

```text
vision-based-morse-code-decoder/
|
├── src/
│   ├── main.py
│   ├── blink_detector.py
│   ├── morse_decoder.py
│   ├── hand_controller.py
│   └── prototype.py
|
├── tests/
|
├── assets/
|
├── README.md
├── requirements.txt
└── .gitignore
```

### Module Responsibilities

| Module               | Responsibility                                   |
| -------------------- | ------------------------------------------------ |
| `main.py`            | Application entry point and real-time processing |
| `blink_detector.py`  | Eye landmark processing and EAR calculation      |
| `morse_decoder.py`   | Morse sequence decoding                          |
| `hand_controller.py` | Hand-based detection toggle                      |
| `prototype.py`       | Original prototype implementation                |

## Tech Stack

### Programming Language

* Python

### Computer Vision

* OpenCV
* MediaPipe FaceMesh

### Numerical Processing

* NumPy

### Core Concepts

* Facial Landmark Detection
* Eye Aspect Ratio
* Real-Time Video Processing
* Blink Detection
* Morse Code Decoding
* Human-Computer Interaction

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd vision-based-morse-code-decoder
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the application using:

```bash
python src/main.py
```

The system opens the webcam and begins processing facial landmarks.

The live interface displays the detection status, eye measurements, current Morse sequence, and decoded output.

Press `Q` to exit the application.

## Detection Parameters

The prototype uses configurable parameters for blink and Morse classification:

```text
BLINK_THRESHOLD
DOT_TIME
DASH_TIME
LETTER_GAP
WORD_GAP
```

These parameters control eye-closure sensitivity and the timing used to distinguish Morse symbols and character boundaries.

## Current Implementation

The current implementation focuses on:

* Real-time facial landmark detection
* EAR-based blink detection
* Blink-duration classification
* Morse sequence generation
* Alphabetic Morse decoding
* Hand-based detection enable and disable control

The project also explores hands-free interaction and blink-based command signaling as part of the computer-vision system.

## Limitations

The system can be affected by real-world computer-vision conditions, including:

* Camera quality
* Lighting conditions
* Head movement
* Eyewear
* Facial landmark stability
* Individual differences in eye shape and blinking behavior

The current implementation uses configurable threshold and timing values rather than fully adaptive user-specific calibration.

## Future Improvements

* Adaptive user-specific EAR calibration
* Temporal smoothing for noisy EAR measurements
* Finite-state-machine-based blink detection
* Improved false-positive filtering
* Support for numeric Morse codes
* Expanded hands-free command control
* Automated unit and integration testing
* Detection accuracy benchmarking
* Latency and FPS measurement
* Improved graphical interface
* Cross-platform support

## Evaluation

The project was tested as a real-time computer-vision system under different practical conditions, including variations in lighting, eyewear, and head movement.

Future versions can include quantitative measurements for:

```text
Detection Accuracy
False Positive Rate
Missed Blink Rate
Average Latency
Frames Per Second
```

Benchmark values should only be reported after being experimentally measured.

## Project Background

This project was developed during an AI/ML internship at Anveshan Foundation, IGDTUW.

The internship involved Python, artificial intelligence and machine-learning fundamentals, OpenCV-based real-time video processing, MediaPipe FaceMesh, facial landmark detection, EAR-based blink detection, and blink-based command decoding.

The internship report describes the development of an AI-based eye-blink detection system for hands-free interaction and coded signaling.

## License

This project is licensed under the MIT License.
