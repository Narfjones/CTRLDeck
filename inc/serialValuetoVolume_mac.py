from __future__ import print_function
import profile
from tkinter.constants import X
import serial
from time import sleep
from ctypes import POINTER, cast
from numpy import copy
import logging
import osascript

##################################################################################
# 
#   List of differences for MacOS from Windows
#   1. No unmappedList(cannot enumerate possible programs)
#
#
#
##################################################################################

# Create global variables. I'm sure there's a more efficient way to handle all of this.   
chosenPort = str()
ser = None
portFile = None
fileLines = None
chosenPort = None
sliderProcesses = None
sliders = None
running = None
numSliders = None
faders = []

# Initializes variables and stores values from temp data file in proper places. Should not run before 'Start CTRLdeck' button is clicked.
def init():    
    global chosenPort
    global ser
    global portFile
    global fileLines
    global chosenPort
    global sliderProcesses
    global sliders
    global running
    global numSliders
    
    portFile = open("COMport", "r")
    fileLines = portFile.readlines()
    chosenPort = str(fileLines[0]) # Line 1 is the chosen COMport
    numSliders = str(fileLines[5]) # Line 6 is the number of sliders
    portFile.close()
    chosenPort = chosenPort.rstrip("\n").lstrip("\n")
    numSliders = int(numSliders.rstrip("\n").lstrip("\n"))

    sliderProcesses = []
    
    for i in range(numSliders):
        sliderProcesses.append(str(fileLines[i+1]).rstrip("\n").split(','))
    
    for i in range(len(sliderProcesses)):    
        sliderProcesses[i] = [j for j in sliderProcesses[i]]

    sliders = [] * numSliders

    running = True
    logging.warning('Program Initiated')


# Create serial connect with chosen COM port(from COMport data file) and store in global serial variable
def connectSerial():
    global ser
    global numSliders
    try:
        ser = serial.Serial(
        port = chosenPort,\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
        sleep(.001) # Short sleep is necessary apparently
        print("connected to: " + chosenPort)
        logging.warning('Serial Port connected')
        data = str(ser.readline()) # Get any serial output from device
        numSliders = data.count('|') + 1
        print("ctrldeck connected")
    except: # If an exception is thrown we assume it is already connected. Needs to be more specific.
        logging.warning('Serial Port was unable to connect')
        pass


#---------------------------------------------------------------------------------
#   Receive Serial data, extract slider values, and store them as strings
#---------------------------------------------------------------------------------
def serial_conversion(line, valIndex):

    sliderlst = line.split("|")
    try:
        sliderStr = str(sliderlst[valIndex])
    except IndexError:     
        sliderStr = 'null'
    return sliderStr


#---------------------------------------------------------------------------------
#   Get Devices and store them for use. Doing this in the loop slows down slider.
#   I would like to add an event to update this when a new device is detected.
#---------------------------------------------------------------------------------


def masterVolume(volumeToSet):
    print("setting volume for master")

#    try:
#        # Send volume value to device. Must be float or int(min = -65.25, max = 0)
#        #print("Time to set volume: " + str(time.perf_counter()))
#    except:
#        pass

def micVolume(volumeToSet):
    print("setting volume for microphone")

#    try:
#        volume.SetMasterVolumeLevelScalar(volumeToSet, None)
#    except:
#        pass


# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume
def volumeSlider(sliderNum):

    print(sliderProcesses)
    # Iterate over and set volume for all processes controlled by the supplied slider'
    for sliderProcess in sliderProcesses[sliderNum-1]:
        if sliderProcess != 'None': # Only runs if the sliderProcess was chosen
            # print(sliderProcess)

            # 'master' uses EndpointVolume while processes are done with ISimpleAudioVolume
            if sliderProcess == "'Master'":
                masterVolume(sliders[sliderNum-1])
                #print("Time to assign sliderProcess: " + str(time.perf_counter()))

            elif sliderProcess == "microphone":
                micVolume(sliders[sliderNum-1])

            else:
                print("Changing volume")
                #sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
#                for session in sessions:
#                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
#                    if session.Process and session.Process.name() == sliderProcess:
#                        try:
#                            volume.SetMasterVolume(sliders[sliderNum-1], None) # Send updated volume value
#                        except:
#                            pass


#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    global sliders
    global numSliders
    global faders

    while True: # Infinite loop unless trigger variable is changed by stop_program()
        #timeStart = float( time.perf_counter())
        # getSessionsSpeakers()
        #timeEnd = float( time.perf_counter())
        #timeTaken = str(timeEnd - timeStart)
        #print("Got Sessions and Speakers: " + timeTaken )
        try:
            if (ser.in_waiting > 0): # Checks if there is data in the serial buffer. Always true if connected

                    # Create variables to store value to check against for change
                    previousSliders= []
                    for i in range(numSliders):
                        previousSliders.append(i)

                    #timeStart = float( time.perf_counter())
                    # create string, convert serial input data to a string a store it
                    line =  str(ser.readline())
                    ser.reset_input_buffer()
                    #timeEnd = float( time.perf_counter())
                    #timeTaken = str(timeEnd - timeStart)
                    #print("Got Serial Data: " + timeTaken )

                    # timeStart = float( time.perf_counter())
                    # Get numbers out of serial data. This will be empty if slider has no assignment
                    sliderStrs = []
                    for i in range(numSliders):
                        sliderStrs.append(''.join(x for x in serial_conversion(line, i) if x.isdigit()))

                    # timeEnd = float( time.perf_counter())
                    # timeTaken = str(timeEnd - timeStart)
                    # print("String Convserion: " + timeTaken )
                    for i in range(len(sliderStrs)):
                        # timeStart = float( time.perf_counter())
                        # Convert digit strings to integer, maps (0,100) input to (0,1) output and rounds to two decimal places
                        try:
                            for x in sliderProcesses[i]:
                                y = x.isdigit()
                                if (y == False): # Runs if any slider has process assignment
                                    sliders.append(int(sliderStrs[i])) # The smallest number of sliders is 2 so this will always run. 
                        except:
                            sliders.append('null')

#                        else: # Skip if no sliders or no process assignments
#                            pass
                        # timeEnd = float( time.perf_counter())
                        # timeTaken = str(timeEnd - timeStart)
                        # print("Store Values: " + timeTaken )
                    
                        # timeStart = float( time.perf_counter())

                    # timeEnd = float( time.perf_counter())
                    # timeTaken = str(timeEnd - timeStart)
                    # print("Dead Band: " + timeTaken )

                    # timeStart = float( time.perf_counter())
                    # Check new value against previous value and send new volume if it has changed

                    for i in range(numSliders):
                        if sliders[i] != previousSliders[i]:
                            previousSliders[i] = sliders[i]
                            print(sliders[i])
                            try:
                                if sliders[i] <= 1: # These are currently acting as a deadband. There is probably a better way.
                                    sliders[i] = 0
                                    volumeSlider(i)
                                else:
                                    pass
                            except TypeError:
                                pass
                            volumeSlider(i)
                            if (sliders[i] != 'null'):
                                if (len(faders) < numSliders):
                                    faders.append(sliders[i])
                                else:
                                    faders[i] = sliders[i]
                        else:
                            pass

                    if running == False:
                        break
                    else:
                        pass

        except serial.serialutil.SerialException:
            if running == False:
                break
            else:
                pass
            print('SerialException: Cannot check in_waiting')
            
        sleep(.01)

# Used to end while loop in getValues(). Must be used before thread can terminate.
def stop_program():
    global ser
    global running
    running = False #Set trigger variable to false and loop will end on next iteration
    try: # Try to close the open port. If an exception is thrown we assume the port is already closed. Could be more specific.
        ser.close()
        logging.warning('Serial Port closed')
    except:
        logging.warning('Not able to close Serial Port')
        pass
