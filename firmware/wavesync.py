import time
import sys
import warnings
import numpy as np
import soundcard as sc
import serial
import serial.tools.list_ports
from scipy.signal.windows import hann
from typing import Optional, List, Tuple

warnings.filterwarnings("ignore", message="data discontinuity in recording")

# --- Configuration ---
BAUD_RATE: int = 115200
SAMPLE_RATE: int = 48000
BLOCK_SIZE: int = 2048
FPS: int = 60

class DynamicNormalizer:
    """Dynamic scaler to ensure each channel rises smoothly without clipping."""
    def __init__(self, decay_rate: float = 0.95):
        self.max_val: float = 0.001
        self.decay_rate: float = decay_rate

    def normalize(self, value: float) -> int:
        self.max_val = max(self.max_val * self.decay_rate, value)
        if self.max_val <= 0:
            return 0
        scaled = (value / self.max_val) * 255.0
        return int(np.clip(scaled, 0, 255))


def find_esp32_port() -> Optional[str]:
    ports = serial.tools.list_ports.comports()
    esp32_identifiers = ["CP210", "CH340", "UART", "USB Serial"]
    for port in ports:
        description = port.description.upper()
        if any(idf in description for idf in esp32_identifiers):
            return port.device
    return None


def calculate_7_bands(fft_data: np.ndarray, freqs: np.ndarray) -> List[float]:
    """Splits the audio spectrum into 7 precise frequency bands."""
    ranges = [
        (20, 100),     # Band 1: Sub-Bass
        (100, 250),    # Band 2: Bass
        (250, 600),    # Band 3: Low-Mids
        (600, 1500),   # Band 4: Mids
        (1500, 3500),  # Band 5: High-Mids
        (3500, 8000),  # Band 6: Treble/Presence
        (8000, 16000)  # Band 7: Brilliance/High Treble
    ]
    
    bands: List[float] = []
    for low, high in ranges:
        mask = (freqs >= low) & (freqs < high)
        val = float(np.mean(fft_data[mask])) if np.any(mask) else 0.0
        bands.append(val)
    return bands


def audio_capture_loop(ser: serial.Serial) -> None:
    print("[*] Listening to WASAPI loopback...")
    try:
        speaker = sc.default_speaker()
        loopback_mic = sc.get_microphone(id=speaker.id, include_loopback=True)
    except Exception as e:
        print(f"[!] Failed to initialize audio device: {e}")
        return

    window = hann(BLOCK_SIZE)
    
    # Normalizers for 7 channels + 1 overall volume level
    normalizers = [DynamicNormalizer() for _ in range(7)]
    vol_normalizer = DynamicNormalizer()
    
    frames_to_read = int(SAMPLE_RATE / FPS)
    print(f"[*] Active Speaker: {speaker.name}")
    print("[*] Streaming 7-channel data to ESP32 matrix... (Press Ctrl+C to stop)")

    frame_count = 0

    with loopback_mic.recorder(samplerate=SAMPLE_RATE) as mic:
        while True:
            data = mic.record(numframes=frames_to_read)
            mono_audio = np.mean(data, axis=1)

            if len(mono_audio) < BLOCK_SIZE:
                mono_audio = np.pad(mono_audio, (0, BLOCK_SIZE - len(mono_audio)))
            else:
                mono_audio = mono_audio[-BLOCK_SIZE:]

            # Overall Volume (RMS)
            rms_volume = float(np.sqrt(np.mean(mono_audio**2)))
            v_val = vol_normalizer.normalize(rms_volume)

            # FFT Analysis
            windowed_audio = mono_audio * window
            fft_mags = np.abs(np.fft.rfft(windowed_audio))
            freqs = np.fft.rfftfreq(BLOCK_SIZE, d=1.0/SAMPLE_RATE)

            # Calculate and normalize 7 channels
            raw_bands = calculate_7_bands(fft_mags, freqs)
            norm_vals = [normalizers[i].normalize(raw_bands[i]) for i in range(7)]

            # Data Format: ch1,ch2,ch3,ch4,ch5,ch6,ch7,volume\n
            payload = ",".join(map(str, norm_vals)) + f",{v_val}\n"
            ser.write(payload.encode('ascii'))
            ser.flush()

            frame_count += 1
            if frame_count >= 30:
                print(f"[~] Live Signal (7 Bands): {payload.strip()}", end="\r")
                frame_count = 0


def main() -> None:
    print("========================================")
    print("  WaveSync: 7-Channel Equalizer System  ")
    print("========================================")

    while True:
        try:
            print("[*] Searching for ESP32...")
            port = find_esp32_port()
            if not port:
                print("[-] ESP32 not found. Retrying in 2 seconds...")
                time.sleep(2)
                continue
                
            print(f"[+] ESP32 detected: {port}")
            with serial.Serial(port, BAUD_RATE, timeout=1) as ser:
                time.sleep(1.5)
                audio_capture_loop(ser)
                
        except serial.SerialException as e:
            print(f"\n[!] Connection lost: {e}")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[*] Shutting down WaveSync...")
            break

if __name__ == "__main__":
    main()
