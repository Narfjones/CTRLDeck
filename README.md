
# CTRLDeck-Python
CTRLDeck software in python using pyserial and tkinter
![This is an image](https://raw.githubusercontent.com/Narfjones/CTRLDeck-Python/master/src/repository-graph.png)

**Recent Features Added**
- Runs in background on exit
- Can assign up to 4 sliders
- Executable now functions
- Multiple processes per slider working properly. Click the process in the ListBox to remove it
- System Tray icon shows assignments on mouseover
- Added event logging
- Auto detects CTRLdeck
- Auto detects number of sliders

**Current Issues**
~~- The keystrokes only get noticed if you hold them down for an extended time
~  -  Possibly an issue in the .ino sketches
~  -  Only happens on some decks
~- Added support for multiple processes on one slider
~  - Clicking on a process in the ListBox removes the process
~ - No warning for 'COM port not chosen' exception
- Currently limited to 4 faders
- GUI background does not reflect number of sliders or keys on actual device

**To-do List**
- Add ability to assign the keystroke assignment to macro keys
- Adjust GUI to match number of sliders in device automatically
- Create modular circuit board for sliders and keys
- Cross-Platform Support(Probably not going to bother with this one myself)
- Instructions for use on first launch

This project is inspired by the **Deej** software written in **Go** by @omriharel. 
The attached STLs were modified from designs of a macro and slider combo device by **MisterDeck**

## Use CTRLdeck with your own macro keyboard
  - The CTRLdeck software only controls the slider input. The other inputs are sent using the arduino Keyboard and Midi libraries.
  - To use your own sliders with CTRLdeck they must output the potentiometer value as a number between 0 and 100 using the following format:
          slider1 | slider2 | slider3 | slider4 
  - CTRLdeck takes exclusive control of the serial device but if you are using an HID compatible controller(ATMega32u4), the macro commands will still pass to Windows

**License:** MIT and GPL-3.0
