from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from getCOM import serial_ports
# import volume_by_process
import subprocess

# Create variable for arduino port
chosenPort = str()

# Create list variable to hold information in buffer file. It must hold these variables so that we don't reference empty indices
global lineList
lineList = ["1", "\n2", "\n3", "\n4", "\n5"]

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
    process_Name = str(sessionsVar_slider1.get())
    if process_Name == "Choose a file:":
        process_Name = chooseFile()
        sessionOptions[3] = process_Name
    else:
        pass
    portFile = open("COMport", "w")
    lineList[1] = ("\n" + process_Name)
    portFile.writelines(lineList)
    portFile.close()

# get chosen sessionID from drop down menu and set session volume to slider 2 value
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

def chooseFile():
    filetypes = (
        ('Executables', '*.exe'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Choose a file:',
        initialdir='/',
        filetypes=filetypes)
       
    filename = filename.split('/')

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

# Call COM ports and put in a list
portOptions = (serial_ports())
portsVar = StringVar()
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

# Create dropdown for audio sessions list for slider 1
# def show_audio_sessions_slider3():
#    sessionLabel_slider1.config( textvariable = sessionsVar_slider1.get() )
#    
# sessionsDrop_slider1 = OptionMenu(frm, sessionsVar_slider1, *sessionOptions, command=saveSlider3).place(x=355, y=60)
# sessionLabel_slider1 = Label( frm , textvariable = " " )
#
## Create dropdown for audio sessions list for slider 1
# def show_audio_sessions_slider4():
#    sessionLabel_slider1.config( textvariable = sessionsVar_slider1.get() )
#    
# sessionsDrop_slider1 = OptionMenu(frm, sessionsVar_slider1, *sessionOptions, command=saveSlider4).place(x=355, y=60)
# sessionLabel_slider1 = Label( frm , textvariable = " " )

def clicked():
    subprocess.Popen("serialValuetoVolume.py", shell=True)

startButton = Button(frm, text="Start CTRLdeck", command=clicked).place(x=720, y=450)

def on_closing():
        portFile = open("COMport", "w")
        lineList = ["1", "\n2", "\n3", "\n4", "\n5"]
        portFile.writelines(lineList)
        portFile.close()
        root.destroy()


# Loops the window processes
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
