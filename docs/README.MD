
# 🌊 WaveSync

WaveSync is a desktop audio visualizer that captures system audio in real time and displays animated LED patterns synchronized with music and sound output.

## Features

* Real-time audio visualization
* USB-powered operation
* Compatible with headphones and speakers
* Custom LED animations
* Low-latency audio processing
* Compact desktop design

---

## Hardware Overview

WaveSync captures audio data directly from the computer and converts it into visual effects displayed through an LED matrix/strip.

### System Architecture

```text
PC Audio Output
        │
        ▼
 Audio Processing Software
        │
        ▼
      ESP32
        │
        ▼
    LED Display
```

---

## Components Used

| Component                   | Quantity  |
| --------------------------  | --------- |
| ESP32 Development Board     | 1         |
| WS2812B NEOPIXEL 8 led bars | 1         |

---

## Wiring Diagram

### ESP32 → LED Matrix

```text
ESP32          WS2812B

5V      -----> VCC
GND     -----> GND
GPIO 5  -----> DIN
```

### Power

```text
USB-C
 │
 ├── 5V → ESP32 VIN
 └── GND → ESP32 GND
```

---

## Software Requirements

* Python 3.10+
* ESP32 Arduino Framework
* USB connection

### Python Libraries

```bash
pip install numpy
pip install sounddevice
pip install pycaw
pip install pyserial
```

---

## Project Structure

```text
WaveSync/
│
├── firmware/
│   └── wavesync.ino
│
├── desktop/
│   ├── main.py
│   ├── audio.py
│   └── visualizer.py
│
├── hardware/
│   ├── schematic.png
│   └── enclosure.stl
│
└── README.md
```

---

## Uploading Firmware

1. Open Arduino IDE.
2. Install ESP32 board support.
3. Select your ESP32 board.
4. Open `wavesync.ino`.
5. Upload the firmware.

---

## Running the Desktop Application

Clone the repository:

```bash
git clone https://github.com/yourusername/wavesync.git
cd wavesync
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

## How It Works

1. The desktop application captures system audio.
2. Audio levels are analyzed in real time.
3. Frequency and amplitude data are sent to the ESP32.
4. The ESP32 converts the data into LED animations.
5. LEDs react instantly to music and system sounds.


---

## Team

Developed by Kuzey and Derin.

Built for learning, creativity, and making sound visible.
