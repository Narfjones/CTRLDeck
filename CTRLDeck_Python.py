import serial
from time import sleep
import sys
import time
import re
from tkinter import *
from tkinter import ttk
from getCOM import serial_ports
import strstr # serial data to string functions

#------------------------------------------------------------------
#       Create Functions for getting user chosen port and
#             using it to connect to the serial port  
#------------------------------------------------------------------
chosenPort = str()
con = False

def saveChoice(event):
    chosenPort = str(portsVar.get()[2:-3])
    connectSerial(chosenPort)
    #print(chosenPort)

def connectSerial(chosenPort):
    ser = serial.Serial(
        port = chosenPort,\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
    print("connected to: " + chosenPort)
    getValues(ser)
    

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
#   - Create dropdown list with a 'Clicked' action
#   - Display dropdown list in frame
#   - Send chosen COM to CTRLdeck_Python.py
#----------------------------------------------------------------------------

# Call COM ports and put in a list
portOptions = [serial_ports()]
portsVar = StringVar()
portsVar.set("Choose your port:")

# Create dropdown to choose arduino port
def show():
    portLabel.config( textvariable = portsVar.get() )

# Create dropdown menu
portDrop = OptionMenu(frm, portsVar, *portOptions, command=saveChoice).place(x = 375, y = 5)

# Create dropdown label
portLabel = Label( frm , textvariable=" " )

#------------------------------------------------------------------
#       Run loop to constantly retrieve serial data
#               and send it to int variables
#------------------------------------------------------------------

def getValues(ser):
        while True:
                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())

                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())
                slider1 = int(slider1str)
                slider2 = int(slider2str)
                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.002)


                print(slider1, slider2)

                # clear input buffer to dump and gathered data during our downtime
                ser.reset_input_buffer() 
                # without this the buffer is empty even after pulling serial data
                sleep(.0001)
        
        ser.close()

# Loops the window processes
root.mainloop()
