#include "Keyboard.h"
#include <Keypad.h>
#include <Control_Surface.h>

USBMIDI_Interface midi;

CCPotentiometer potentiometers[] = {
  {A0, 0x10},
  {A1, 0x11},
};

const byte ROWS = 3;
const byte COLS = 2;
const int NUM_SLIDERS = 2;
const int analogInputs[NUM_SLIDERS] = {A0, A1};

int analogSliderValues[NUM_SLIDERS];

char keys[ROWS][COLS] = {
  {'6', '5'},
  {'4', '3'},
  {'2', '1'}
};

byte rowPins[ROWS] = {6, 7, 8};
byte colPins[COLS] = {2, 3};

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup() {
  Control_Surface.begin();
  Serial.begin(9600);
  Keyboard.begin();

  for (int i = 0; i < NUM_SLIDERS; i++) {
  pinMode(analogInputs[i], INPUT);
  }
  Serial.begin(9600);
  
}

void sendMacroCommand(uint8_t key) {
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(key);
}

void loop() {
  Control_Surface.loop();
    char key = keypad.getKey();

  if (key) {
    Serial.println(key);
    switch (key) {
      case '1':
        sendMacroCommand(KEY_F18);
        break;
      case '2':
        sendMacroCommand(KEY_F17);
        break;
      case '3':
        sendMacroCommand(KEY_F16);
        break;
      case '4':
        sendMacroCommand(KEY_F15);
        break;
      case '5':
        sendMacroCommand(KEY_F14);
        break;
      case '6':
        sendMacroCommand(KEY_F13);
        break;
    }

    delay(30);
    Keyboard.releaseAll();

  }
  
  updateSliderValues();
  sendSliderValues();
  delay(10);
  while(Serial.available())
    Serial.write(Serial.read());
  
}

void updateSliderValues() {
  for (int i = 0; i < NUM_SLIDERS; i++) {
     analogSliderValues[i] = analogRead(analogInputs[i]);
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
