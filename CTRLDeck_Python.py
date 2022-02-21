import serial
from time import sleep
import sys
import time
import re

# serial data to string functions
import strstr


ser = serial.Serial(
    port='COM20',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)



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
