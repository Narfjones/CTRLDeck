import serial
import re
from time import sleep

def serial_conversion_1(line):

    sliderlst1 = line.split("|")

    slider1str = str(sliderlst1[0])
               
    return slider1str

def serial_conversion_2(line):

    sliderlst2 = line.split("|")

    slider2str = str(sliderlst2[-1])

    return slider2str
