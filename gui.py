from tkinter import *
from tkinter import ttk
from getCOM import serial_ports

# Create Window
root = Tk()
root.title("CTRLdeck")
root.geometry('827x508')

# Create background image
bg = PhotoImage(file = "6x4deck-bkgrd.png")

labelbg = Label(root, image = bg)
labelbg.place(x=0, y=0)

# Create a child frame from root
frm = ttk.Frame(root, padding=10)

# Generate grid for alignment purposes
# frm.grid()

# Create Label and align upper left
label2 = Label(frm, text="CTRLdeck") # .grid(column=0, row=0)



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
portDrop = OptionMenu(frm, portsVar, *portOptions) # .grid(column=3, row=0)

# Create portDropdown button
# portButton = Button( frm, text = "Choose Your Port", command = show ) #.grid(column=2, row=0)

# Create dropdown label
portLabel = Label( frm , textvariable=" " ) #.grid( column=3 , row=0 )

# Loops the window processes
root.mainloop()