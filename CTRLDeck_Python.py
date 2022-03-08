from operator import iconcat
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from getCOM import serial_ports
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import serialValuetoVolume
import threading
import pythoncom

# Create global variable for arduino port. Can't remember if it is still needed
chosenPort = str()

# Create list variable to hold information in buffer file. It must hold these variables so that we don't reference empty indices
global lineList
lineList = ["1", "\n2", "\n3", "\n4", "\n5"] # Default value to maintain the correct number of indicies. 

# Variable for systray icon
global icon

# List to which we append threads
threads = []

#------------------------------------------------------------------
#       Create Functions for getting user chosen port and
#             using it to open the serial port  
#------------------------------------------------------------------

# Get chosen COM port from drop down menu and open serial port
def saveChoice(event):
    global chosenPort
    chosenPort = str(portsVar.get())
    portFile = open("COMport", "w")
    lineList[0] = (chosenPort)
    portFile.writelines(lineList)
    portFile.close()

#------------------------------------------------------------------
#       Create Functions for getting user chosen AudioSession and
#             using it to create AudioController object  
#------------------------------------------------------------------

# get chosen sessionID from drop down menu and set session volume to slider 1 value
def saveSlider1(event):
    # Checks for user input choice and runs filedialog function chooseFile()
    process_Name = str(sessionsVar_slider1.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[3] = process_Name
    else:
        pass
    # Opens the temp file and stores the chosen process name
    portFile = open("COMport", "w")
    lineList[1] = ("\n" + process_Name)
    portFile.writelines(lineList)
    portFile.close()

def saveSlider2(event):
    process_Name = str(sessionsVar_slider2.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[3] = process_Name
    else:
        pass
    portFile = open("COMport", "w")
    lineList[2] = ("\n" + process_Name)
    portFile.writelines(lineList)
    portFile.close()

def saveSlider3(event):
    process_Name = str(sessionsVar_slider3.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[3] = process_Name
    else:
        pass
    portFile = open("COMport", "w")
    lineList[3] = ("\n" + process_Name)
    portFile.writelines(lineList)
    portFile.close()

def saveSlider4(event):
    process_Name = str(sessionsVar_slider4.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[4] = process_Name
    else:
        pass
    portFile = open("COMport", "w")
    lineList[4] = ("\n" + process_Name)
    portFile.writelines(lineList)
    portFile.close()

# Opens filedialog and allows user to choose .exe file to which they wish to assign slider
def chooseFile():
    filetypes = (
        ('Executables', '*.exe'),
    )

    filename = filedialog.askopenfilename(
        title='Choose a file:',
        initialdir='/',
        filetypes=filetypes)
    # Strip file location and pull just the filename
    filename = filename.split('/')
    # Return filename.exe
    return(str(filename[-1]))


    
#------------------------------------------------------------------
#                          Create GUI
# -----------------------------------------------------------------   

# Create Window
root = Tk()
root.title("CTRLdeck")
root.geometry('827x508')

# Create background image
bg = PhotoImage(file = "6x4deck-bkgrd.png")

# Create a child frame from root
frm = ttk.Frame(root, padding = 0)

# Generate grid for alignment purposes
frm.grid()
labelbg = Label(frm, image = bg, width = bg.width(), height = bg.height())
labelbg.grid(column = 0, row = 0)

#----------------------------------------------------------------------------
#   - Call list of COM ports from getCOM
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveChoice()
#----------------------------------------------------------------------------

# Call available COM ports and put in a list
portOptions = (serial_ports())
portsVar = StringVar()
# Set default value for menu
portsVar.set("Choose your port:")

# Create dropdown to choose arduino port
def show():
    portLabel.config( textvariable = portsVar.get() )

# Create port dropdown menu
portDrop = OptionMenu(frm, portsVar, *portOptions, command=saveChoice).place(x = 375, y = 5)

# Create port dropdown label
portLabel = Label( frm , textvariable = " " )

#----------------------------------------------------------------------------
#   - Call list of Audio Sessions volume_by_process.py
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveSlider()
#----------------------------------------------------------------------------

# Create list of common audio sessions
sessionOptions = ["master", "chrome.exe", "firefox.exe", "discord.exe", "Choose a file:" ]

# Store audio sessions for slider 1
sessionsVar_slider1 = StringVar()
sessionsVar_slider1.set("Slider 1")

# Store audio sessions for slider 2
sessionsVar_slider2 = StringVar()
sessionsVar_slider2.set("Slider 2")

# Store audio sessions for slider 2
sessionsVar_slider3 = StringVar()
sessionsVar_slider3.set("Slider 3")

# Store audio sessions for slider 2
sessionsVar_slider4 = StringVar()
sessionsVar_slider4.set("Slider 4")

# Create dropdown for audio sessions list for slider 1
def show_audio_sessions_slider1():
    sessionLabel_slider1.config( textvariable = sessionsVar_slider1.get() )

sessionsDrop_slider1 = OptionMenu(frm, sessionsVar_slider1, *sessionOptions, command=saveSlider1).place(x=345, y=60)
sessionLabel_slider1 = Label( frm , textvariable = " " )

# Create session dropdown label for slider2
def show_audio_sessions_slider2():
    sessionLabel_slider2.config( textvariable = sessionsVar_slider2.get())

sessionsDrop_slider2 = OptionMenu(frm, sessionsVar_slider2, *sessionOptions, command=saveSlider2).place(x=440, y=60)
sessionLabel_slider2 = Label( frm, textvariable = " ")

# Create session dropdown label for slider3
def show_audio_sessions_slider3():
    sessionLabel_slider3.config( textvariable = sessionsVar_slider3.get())

sessionsDrop_slider3 = OptionMenu(frm, sessionsVar_slider3, *sessionOptions, command=saveSlider3).place(x=535, y=60)
sessionLabel_slider3 = Label( frm, textvariable = " ")

# Create session dropdown label for slider4
def show_audio_sessions_slider4():
    sessionLabel_slider4.config( textvariable = sessionsVar_slider4.get())

sessionsDrop_slider4 = OptionMenu(frm, sessionsVar_slider4, *sessionOptions, command=saveSlider4).place(x=630, y=60)
sessionLabel_slider4 = Label( frm, textvariable = " ")

# This runs the functions that get serial data, convert to windows accepted values, and assign volumes
def sliderRun():
    pythoncom.CoInitialize() # Necessary to run this function in another thread

    try: # Attempt to close the program first to make sure it isn't already running
        serialValuetoVolume.stop_program()
    except: # If the program throws an exception we assume it's because it's not currently running
        pass 
    serialValuetoVolume.init()
    serialValuetoVolume.connectSerial()
    serialValuetoVolume.getValues()

def clicked():
    # Creates thread and appends it to thread list
    global t
    t = threading.Thread(target=sliderRun) # Sets target function that should run in this thread
    threads.append(t)
    t.start() # Starting thread runs the target function
    global startButton
    startButton = Button(frm, text="Restart CTRLdeck", command=clicked).place(x=720, y=450) # Rename the 'start' button to 'restart'

# Creates start button that runs the clicked which kicks off the actual program
startButton = Button(frm, text="Start CTRLdeck", command=clicked).place(x=720, y=450)

# This is the actual closing function which ends the program and it's associated threads. Only accessed by 'Quit' in the taskbar
def on_closing(icon, item):
    serialValuetoVolume.stop_program() # serialValuetoVolume loop must be stopped before thread can be exited

    # Reset temp file so that the number of entries in list stays the same for next execute. Might be redundant.
    portFile = open("COMport", "w")
    lineList = ["1", "\n2", "\n3", "\n4", "\n5"]
    portFile.writelines(lineList)
    portFile.close()
    try: # Attempt to close thread. This only works if getValues() loop has stopped.
        t.join()
    except: # If this throws an exception we assume it's because it is not running. Could be more specific
        pass
    icon.stop() # Destroys the system tray icon
    root.destroy() # Destroys the window

# Recreates the window from the system tray icon
def open_window(icon, item):
    root.lift() # Brings window to the front
    root.after( 0 , root.deiconify) # Destroys the system tray icon after the window is opened
    icon.stop() # Necessary to destroy system tray icon but I don't know why

# Hide the window and show on the system taskbar
def hide_window():
    global icon
    root.withdraw() # Hides GUI Window
    image=Image.open("fader.ico") 
    menu=(item('Show', open_window) , item('Quit', on_closing)) # Creates right click menu and it's options in the system tray icon
    icon=pystray.Icon("name", image, "CTRLDeck", menu) # Creates click options on system tray icon
    icon.run() # Start system tray icon

# Loops the window processes
root.protocol("WM_DELETE_WINDOW", hide_window)
root.mainloop()
