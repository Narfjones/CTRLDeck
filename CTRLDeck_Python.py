import serial
from time import sleep
import sys
import time
import re

ser = serial.Serial(
    port='COM15',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1

slider1str: str
slider2str: str

def getIntegers(string):
        numbers = [int(x) for x in string.split() if x.isnumeric()]
        return numbers


while True:
        # create string, convert serial input data to a string a store it
        line =  str(ser.readline())

        sliderlst = line.split("|")

        slider1str = re.findall(r'\d+', sliderlst)



        print(type(slider1str))
               
        sleep(.01)

        
        # print the count, serial data string, and up the count
        #print(str(count) + str(': ') + slider1 + str("|") + slider2)
        #count +=1
        
        # sleep for .02 seconds because arduino is outputting every 10 milliseconds
        #sleep(.005)
        
        # clear input buffer to dump gathered data during our downtime
        ser.reset_input_buffer() 
        
        # sleep for another .02 seconds or clearing input buffer prevents new input
        sleep(.01)
        
        
ser.close()
