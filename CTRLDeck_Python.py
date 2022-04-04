from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from getCOM import serial_ports
from pystray import MenuItem as item
import pystray
from PIL import Image
import serialValuetoVolume
import threading
import pythoncom
import logging

# Create global variable for arduino port. Can't remember if it is still needed
chosenPort = str()

# Create list variable to hold information in buffer file. It must hold these variables so that we don't reference empty indices
global lineList
lineList = ["1", "\n2", "\n3", "\n4", "\n5"] # Default value to maintain the correct number of indicies.
macroList = ["1", "\n2", "\n3", "\n4", "\n5", "\n6", "\n7", "\n8", "\n9", "\n10", "\n11", "\n12"] 

# Variable for systray icon
global icon

# List to which we append threads
threads = []
# Create log file
logging.basicConfig(filename='ctrldeck.log', filemode= 'w', encoding='utf-8', level=logging.DEBUG)

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
        sessionOptions[1] = process_Name
        logging.info('Process ' + process_Name + 'successfully added to Slider 1')
    else:
        pass
    # Opens the temp file and stores the chosen process name
    sessionLabel_1.insert(END, process_Name) 
    global lineList
    listSize = sessionLabel_1.size()
    sliderStr = ''
    sliderList = list(sessionLabel_1.get(0, listSize))
    for item in sliderList:
        sliderStr += str(item) + ","
    lineList[1] = ("\n" + sliderStr)
    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        logging.info(lineList[1] + 'added to Slider 1')
        serialValuetoVolume.init()
    except:
        logging.debug('Process not added to Slider1')


def saveSlider2(event):
    process_Name = str(sessionsVar_slider2.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[2] = process_Name
    else:
        pass
    sessionLabel_2.insert(END, process_Name)
    listSize = sessionLabel_2.size()
    sliderStr = ''
    sliderList = list(sessionLabel_2.get(0, listSize))
    for item in sliderList:
        sliderStr += str(item) + ","
    lineList[2] = ("\n" + sliderStr)
    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        logging.info(lineList[2] + 'added to Slider 2')
        serialValuetoVolume.init()
    except:
        logging.debug('Process not added to Slider 2')
        pass


def saveSlider3(event):
    process_Name = str(sessionsVar_slider3.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[3] = process_Name
    else:
        pass
    sessionLabel_3.insert(END, process_Name)
    listSize = sessionLabel_3.size()
    sliderStr = ''
    sliderList = list(sessionLabel_3.get(0, listSize))
    for item in sliderList:
        sliderStr += str(item) + ","
    lineList[3] = ("\n" + sliderStr)
    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        serialValuetoVolume.init()
        logging.info(lineList[3] + 'added to Slider 3')
    except:
        logging.debug('Process not added to Slider 3')
        pass

def saveSlider4(event):
    process_Name = str(sessionsVar_slider4.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[4] = process_Name
    else:
        pass
    sessionLabel_4.insert(END, process_Name)
    listSize = sessionLabel_4.size()
    sliderStr = ''
    sliderList = list(sessionLabel_4.get(0, listSize))
    for item in sliderList:
        sliderStr += str(item) + ","
    lineList[4] = ("\n" + sliderStr)
    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        logging.info(lineList[4] + 'added to Slider 4')
        serialValuetoVolume.init()
    except:
        logging.debug('Process not added to Slider 4')
        pass

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
root.geometry('1240x720')

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
portDrop = OptionMenu(frm, portsVar, *portOptions, command=saveChoice).place(x = 30, y = 25)

# Create labels
portLabel = Label( frm , textvariable = " " )

# Function to delete items from the ListBox and remove the processes from the sliders
def onselect_1(evt):
    global lineList
    print(len(lineList[1]))

    # Access storage of processes and create widget that triggers on select event in ListBox
    w = evt.widget
    index = int(w.curselection()[0]) # Get index of currently selected process in Listbox
    value = w.get(index) # Get the name of the process to remove
    start = int(lineList[1].find(value)) # Get index of the first letter of the process name
    length= int(len(value)) # Get length of the process name
    stop = int(length + start + 1) # Create ending index of process name
    value1 = (lineList[1][:start] + lineList[1][stop:-1]) # Take linList and create new string with currently selected process removed
    lineList[1] = value1 # Substitute new string into lineList
    sessionLabel_1.delete(index) # Remove the process from the label
    print(len(lineList[1]))
    # Prevent remove command from emptying the indices of lineList. If the number of indices changes the whole program will oh I don't know decide to rob a liquor store.
    if len(lineList[1]) < 3:
        lineList[1] += "2" # Stick in default value for lineList to keep the right number of indices
    else: 
        pass
    # Open file and write new lineList
    portFile = open("COMport", "w")
    portFile.writelines(lineList)
    portFile.close()

def onselect_2(evt):
    global lineList
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    start = int(lineList[2].find(value))
    length= int(len(value))
    stop = int(length + start + 1)
    value1 = (lineList[2][:start] + lineList[2][stop:-1])
    lineList[2] = value1
    sessionLabel_2.delete(index)
    if len(lineList[2]) < 3:
        lineList[2] += "3" # Stick in default value for lineList to keep the right number of indices
    else: 
        pass
    portFile = open("COMport", "w")
    portFile.writelines(lineList)
    portFile.close()

def onselect_3(evt):
    global lineList
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    start = int(lineList[3].find(value))
    length= int(len(value))
    stop = int(length + start + 1)
    value1 = (lineList[3][:start] + lineList[3][stop:-1])
    lineList[3] = value1
    sessionLabel_3.delete(index)
    if len(lineList[3]) < 3:
        lineList[3] += "4" # Stick in default value for lineList to keep the right number of indices
    else: 
        pass
    portFile = open("COMport", "w")
    portFile.writelines(lineList)
    portFile.close()
    
def onselect_4(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    start = int(lineList[4].find(value))
    length= int(len(value))
    stop = int(length + start + 1)
    value1 = (lineList[4][:start] + lineList[4][stop:-1])
    lineList[4] = value1
    sessionLabel_4.delete(index)
    if len(lineList[4]) < 3:
        lineList[4] += "5" # Stick in default value for lineList to keep the right number of indices
    else: 
        pass
    portFile = open("COMport", "w")
    portFile.writelines(lineList)
    portFile.close()

sessionLabel_1 = Listbox( frm, width=14, bd=0, height=3, selectmode="single", borderwidth=0,  )
sessionLabel_1.place(x=1075, y=135)
sessionLabel_1.bind('<<ListboxSelect>>', onselect_1)
sessionLabel_2 = Listbox( frm, width=14, bd=0, height=3 )
sessionLabel_2.place(x=1075, y=230)
sessionLabel_2.bind('<<ListboxSelect>>', onselect_2)
sessionLabel_3 = Listbox( frm, width=14, bd=0, height=3 )
sessionLabel_3.place(x=1075, y=327)
sessionLabel_3.bind('<<ListboxSelect>>', onselect_3)
sessionLabel_4 = Listbox( frm, width=14, bd=0, height=3 )
sessionLabel_4.place(x=1075, y=440)
sessionLabel_4.bind('<<ListboxSelect>>', onselect_4)



#----------------------------------------------------------------------------
#   - Call list of Audio Sessions volume_by_process.py
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveSlider()
#----------------------------------------------------------------------------

# Create list of common audio sessions
sessionOptions = ["master", "chrome.exe", "firefox.exe", "discord.exe", "microphone", "unmapped", "Choose a file:" ]

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

sessionsDrop_slider1 = OptionMenu(frm, sessionsVar_slider1, *sessionOptions, command=saveSlider1).place(x=455, y=60)
sessionLabel_slider1 = Label( frm , textvariable = " " )

# Create session dropdown label for slider2
def show_audio_sessions_slider2():
    sessionLabel_slider2.config( textvariable = sessionsVar_slider2.get())

sessionsDrop_slider2 = OptionMenu(frm, sessionsVar_slider2, *sessionOptions, command=saveSlider2).place(x=590, y=60)
sessionLabel_slider2 = Label( frm, textvariable = " ")

# Create session dropdown label for slider3
def show_audio_sessions_slider3():
    sessionLabel_slider3.config( textvariable = sessionsVar_slider3.get())

sessionsDrop_slider3 = OptionMenu(frm, sessionsVar_slider3, *sessionOptions, command=saveSlider3).place(x=720, y=60)
sessionLabel_slider3 = Label( frm, textvariable = " ")

# Create session dropdown label for slider4
def show_audio_sessions_slider4():
    sessionLabel_slider4.config( textvariable = sessionsVar_slider4.get())

sessionsDrop_slider4 = OptionMenu(frm, sessionsVar_slider4, *sessionOptions, command=saveSlider4).place(x=850, y=60)
sessionLabel_slider4 = Label( frm, textvariable = " ")

# This runs the functions that get serial data, convert to windows accepted values, and assign volumes
def sliderRun():
    pythoncom.CoInitialize() # Necessary to run this function in another thread

    try: # Attempt to close the program first to make sure it isn't already running
        serialValuetoVolume.stop_program()
        print("program stopped")
        logging.info('Program was stopped before starting again')
    except: # If the program throws an exception we assume it's because it's not currently running
        pass 
    serialValuetoVolume.init()
    serialValuetoVolume.connectSerial()
    serialValuetoVolume.getValues()

def clicked():
    try:
        serialValuetoVolume.stop_program()
        logging.info('SerialtoVolume stopped before running')
    except:
        logging.debug('SerialtoVolume could not stop')
        pass
    # Creates thread and appends it to thread list
    global t
    t = threading.Thread(target=sliderRun) # Sets target function that should run in this thread
    threads.append(t)
    t.start() # Starting thread runs the target function
    global startButton
    startButton = ttk.Button(frm, text="Restart CTRLdeck", command=clicked).place(x=1110, y=670) # Rename the 'start' button to 'restart'

# Creates start button that runs the clicked which kicks off the actual program
startButton = ttk.Button(frm, text="Start CTRLdeck", command=clicked).place(x=1110, y=670)

# This is the actual closing function which ends the program and it's associated threads. Only accessed by 'Quit' in the taskbar
def on_closing(icon, item):
    serialValuetoVolume.stop_program() # serialValuetoVolume loop must be stopped before thread can be exited
    logging.debug('Serial to Volume stopped')

    # Reset temp file so that the number of entries in list stays the same for next execute. Might be redundant.
    portFile = open("COMport", "w")
    lineList = ["1", "\n2", "\n3", "\n4", "\n5"]
    portFile.writelines(lineList)
    portFile.close()
    logging.debug('File reset')
    try: # Attempt to close thread. This only works if getValues() loop has stopped.
        t.join()
        logging.debug('Thread for volume control ended')
    except: # If this throws an exception we assume it's because it is not running. Could be more 
        logging.debug('Could not end thread')
        pass
    icon.stop() # Destroys the system tray icon
    logging.debug('Icon destroyed')
    root.destroy() # Destroys the window
    logging.debug('Window destroyed')

# Recreates the window from the system tray icon
def open_window(icon, item):
    root.lift() # Brings window to the front
    root.after( 0 , root.deiconify) # Destroys the system tray icon after the window is opened
    logging.debug('System tray con was destroyed for window to open')
    icon.stop() # Necessary to destroy system tray icon but I don't know why

# Hide the window and show on the system taskbar
def hide_window():
    # Store proccesses assigned to sliders to display in icon menu
    sliderProcess1 = str(serialValuetoVolume.sliderProcess1)
    sliderProcess2 = str(serialValuetoVolume.sliderProcess2)
    sliderProcess3 = str(serialValuetoVolume.sliderProcess3)
    sliderProcess4 = str(serialValuetoVolume.sliderProcess4)
    global icon
    root.withdraw() # Hides GUI Window
    logging.debug('Window hidden')
    image=Image.open("fader.ico")
    logging.debug('Icon created')
    menu=(item('Slider 1: ' + sliderProcess1, 0), item('Slider 2: ' + sliderProcess2, 0), item('Slider 3: ' + sliderProcess3, 0),
    item('Slider 4: ' + sliderProcess4, 0), item('Restart', clicked), item('Show', open_window) , item('Quit', on_closing)) # Creates right click menu and it's options in the system tray icon
    icon=pystray.Icon("name", image, "CTRLDeck", menu) # Creates click options on system tray icon
    icon.run() # Start system tray icon
    logging.debug('System tray icon running')

# Loops the window processes
root.protocol("WM_DELETE_WINDOW", hide_window)
root.mainloop()
