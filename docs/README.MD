
# 🌊 WaveSync

WaveSync is a desktop audio visualizer that captures system audio in real time and displays animated LED patterns synchronized with music and sound output.


![WaveSync Device Showcase](https://f8d710a55cb9b516d88635f103c2c9f2.r2.cloudflarestorage.com/fallout-prod/x2gqi3knwo88dh5lwbaf49nvmesw?response-content-disposition=inline%3B%20filename%3D%22image.png%22%3B%20filename%2A%3DUTF-8%27%27image.png&response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=5772cb82b969263c7af56eaa97f94e11%2F20260616%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260616T172810Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=d21694b9066868f6dfb1eafe95347f178a38204bd6720931997fd2bed53a364b)

![WaveSync Electronic Schematics](https://f8d710a55cb9b516d88635f103c2c9f2.r2.cloudflarestorage.com/fallout-prod/j5gme1vwfivnm8gs35r6j7rfnr1x?response-content-disposition=inline%3B%20filename%3D%22Screenshot%202026-06-13%20202134.png%22%3B%20filename%2A%3DUTF-8%27%27Screenshot%25202026-06-13%2520202134.png&response-content-type=image%2Fjpeg&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=5772cb82b969263c7af56eaa97f94e11%2F20260616%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260616T172810Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=c20c54f52b2474583490aab3948630f7548dcb757715c698aea6f058b257fe23)


## Features

* Real-time audio visualization
* USB-powered operation
* Compatible with headphones and speakers
* Custom LED animations
* Low-latency audio processing
* Compact desktop design

---

## Hardware Overview

WaveSync captures audio data directly from the computer wia a usb cable and converts it into visual effects displayed through an LED matrix/strip.

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
| WS2812B NEOPIXEL 8 led bars | 7         |

---

## Wiring Diagram

### ESP32 → LED Matrix

```text
ESP32          WS2812B

5V      -----> VCC
GND     -----> GND
GPIO 12  -----> DIN
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
pip install numpy pyserial soundcard scipy
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
git clone https://github.com/FECstudios/wavesync.git
cd wavesync/code
```

Install dependencies:

```bash
pip install numpy pyserial soundcard scipy
```

Run the application:

```bash
python wavesync.py
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

Developed by Kuzey and Derin for HackClub Fallout.

