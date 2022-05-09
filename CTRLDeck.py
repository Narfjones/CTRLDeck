from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from inc.getCOM import serial_ports
from pystray import MenuItem as item
import pystray
from PIL import Image
import inc.serialValuetoVolume as serialValuetoVolume
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
logging.basicConfig(filename='ctrldeck.log', filemode= 'w', level=logging.DEBUG)

#------------------------------------------------------------------
#       Create Functions for getting user chosen port and
#             using it to open the serial port  
#------------------------------------------------------------------

# Get chosen COM port from drop down menu and open serial port
def savePortChoice():
    # global chosenPort
    # chosenPort = port
    portFile = open("COMport", "w")
    # lineList[0] = (chosenPort)
    portFile.writelines(lineList)
    portFile.close()
    

#------------------------------------------------------------------
#       Create Functions for getting user chosen AudioSession and
#             using it to create AudioController object  
#------------------------------------------------------------------

# get chosen sessionID from drop down menu and set session volume to slider sliderNum value
def saveSlider(sliderNum):
    slider = sliders[sliderNum - 1]
    label = labels[sliderNum - 1]

    # Checks for user input choice and runs filedialog function chooseFile()
    process_Name = str(slider.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        if len(process_Name) > 2:
            sessionOptions[sliderNum] = process_Name
        else:
            pass
        logging.info('Process ' + process_Name + 'successfully added to Slider ' +  str(sliderNum))
    else:
        pass

    # Opens the temp file and stores the chosen process name
    label.insert(END, process_Name)
    global lineList
    listSize = label.size()
    sliderStr = ''
    sliderList = list(label.get(0, listSize))
    for item in sliderList:
        sliderStr += str(item) + ","
    lineList[sliderNum] = ("\n" + sliderStr)
    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        logging.info(lineList[sliderNum] + 'added to Slider ' +  str(sliderNum))
        serialValuetoVolume.init()
    except:
        logging.debug('Process was not added to Slider ' + str(sliderNum))


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

# Function to delete items from the ListBox and remove the processes from the sliders
# def onselect(evt, labelNum):
#    label = labels[labelNum - 1]
#
#   print(len(lineList[labelNum]))
#
#    # Access storage of processes and create widget that triggers on select event in ListBox
#    w = evt.widget
#    try:
#        index = int(w.curselection()[0]) # Get index of currently selected process in Listbox
#        value = w.get(index) # Get the name of the process to remove
#        start = int(lineList[labelNum].find(value)) # Get index of the first letter of the process name
#        length= int(len(value)) # Get length of the process name
#        stop = int(length + start + 1) # Create ending index of process name
#        value1 = (lineList[labelNum][:start] + lineList[labelNum][stop:-1]) # Take linList and create new string with currently selected process removed
#        lineList[labelNum] = value1 # Substitute new string into lineList
#        label.delete(index) # Remove the process from the label
#        print(len(lineList[labelNum]))
#        # Prevent remove command from emptying the indices of lineList. If the number of indices changes the whole program will oh I don't know decide to rob a liquor store.
#        if len(lineList[labelNum]) < 3:
#            lineList[labelNum] += str(labelNum + 1) # Stick in default value for lineList to keep the right number of indices
#        else: 
#            pass
#        # Open file and write new lineList
#        portFile = open("COMport", "w")
#        portFile.writelines(lineList)
#        portFile.close()
#    except IndexError:
#        pass
    

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


def start_clicked():
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
    
# Call available COM ports and put in a list
portOptions = (serial_ports())

# Define number of sliders
numSliders = 4

#----------------------------------------------------------------------------
#   - Call list of Audio Sessions volume_by_process.py
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveSlider()
#----------------------------------------------------------------------------

# Create list of common audio sessions
sessionOptions = ["master", "chrome.exe", "firefox.exe", "discord.exe", "microphone", "unmapped", "Choose a file:" ]


sliders = []
for i in range (numSliders):
    slider = str()
    sliders.append(str("Slider " + str(i+1)))

labels = []
