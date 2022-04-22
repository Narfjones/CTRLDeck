from inc.getCOM import serial_ports
from pystray import MenuItem as item
import pystray
from PIL import Image
import inc.serialValuetoVolume as serialValuetoVolume
import threading
import pythoncom
import logging
import eel

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
def savePortChoice(event):
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


# Create dropdown to choose arduino port
def show():
    portLabel.config( textvariable = portsVar.get() )


# Function to delete items from the ListBox and remove the processes from the sliders
def onselect(evt, labelNum):
    global lineList
    label = labels[labelNum - 1]

    print(len(lineList[labelNum]))

    # Access storage of processes and create widget that triggers on select event in ListBox
    w = evt.widget
    try:
        index = int(w.curselection()[0]) # Get index of currently selected process in Listbox
        value = w.get(index) # Get the name of the process to remove
        start = int(lineList[labelNum].find(value)) # Get index of the first letter of the process name
        length= int(len(value)) # Get length of the process name
        stop = int(length + start + 1) # Create ending index of process name
        value1 = (lineList[labelNum][:start] + lineList[labelNum][stop:-1]) # Take linList and create new string with currently selected process removed
        lineList[labelNum] = value1 # Substitute new string into lineList
        label.delete(index) # Remove the process from the label
        print(len(lineList[labelNum]))
        # Prevent remove command from emptying the indices of lineList. If the number of indices changes the whole program will oh I don't know decide to rob a liquor store.
        if len(lineList[labelNum]) < 3:
            lineList[labelNum] += str(labelNum + 1) # Stick in default value for lineList to keep the right number of indices
        else: 
            pass
        # Open file and write new lineList
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
    except IndexError:
        pass
    

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

 #tkinter   startButton = ttk.Button(frm, text="Restart CTRLdeck", command=start_clicked).place(x=1110, y=670) # Rename the 'start' button to 'restart'


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
#tkinter    icon.stop() # Destroys the system tray icon
    logging.debug('Icon destroyed')
#tkinter    root.destroy() # Destroys the window
    logging.debug('Window destroyed')


# Recreates the window from the system tray icon
#tkinter def open_window(icon, item):
#tkinter    root.lift() # Brings window to the front
#tkinter    root.after( 0 , root.deiconify) # Destroys the system tray icon after the window is opened
#tkinter    logging.debug('System tray con was destroyed for window to open')
#tkinter    icon.stop() # Necessary to destroy system tray icon but I don't know why


# Hide the window and show on the system taskbar
def hide_window():
    # Store proccesses assigned to sliders to display in icon menu
    sliderProcesses = []
    for i in range(numSliders):
        try:
            sliderProcesses.append(str(serialValuetoVolume.sliderProcesses[i]))
        except TypeError:
            sliderProcesses.append("No process assigned")z

@eel.expose
def demo(x):
    return x**2

eel.start('index.html', size=(1000, 600))

#tkinter    global icon
#tkinter    root.withdraw() # Hides GUI Window
#tkinter   logging.debug('Window hidden')
#tkinter    image=Image.open("fader.ico")
#tkinter    logging.debug('Icon created')
#tkinter    menu=(item('Slider 1: ' + sliderProcesses[0], 0), item('Slider 2: ' + sliderProcesses[1], 0), item('Slider 3: ' + sliderProcesses[2], 0),
#tkinter    item('Slider 4: ' + sliderProcesses[3], 0), item('Restart', start_clicked), item('Show', open_window) , item('Quit', on_closing)) # Creates right click menu and it's options in the system tray icon
#tkinter    icon=pystray.Icon("name", image, "CTRLDeck", menu) # Creates click options on system tray icon
#tkinter    icon.run() # Start system tray icon
#tkinter    logging.debug('System tray icon running')


#------------------------------------------------------------------
#                          Create GUI
# -----------------------------------------------------------------

### Create Window
#tkinter root = Tk()
#tkinter root.title("CTRLdeck")
#tkinter root.geometry('1240x720')

# Create background image
#tkinter bg = PhotoImage(file = "6x4deck-bkgrd.png")

# Create a child frame from root
#tkinter frm = ttk.Frame(root, padding = 0)

# Generate grid for alignment purposes
#tkinter frm.grid()
#tkinter labelbg = Label(frm, image = bg, width = bg.width(), height = bg.height())
#tkinter labelbg.grid(column = 0, row = 0)

### Set COM Port GUI elements

# Call available COM ports and put in a list
portOptions = (serial_ports())

# Set default value for menu
#tkinter portsVar = StringVar()
#tkinter portsVar.set("Choose your port:")

# Create port dropdown menu
#tkinter portDrop = OptionMenu(frm, portsVar, *portOptions, command=savePortChoice).place(x = 30, y = 25)

# Create label
#tkinter portLabel = Label( frm , textvariable = " " )

### Create slider GUI elements

# Define number of sliders
numSliders = 4

#----------------------------------------------------------------------------
#   - Call list of Audio Sessions volume_by_process.py
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveSlider()
#----------------------------------------------------------------------------

# Create list of common audio sessions
#tkinter sessionOptions = ["master", "chrome.exe", "firefox.exe", "discord.exe", "microphone", "unmapped", "Choose a file:" ]

# Store audio sessions for 4 sliders
#tkinter SliderDropdownsXPositions = [455, 590, 720, 850]
#tkinter SliderDropdownsYPosition = 60

sliders = []
#tkinter for i in range (numSliders):
#tkinter    slider = StringVar()
#tkinter    slider.set("Slider " + str(i+1))
#tkinter    OptionMenu(frm, slider, *sessionOptions, command=lambda event, sliderNum=i+1: saveSlider(sliderNum)).place(x=SliderDropdownsXPositions[i], y=SliderDropdownsYPosition)
#tkinter    sliders.append(slider)

# Create sessionLabels for processes currently controlled by sliders
#tkinter SliderLabelsXPosition = 1075
#tkinter SliderLabelsYPositions = [135, 230, 327, 440]

#tkinter labels = []
#tkinter for i in range (numSliders):
#tkinter     label = Listbox( frm, width=14, bd=0, height=3, selectmode="single", borderwidth=0,  )
#tkinter     label.place(x=SliderLabelsXPosition, y=SliderLabelsYPositions[i])
#tkinter     label.bind('<<ListboxSelect>>', lambda evt, labelNum=i+1 : onselect(evt, labelNum))
#tkinter     labels.append(label)

# Creates start button that runs the clicked which kicks off the actual program
#tkinter startButton = ttk.Button(frm, text="Start CTRLdeck", command=start_clicked).place(x=1110, y=670)

# Loops the window processes
#tkinter root.protocol("WM_DELETE_WINDOW", hide_window)
#tkinter root.mainloop()
