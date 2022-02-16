import serial
from time import sleep
import sys
import time


ser = serial.Serial(
    port='COM15',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1

while True:
    line =  str(ser.readline())

    print(str(count) + str(': ') + str(line) )
    count = count+1
    line = None

ser.close()
