#include <FastLED.h>

// --- Hardware & Matrix Configuration ---
#define LED_PIN          4      // Your WS2812B Data Pin
#define NUM_CHANNELS     7      // Number of equalizer columns
#define LEDS_PER_CHANNEL 8      // Number of LEDs per column (Height)
#define NUM_LEDS         56     // Total LEDs (7 x 8)
#define LED_TYPE         WS2812B
#define COLOR_ORDER      GRB

CRGB leds[NUM_LEDS];

// If your column colors look mixed up or inverted, set this to false.
const bool IS_ZIGZAG = true; 

// Storage for incoming 7-channel frequency data and overall volume
int ch[NUM_CHANNELS] = {0, 0, 0, 0, 0, 0, 0};
int volume = 0;

// Equalizer Column Colors (Rainbow effect running from Left to Right: Red to Purple)
const CRGB channelColors[NUM_CHANNELS] = {
  CRGB::Red,       // Band 1: Sub-Bass / Bass
  CRGB::Orange,    // Band 2: Bass
  CRGB::Yellow,    // Band 3: Low-Mids
  CRGB::Green,     // Band 4: Mids
  CRGB::Cyan,      // Band 5: High-Mids
  CRGB::Blue,      // Band 6: Treble
  CRGB::Purple     // Band 7: High Treble / Brilliance
};

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  
  // Power-On Panel Test: Briefly illuminate the entire matrix with a dim white light
  fill_solid(leds, NUM_LEDS, CRGB(30, 30, 30));
  FastLED.show();
  delay(500);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  // Listen for incoming serial packages from the Python desktop script
  if (Serial.available() > 0) {
    String payload = Serial.readStringUntil('\n');
    
    // Parse the incoming data format: ch1,ch2,ch3,ch4,ch5,ch6,ch7,volume
    int parsed = sscanf(payload.c_str(), "%d,%d,%d,%d,%d,%d,%d,%d", 
                        &ch[0], &ch[1], &ch[2], &ch[3], &ch[4], &ch[5], &ch[6], &volume);
    
    if (parsed == 8) {
      drawEqualizer();
    }
  }
}


int getLEDIndex(int col, int row) {
  if (IS_ZIGZAG) {
    if (col % 2 == 1) {
      return (col * LEDS_PER_CHANNEL) + (LEDS_PER_CHANNEL - 1 - row);
    }
  }
  return (col * LEDS_PER_CHANNEL) + row;
}

void drawEqualizer() {
  FastLED.clear();

  // Dynamically scale overall brightness based on the music's volume
  uint8_t dynamicBrightness = map(volume, 0, 255, 30, 255);
  FastLED.setBrightness(dynamicBrightness);

  // Scan through each of the 7 frequency columns
  for (int col = 0; col < NUM_CHANNELS; col++) {
    // Map the 0-255 frequency value to the number of active LEDs in this column (0 to 8)
    int ledsToLight = map(ch[col], 0, 255, 0, LEDS_PER_CHANNEL);
    
    // Illuminate the active LEDs for this specific column with its assigned color
    for (int row = 0; row < ledsToLight; row++) {
      int ledIndex = getLEDIndex(col, row);
      
      // Safety guard check to prevent memory array out-of-bounds writing
      if (ledIndex >= 0 && ledIndex < NUM_LEDS) {
        leds[ledIndex] = channelColors[col];
      }
    }
  }

  // Push the freshly calculated frame buffer to the physical LED matrix
  FastLED.show();
}
