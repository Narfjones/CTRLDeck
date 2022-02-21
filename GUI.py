from tkinter import *
from tkinter import ttk

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
frm.grid()

# Create Label and align upper left
label2 = Label(frm, text="CTRLdeck").grid(column=0, row=0)

# Create dropdown to choose arduino port
def show():
    portLabel.config( text = portClicked.get() )

# Dropdown menu options
portOptions = [
    "Port 1",
    "Port 2",
    "Port 3",
]

# Datatype of menu text
portClicked = StringVar()

# Initial Menu Text
portClicked.set( "Port 1" )

# Create dropdown menu
portDrop = OptionMenu(frm, portClicked, *portOptions)

# Create portDropdown button
portButton = Button( frm, text = "Choose Your Port", command = show ).grid(column=2, row=0)

# Create dropdown label
portLabel = Label( frm , text = " " ).grid( column=3 , row=0 )

# Loops the window processes
root.mainloop()