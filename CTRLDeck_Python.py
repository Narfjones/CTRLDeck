import serial
from time import sleep
import sys
import time
import re
import strstr

ser = serial.Serial(
    port='COM15',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1


def getIntegers(string):
        numbers = [int(x) for x in string.split() if x.isnumeric()]
        return numbers


while True:
        # create string, convert serial input data to a string a store it
        line =  str(ser.readline())

        slider1 = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
        slider2 = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())

        

        print(slider1)

        ser.reset_input_buffer() 
        sleep(.0001)
        
        
        
ser.close()
