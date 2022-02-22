from tkinter import *
from tkinter import ttk
from getCOM import serial_ports
import serial

# Create Window
root = Tk()
root.title("CTRLdeck")
root.geometry('827x508')

chosenPort = str()

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

# Loops the window processes
root.mainloop()