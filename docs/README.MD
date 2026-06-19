
#  WaveSync

WaveSync is a desktop audio visualizer that captures system audio in real time and displays animated LED patterns synchronized with music and sound output.


<img width="810" height="1237" alt="image" src="https://github.com/user-attachments/assets/ff536da4-8927-44f4-af15-ea80fe9c820a" />


<table align="center" cellspacing="10">
  <tr>
    <td align="center">
      <img
        src="https://github.com/user-attachments/assets/e1ed68ea-b86d-4f94-bba4-cacf17eec1df"
        height="400"
        alt="WaveSync Aygıtı"
      />
    </td>
    <td align="center">
      <img
        src="https://github.com/user-attachments/assets/8fb8e9ff-7845-4e29-9971-e7669ba1e188"
        height="400"
        alt="WaveSync Spektrum Analizi"
      />
    </td>
  </tr>
</table>

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
4. Open [firmware/wavesync.ino](../firmware/wavesync.ino).
5. Upload the firmware.

---

## Running the Desktop Application

Clone the repository:

```bash
git clone https://github.com/FECstudios/wavesync.git
cd wavesync/firmware
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

