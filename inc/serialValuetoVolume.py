from __future__ import print_function
from tkinter.constants import X
import serial
from time import sleep
from pycaw.pycaw import DEVICE_STATE, AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL 
import logging

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
unmappedList = []

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
    global devices
    global sessions
    global numSliders
    
    devices = AudioUtilities.GetSpeakers() # Gets Audio End Point Devices (Speakers, Headphones, Microphones, etc.)
    sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
    portFile = open("COMport", "r")
    fileLines = portFile.readlines()
    chosenPort = str(fileLines[0]) # Line 1 is the chosen COMport
    chosenPort = chosenPort.rstrip("\n")

    numSliders = 4

    sliderProcesses = []
    
    try:
        for i in range(numSliders):
            sliderProcesses.append(str(fileLines[i+1]).rstrip("\n").split(','))
    except IndexError:
        pass
    
    for i in range(len(sliderProcesses)):    
        sliderProcesses[i] = [j for j in sliderProcesses[i] if j != '']
    print(sliderProcesses)

    sliders = [float] * numSliders
    global unmappedList
    unmappedList = sliderProcesses[0] + sliderProcesses[1] + sliderProcesses[2] + sliderProcesses[3]
    running = True
    logging.debug('Program Initiated')


# Create serial connect with chosen COM port(from COMport data file) and store in global serial variable
def connectSerial():
    global ser
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
        logging.debug('Serial Port connected')
        print(sliderProcesses)
    except: # If an exception is thrown we assume it is already connected. Needs to be more specific.
        logging.debug('Serial Port was unable to connect')
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

def getSessionsSpeakers():
    global devices
    global sessions
    devices = AudioUtilities.GetSpeakers()
    sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess


# Master volume communicates with Windows through IAudioEndPointVolume instead of ISimpleAudioVolume.
# Think of it as turning your speakers down instead of sliding the volume mixer fader down.
# Accepts a float or int value respresenting decibels from Max=0 to Min=-60
def masterVolume(volumeToSet):
    global devices
    global sessions

    # Get the devices for the system. Always returns active speaker device
    #devices = AudioUtilities.GetSpeakers()
    #print(type(devices))

    # Activate the interface with the speaker device so you can get and set volume.
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #print("Time to setup interface: " + str(time.perf_counter()))
    try:
        # Send volume value to device. Must be float or int(min = -65.25, max = 0)
        volume.SetMasterVolumeLevelScalar(volumeToSet, None)
        #print("Time to set volume: " + str(time.perf_counter()))
    except:
        pass

def micVolume(volumeToSet):
    # Get the devices for the system. Always returns active speaker device
    devices = AudioUtilities.GetMicrophone()

    # Activate the interface with the speaker device so you can get and set volume.
    interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    try:
        volume.SetMasterVolumeLevelScalar(volumeToSet, None)
    except:
        pass


# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume
def volumeSlider(sliderNum):
    global devices
    global sessions
    # print(sliderProcess1)
    # Iterate over and set volume for all processes controlled by the supplied slider
    for sliderProcess in sliderProcesses[sliderNum-1]:
        if sliderProcess != None: # Only runs if the sliderProcess was chosen
            # print(sliderProcess)

            # 'master' uses EndpointVolume while processes are done with ISimpleAudioVolume
            if sliderProcess == "master":
                masterVolume(sliders[sliderNum-1])
                #print("Time to assign sliderProcess: " + str(time.perf_counter()))

            elif sliderProcess == "microphone":
                micVolume(sliders[sliderNum-1])

            elif sliderProcess == 'unmapped': # If not master, use ISimpleAudioVolume
                global unmappedList
                # sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        # If an audio session is not assigned, change it's volume
                    if session.Process and session.Process.name() not in unmappedList:
                        try:
                            volume.SetMasterVolume(sliders[sliderNum-1], None) # Send updated volume value
                        except:
                            pass

            else:
                #sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if session.Process and session.Process.name() == sliderProcess:
                        try:
                            volume.SetMasterVolume(sliders[sliderNum-1], None) # Send updated volume value
                        except:
                            pass


#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    global sliders
    global numSliders

    while True: # Infinite loop unless trigger variable is changed by stop_program()
        #timeStart = float( time.perf_counter())
        getSessionsSpeakers()
        #timeEnd = float( time.perf_counter())
        #timeTaken = str(timeEnd - timeStart)
        #print("Got Sessions and Speakers: " + timeTaken )
        try:
            if (ser.in_waiting > 0): # Checks if there is data in the serial buffer. Always true if connected

                    # Create variables to store value to check against for change
                    previousSliders= []
                    for i in range(numSliders):
                        previousSliders.append(float())

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

                    if (sliderStrs[0] != '' or sliderStrs[1] !='' or sliderStrs[2] != '' or sliderStrs[3] != ''): # Runs if any slider has process assignment
                        # timeStart = float( time.perf_counter())
                        # Convert digit strings to integer, maps (0,100) input to (0,1) output and rounds to two decimal places
                        for i in range(numSliders):
                            try:
                                sliders[i] = float(float(sliderStrs[i]) * .01) # The smallest number of sliders is 2 so this will always run. 
                                sliders[i] = round(sliders[i], 2)
                            except:
                                sliders[i] = 'null'

                    else: # Skip if no sliders or no process assignments
                        pass
                    # timeEnd = float( time.perf_counter())
                    # timeTaken = str(timeEnd - timeStart)
                    # print("Store Values: " + timeTaken )
                
                    # timeStart = float( time.perf_counter())
                    # These are currently acting as a deadband. There is probably a better way.

                    for i in range(numSliders):
                        try:
                            if sliders[i] <= .00:
                                sliders[i] = 0.00
                                volumeSlider(i+1)
                            else:
                                pass
                        except TypeError:
                            pass

                    # timeEnd = float( time.perf_counter())
                    # timeTaken = str(timeEnd - timeStart)
                    # print("Dead Band: " + timeTaken )

                    # timeStart = float( time.perf_counter())
                    # Check new value against previous value and send new volume if it has changed

                    for i in range(numSliders):
                        if sliders[i] != previousSliders[i]:
                            previousSliders[i] = sliders[i]
                            volumeSlider(i+1)
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


# Used to end while loop in getValues(). Must be used before thread can terminate.
def stop_program():
    global ser
    global running
    running = False #Set trigger variable to false and loop will end on next iteration
    try: # Try to close the open port. If an exception is thrown we assume the port is already closed. Could be more specific.
        ser.close()
        logging.debug('Serial Port closed')
    except:
        logging.debug('Not able to close Serial Port')
        pass
