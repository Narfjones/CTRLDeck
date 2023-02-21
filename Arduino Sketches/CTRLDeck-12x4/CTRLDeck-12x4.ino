#include <Keyboard.h>
#include <Keypad.h>
/* #include <Control_Surface.h> */

/* USBMIDI_Interface midi;

CCPotentiometer potentiometers[] = {
  {A0, 0x10},
  {A1, 0x11},
  {A2, 0x12},
  {A3, 0x13},
};
*/

const byte ROWS = 3;
const byte COLS = 4;
const int NUM_SLIDERS = 4;
const int analogInputs[NUM_SLIDERS] = {A0, A1, A2, A3};

int analogSliderValues[NUM_SLIDERS];
int analogSliderValuesPrev[NUM_SLIDERS];

char keys[ROWS][COLS] = {
  {'1', '2', '3', '4'},
  {'5', '6', '7', '8'},
  {'9', '0', 'A', 'B'}
};

byte rowPins[ROWS] = {6, 7, 8};
byte colPins[COLS] = {2, 3, 4, 5};

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup() {
  /* Control_Surface.begin(); */
  Serial.begin(9600);
  Keyboard.begin();

  for (int i = 0; i < NUM_SLIDERS; i++) {
  pinMode(analogInputs[i], INPUT);
  }
  Serial.begin(9600);
  
}

void sendMacroCommand(uint8_t key) {
  Keyboard.press(key);
  Keyboard.releaseAll();
}

void loop() {
  /* Control_Surface.loop(); */
  char key = keypad.getKey();

  if (key) {
    Serial.println(key);
    switch (key) {
      case '1':
        sendMacroCommand(KEY_F24);
        break;
      case '2':
        sendMacroCommand(KEY_F23);
        break;
      case '3':
        sendMacroCommand(KEY_F22);
        break;
      case '4':
        sendMacroCommand(KEY_F21);
        break;
      case '5':
        sendMacroCommand(KEY_F20);
        break;
      case '6':
        sendMacroCommand(KEY_F19);
        break;
        case '7':
        sendMacroCommand(KEY_F18);
        break;
      case '8':
        sendMacroCommand(KEY_F17);
        break;
      case '9':
        sendMacroCommand(KEY_F16);
        break;
      case '0':
        sendMacroCommand(KEY_F15);
        break;
      case 'A':
        sendMacroCommand(KEY_F14);
        break;
      case 'B':
        sendMacroCommand(KEY_F13);
        break;
    }

    delay(20);
    Keyboard.releaseAll();
  }
  
  updateSliderValues();
  sendSliderValues();
  delay(10);
  
}

void updateSliderValues() {
  int sliders[NUM_SLIDERS];
  for (int i = 0; i < NUM_SLIDERS; i++) {
    sliders[i] = analogRead(analogInputs[i]);
    if (sliders[i] - analogSliderValuesPrev[i] > 2 || sliders[i] - analogSliderValuesPrev[i] < -2){
      analogSliderValuesPrev[i] = sliders[i];
      analogSliderValues[i] = sliders[i];
    }

  }
}

void sendSliderValues() {
  String builtString = String("");
  
  for (int i = 0; i < NUM_SLIDERS; i++) {
    builtString += String(analogSliderValues[i]);
    
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
