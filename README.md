
# CTRLDeck-Python
CTRLDeck software in python using pyserial and tkinter
![This is an image](https://raw.githubusercontent.com/Narfjones/CTRLDeck-Python/master/src/repository-graph.png)

**Recent Features Added**
- Runs in background on exit
- Works with any number sliders up to 4
- Portable Executable in \dist folder

**Current Issues**
- The keystrokes only get noticed if you hold them down for an extended time( Issue in the .ino files I'm sure)

**To-do List**
- Add support for microphone input level
- Adjust GUI to match number of sliders in device(will require two-way serial communication)
- Add support for multiple processes on one slider
- Clean up GUI( UX/UI )
- Show slider assignment in systray
- Deal with access violation on hide_window


This project is based on the **Deej** software written in **Go** by @omriharel. 
The attached STLs were modified from designs of a macro and slider combo device by **MisterDeck**
