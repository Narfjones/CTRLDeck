import sys
import glob
import serial
from time import sleep
import re

#------------------------------------------------------------------------#
# Get list of COM ports, pull output from buffer and check format to     #
# verify that it is a CTRLdeck and then stores the proper port for main  #
# scrip to access.                                                       #
#------------------------------------------------------------------------#

chosenPort = None
lineList = ["1", "\n2", "\n3", "\n4", "\n5", "\n6"]
ser = serial.Serial

def serial_ports():
    """ 
        Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def findDeck():
    global chosenPort
    global ser
    for i in serial_ports(): # Cycle through available COM ports on machine
        try:
            # Connect to COM port
            ser = serial.Serial(
            port = i,\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
                timeout=0)
            sleep(.001) # Short sleep is necessary apparently
            print("Trying to connect to: " + i)
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
                chosenPort = str(i)
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

if __name__ == '__main__':
    findDeck()