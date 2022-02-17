import serial
from time import sleep
import sys
import time
counter=32

ser = serial.Serial(
    port='COM20',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1



while True:
        # create string, convert serial input data to a string a store it
        line =  str(ser.readline())
        
        # print the count, serial data string, and up the count
        print(str(count) + str(': ') + str(line) )
        count +=1
        
        # sleep for .02 seconds because arduino is outputting every 10 milliseconds
        sleep(.002)
        
        # clear input buffer to dump and gathered data during our downtime
        ser.reset_input_buffer() 
        
        # sleep for another .02 seconds or clearing input buffer prevents new input
        sleep(.002)
        
        
ser.close()
