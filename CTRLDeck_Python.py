import serial
from time import sleep
import sys
import time
import re
from tkinter import *
from tkinter import ttk

from serial.serialwin32 import Serial
from getCOM import serial_ports
import volume_by_process
import strstr # serial data to string functions
from pycaw.pycaw import AudioUtilities

#------------------------------------------------------------------
#       Create Functions for getting user chosen port and
#             using it to open the serial port  
#------------------------------------------------------------------

chosenPort = str() # global variable to store port choice from drop down
ser = None # Create global ser variable

# Get chosen COM port from drop down menu and open serial port
def saveChoice(event):
    chosenPort = str(portsVar.get()[2:-3])
    connectSerial(chosenPort)
    #print(chosenPort)


#------------------------------------------------------------------
#       Create Functions for getting user chosen AudioSession and
#             using it to create AudioController object  
#------------------------------------------------------------------
# get chosen sessionID from drop down menu and set session volume to slider 1 value
def saveSlider1(event):
    process_Name = str(sessionsVar_slider1.get()[0:-4])
    #globals()[process_Name +"_controller"] = (sessionsVar_slider1.get())
    print(process_Name)

# get chosen sessionID from drop down menu and set session volume to slider 2 value
def saveSlider2(event):
    process_Name = str(sessionsVar_slider2.get())
    #volume_by_process.set_volume(process_Name)
    print(process_Name)

# Create serial connect with chosen COM port and store in global serial variable
def connectSerial(chosenPort1):
    global ser 
    ser = serial.Serial(
        port = chosenPort1,\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
    sleep(.01)
    print("connected to: " + chosenPort1)
    

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
#   - Call list of COM ports from getCOM.py
#   - Create dropdown list with a 'clicked' action
#   - Display dropdown list in frame
#   - Send chosen value to saveChoice()
#----------------------------------------------------------------------------

# Call COM ports and put in a list
portOptions = [serial_ports()]
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

# Get list of audio sessions
sessionOptions = (volume_by_process.main())


# Store audio sessions for slider 1
sessionsVar_slider1 = StringVar()
sessionsVar_slider1.set("Slider 1")

# Store audio sessions for slider 2
sessionsVar_slider2 = StringVar()
sessionsVar_slider2.set("Slider 2")

# Create dropdown for audio sessions list for slider 1
def show_audio_sessions_slider1():
    sessionLabel_slider1.config( textvariable = sessionsVar_slider1.get() )
sessionsDrop_slider1 = OptionMenu(frm, sessionsVar_slider1, *sessionOptions, command=saveSlider1).place(x=355, y=60)
sessionLabel_slider1 = Label( frm , textvariable = " " )

# Create session dropdown label for slider2
def show_audio_sessions_slider2():
    sessionLabel_slider2.config( textvariable = sessionsVar_slider2.get())
sessionsDrop_slider2 = OptionMenu(frm, sessionsVar_slider2, *sessionOptions, command=saveSlider2).place(x=460, y=60)
sessionLabel_slider2 = Label( frm, textvariable = " ")

#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())

                # Get numbers out of serial data
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())

                # Convert digit strings to integers
                slider1 = int(slider1str)
                slider2 = int(slider2str)

                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.001)

                print(slider1, slider2)

                # clear input buffer to dump and gathered data during our downtime
                ser.reset_input_buffer() 
                # without this the buffer is empty even after pulling serial data
                sleep(.001)  

                print(slider1, slider2)      

print(ser)

#if connectSerial.ser.in_waiting > 0:
        #while True:
                #getValues()

# Loops the window processes
root.mainloop()
