import sys
import glob
import serial
from time import sleep
import re

#------------------------------------------------------------------------#
# Create list and populate it with available COM ports by checking all   #
#           ports and appending them to list if they return              #
#                   a response to the open command                       #
#------------------------------------------------------------------------#

chosenPort = None
lineList = ["1", "\n2", "\n3", "\n4", "\n5"]
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
    for i in serial_ports():
        try:
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
            data = str(ser.readline())
            data = data.lstrip("b'").rstrip("\\r\\n'").strip("|")
            print(data)
            RE_D = re.compile('\d\d')
            def f3(string):
                return RE_D.search(string)
            if f3(data):
                global lineList
                chosenPort = str(i)
                chosenPort = chosenPort.rstrip("\n")
                lineList[0] = chosenPort
                portFile = open("COMport", "w")
                portFile.writelines(lineList)                
                portFile.close()            
                print("Device found and recorded")
                sleep(.01)
                try:
                    ser.flush()
                    ser.close()
                    print("connection closed")
                except:
                    print("connection couldn't close")
                break
            else:
                print("cannot store connection port")
                break
                   #print(ser.readline())
        except: # If an exception is thrown we assume it is already connected. This needs to be more specific.
            try:
                ser.flush()
                ser.close()
            except:
                pass
            print("reached exception")

if __name__ == '__main__':
    findDeck()
    print(chosenPort)