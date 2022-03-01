import serial
from time import sleep
import strstr
from pycaw.pycaw import AudioUtilities

ser = None
portFile = open("COMport.py", "r")
chosenPort = portFile.read()

# Create serial connect with chosen COM port and store in global serial variable
def connectSerial():
    global ser
    ser = serial.Serial(
    port = chosenPort,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
    sleep(.01)
    print("connected to: " + chosenPort)

#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    while True: 
        sleep(.01)
        if (ser.in_waiting > 0):
                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())

                # Get numbers out of serial data
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())

                if (slider1str != ''): # Convert digit strings to integers
                    slider1 = int(slider1str)
                    slider2 = int(slider2str)
                else:
                    pass

                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.002)

                print(slider1, slider2)

                # clear input buffer to dump and gathered data during our downtime
                ser.reset_input_buffer() 

                
                    


                


        else:
            print("The Serial port is no longer connected")
            break

connectSerial()
sleep(.01)
getValues()
