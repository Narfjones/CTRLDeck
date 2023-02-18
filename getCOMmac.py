import serial
from serial.tools import list_ports
from time import sleep
import re

chosenPort = None
lineList = ["1", "\n2", "\n3", "\n4", "\n5", "\n6"]
ser = serial.Serial

enmu_ports = enumerate(list_ports.comports())

port = ""

def findDeck():
    global chosenPort
    global ser
    for i, (p, descriptor, hid) in enmu_ports: # Cycle through available COM ports on machine
        try:
            # Connect to COM port
            ser = serial.Serial(
            port = p,\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0)
            sleep(.001) # Short sleep is necessary apparently
            print("Trying to connect to: " + p)
            ser.flush()
            sleep(.01)
            data = str(ser.readline()) # Get any serial output from device
            numSliders = "\n" + str(data.count("|") + 1)
            data = data.lstrip("b'").rstrip("\\r\\n'").strip("|") # strip any newline, carriage return, or extra characters
            RE_D = re.compile('\d') # Create format against which to check the serial data
            def f3(string):
                return RE_D.search(string)
            if f3(data): # If serial string matches format store it in the first line of the COMport file
                global lineList
                chosenPort = str(p)
                chosenPort = chosenPort.rstrip("\n")
                lineList[0] = chosenPort
                lineList[5] = numSliders
                portFile = open("COMport", "w")
                portFile.writelines(lineList)              
                portFile.close()            
                print("Device found and recorded")
                sleep(.01)
                try: # Safely closes connection so that the port can be opened by main script
                    ser.flush()
                    ser.close()
                    print("connection closed")
                except: # Pops if connection cannot be closed
                    print("connection couldn't close")
                
            else: # Pops if the connection is not correct device(serial data doesn't match expected format)
                print("cannot store connection port")
                
        except: # If an exception is thrown we assume the device is already connected somewhere  else. This needs to be more specific.
            try:
                ser.flush()
                ser.close()
            except:
                pass
            print("reached exception")

findDeck()