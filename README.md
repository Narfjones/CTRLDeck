
# CTRLDeck-Python
CTRLDeck software in python using pyserial and tkinter
![This is an image](https://raw.githubusercontent.com/Narfjones/CTRLDeck-Python/master/src/repository-graph.png)

**Recent Features Added**
- Runs in background on exit
- Works with any number of sliders up to 4
- Executable now functions properly
- Multiple processes per slider working properly. Click the process in the ListBox to remove it
- System Tray icon shows assignments on mouseover

**Current Issues**
~~- The keystrokes only get noticed if you hold them down for an extended time
~  -  Possibly an issue in the .ino sketches
~  -  Only happens on some decks
~- Added support for multiple processes on one slider
~  - Clicking on a process in the ListBox removes the process
- No warning for 'COM port not chosen' exception

**To-do List**
- Adjust GUI to match number of sliders in device(will require two-way serial communication)
- Add auto device(COMport) finder(will require two-way serial communication)
- Clean up GUI( UX/UI )
- Create modular circuit board for sliders and keys
- Cross-Platform Support(Probably not going to bother with this one myself)
- Instructions for use on first launch
- Add slider assignment options and restart to system tray icon

This project is inspired by the **Deej** software written in **Go** by @omriharel. 
The attached STLs were modified from designs of a macro and slider combo device by **MisterDeck**

**License:** MIT and GPL-3.0
