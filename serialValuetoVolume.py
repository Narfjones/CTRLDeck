import serial
from time import sleep
import strstr

chosenPort1 = None
ser = serial.Serial

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
    sleep(.001)
    return(1)
    print("connected to: " + chosenPort1)

#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues(): 
    while True:
        if (ser.in_waiting > 0):
                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())

                # Get numbers out of serial data
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())

                # Convert digit strings to integers
                slider1 = int(slider1str)
                slider2 = int(slider2str)

                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.005)

                print(slider1, slider2)

                # clear input buffer to dump and gathered data during our downtime
                ser.reset_input_buffer() 
                # without this the buffer is empty even after pulling serial data
                sleep(.005)  

                print(slider1, slider2)
        else:
            print("There is no more data coming from serial")

getValues()