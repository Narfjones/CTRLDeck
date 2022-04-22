#include <Keyboard.h>
#include <Keypad.h>
#include <Control_Surface.h>

USBMIDI_Interface midi;

CCPotentiometer potentiometers[] = {
  {A0, 0x10},
  {A1, 0x11},
  {A2, 0x12},
  {A3, 0x13}
};

const byte ROWS = 3;
const byte COLS = 2;
const int NUM_SLIDERS = 4;

const int analogInputs[NUM_SLIDERS] = {A0, A1, A2, A3};

float  analogSliderValues[NUM_SLIDERS];
float analogOutputValues[NUM_SLIDERS];

char keys[ROWS][COLS] = {
  {'5', '6'},
  {'3', '4'},
  {'1', '2'}
};

byte rowPins[ROWS] = {6, 7, 8};
byte colPins[COLS] = {2, 3};

char connected = 'n';
int start = 0;
boolean handshake = false;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup() {
  Control_Surface.begin();
  Serial.begin(9600);
  Keyboard.begin();
  
  for (int i = 0; i < NUM_SLIDERS; i++) {
  pinMode(analogInputs[i], INPUT);
  }
  
}

void sendMacroCommand(uint8_t key) {
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(key);
  delay(10);
  Keyboard.releaseAll();
}


void loop() {

    Control_Surface.loop();
    char key = keypad.getKey();
    
    if (key) {
      Serial.println(key);
      switch (key) {
        case '1':
          sendMacroCommand(KEY_F13);
          break;
        case '2':
          sendMacroCommand(KEY_F14);
          break;
        case '3':
          sendMacroCommand(KEY_F15);
          break;
        case '4':
          sendMacroCommand(KEY_F16);
          break;
        case '5':
          sendMacroCommand(KEY_F17);
          break;
        case '6':
          sendMacroCommand(KEY_F18);
          break;
      }

    }
   updateSliderValues();
   sendSliderValues();
   Serial.flush();
    delay(5);

}


void updateSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
     analogSliderValues[i] = map(analogRead(analogInputs[i]), 0, 1022, 0,100);
  }
}

void sendSliderValues() {
  String builtString = String("");
  
  for (int i = 0; i < NUM_SLIDERS; i++) {
    builtString += String((int)analogSliderValues[i]);
    
    if (i < NUM_SLIDERS - 1) {
      builtString += String("|");
    }
  }
  
  Serial.println(builtString);
}

void printSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
    String printedString = String("Slider #") + String(i + 1) + String(": ") + String(analogSliderValues[i]) + String(" mV");
    Serial.write(printedString.c_str());
    if (i < NUM_SLIDERS - 1) {
      Serial.write(" | ");
    } else {
      Serial.write("\n");
    }
  }
}
