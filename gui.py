from tkinter import *
from tkinter import ttk
from getCOM import serial_ports

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
portsVar = StringVar(frm)
portsVar.set(portOptions[0])

# Create dropdown to choose arduino port
def show():
    portLabel.config( textvariable = portsVar.get() )

# Create dropdown menu
portDrop = OptionMenu(frm, portsVar, *portOptions).place(x = 450, y = 10)

# Create portDropdown button
choosePortLabel= Label( frm, text = "Choose Your Port:").place(x = 350, y = 15)

# Create dropdown label
portLabel = Label( frm , textvariable=" " )

# Loops the window processes
root.mainloop()