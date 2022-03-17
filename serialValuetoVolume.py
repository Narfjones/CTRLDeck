from __future__ import print_function
from tkinter.constants import X
import serial
from time import sleep
import strstr
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL 

# Create global variables. I'm sure there's a more efficient way to handle all of this.   
chosenPort = str()
ser = None
portFile = None
fileLines = None
chosenPort = None
sliderProcess1 = None
sliderProcess2 = None
sliderProcess3 = None
sliderProcess4 = None
slider1 = None
slider2 = None
slider3 = None
slider4 = None
volume1 = None
volume2 = None
volume3 = None
volume4 = None
running = None
unmappedList = []

# Initializes variables and stores values from temp data file in proper places. Should not run before 'Start CTRLdeck' button is clicked.
def init():    
    global chosenPort
    global ser
    global portFile
    global fileLines
    global chosenPort
    global sliderProcess1
    global sliderProcess2
    global sliderProcess3
    global sliderProcess4
    global slider1
    global slider2
    global slider3
    global slider4
    global volume1
    global volume2
    global volume3
    global volume4
    global running
    
    portFile = open("COMport", "r")
    fileLines = portFile.readlines()
    chosenPort = str(fileLines[0]) # Line 1 is the chosen COMport
    chosenPort = chosenPort.rstrip("\n")
    sliderProcess1 = str(fileLines[1]) # Line 2 is the first slider process assignment
    sliderProcess1 = sliderProcess1.rstrip("\n")
    sliderProcess1 = sliderProcess1.split(',')
    sliderProcess2 = str(fileLines[2])# Line 3 is the second slider process assignment
    sliderProcess2 = sliderProcess2.rstrip("\n")
    sliderProcess2 = sliderProcess2.split(',')
    sliderProcess3 = str(fileLines[3])# Line 4 is the third slider process assignment
    sliderProcess3 = sliderProcess3.rstrip("\n")
    sliderProcess3 = sliderProcess3.split(',')
    sliderProcess4 = str(fileLines[4]) # line 5 is the fourth slider process assignment
    sliderProcess4 = sliderProcess4.rstrip("\n")
    sliderProcess4 = sliderProcess4.split(',')
    global unmappedList
    unmappedList = sliderProcess1 + sliderProcess2 + sliderProcess3 + sliderProcess4
    running = True
    
# Create serial connect with chosen COM port(from COMport data file) and store in global serial variable
def connectSerial():
    global ser
    try:
        ser = serial.Serial(
        port = chosenPort,\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
        sleep(.001) # Short sleep is necessary apparently
        print("connected to: " + chosenPort)
    except: # If an exception is thrown we assume it is already connected. Needs to be more specific.
        pass

# Master volume communicates with Windows through IAudioEndPointVolume instead of ISimpleAudioVolume.
# Think of it as turning your speakers down instead of sliding the volume mixer fader down.
# Accepts a float or int value respresenting decibels from Max=0 to Min=-60
def masterVolume(volume5):
    # Take input of (0, 1) and map values to (-65.25, 0). Similar to arduino map() function
            #volume5 = float( (volume5 - 0)*(0 - -65.25) / (1 - 0) + -65.25)
            #volume5 = round(volume5, 1)
            
            # Get the devices for the system. Always returns active speaker device
            devices = AudioUtilities.GetSpeakers()
            
            # Activate the interface with the speaker device so you can get and set volume.
            interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Send volume value to device. Must be float or int(min = -65.25, max = 0)
            volume.SetMasterVolumeLevelScalar(volume5, None)

def micVolume(volume5):
    # Take input of (0, 1) and map values to (-65.25, 0). Similar to arduino map() function
            #volume5 = float( (volume5 - 0)*(6.0 - 0) / (1 - 0) + 0)
            #volume5 = round(volume5, 1)
            sleep(.005)
            
            # Get the devices for the system. Always returns active speaker device
            devices = AudioUtilities.GetMicrophone()
                        
            # Activate the interface with the speaker device so you can get and set volume.
            interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
        
            volume.SetMasterVolumeLevelScalar(volume5, None)

# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume
def volumeSlider1(volume1):
    # print(sliderProcess1)
    for sliderProcess in sliderProcess1:
        if sliderProcess != None: # Only runs if the sliderProcess was chosen

            # 'master' uses EndpointVolume while processes are done with ISimpleAudioVolume
            if sliderProcess == "master":
                masterVolume(volume1)

            elif sliderProcess == "microphone":
                micVolume(volume1)

            elif sliderProcess == 'unmapped': # If not master, use ISimpleAudioVolume
                global unmappedList
                sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    # If an audio session is not assigned, change it's volume
                    if session.Process and session.Process.name() not in unmappedList:
                        volume.SetMasterVolume(volume1, None) # Send updated volume value

            else:
                sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if session.Process and session.Process.name() == sliderProcess:
                        volume.SetMasterVolume(volume1, None) # Send updated volume value

      
# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume
def volumeSlider2(volume2):
    for sliderProcess in sliderProcess2:
        if sliderProcess != None:
            # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
            if sliderProcess == "master":
                masterVolume(volume2)
            
            elif sliderProcess == "microphone":
                micVolume(volume2)

            elif sliderProcess == 'unmapped': # If not master, use ISimpleAudioVolume
                global unmappedList
                sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    # If an audio session is not assigned, change it's volume
                    if session.Process and session.Process.name() not in unmappedList:
                        volume.SetMasterVolume(volume2, None) # Send updated volume value

            else: # If not master, use ISimpleAudioVolume
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions: # Scans sessions and locates the one with a name matching the sliderProcess
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if session.Process and session.Process.name() == sliderProcess:
                        volume.SetMasterVolume(volume2, None) # Send updated volume value

# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume
def volumeSlider3(volume3):
    for sliderProcess in sliderProcess3:
        if sliderProcess != None:
            # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
            if sliderProcess == "master":
                masterVolume(volume3)
                
            elif sliderProcess == "microphone":
                micVolume(volume3)

            elif sliderProcess == 'unmapped': # If not master, use ISimpleAudioVolume
                global unmappedList
                sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    # If an audio session is not assigned, change it's volume
                    if session.Process and session.Process.name() not in unmappedList:
                        volume.SetMasterVolume(volume3, None) # Send updated volume value

            else: # If not master, use ISimpleAudioVolume
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions: # Scans sessions and locates the one with a name matching the sliderProcess
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if session.Process and session.Process.name() == sliderProcess:
                        volume.SetMasterVolume(volume3, None) # Send updated volume value

# Takes assigned process from slider variable and sends the value to the audio endpoint to update volume               
def volumeSlider4(volume4):
    for sliderProcess in sliderProcess4:
        if sliderProcess != None:
            # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
            if sliderProcess == "master":
                masterVolume(volume4)  
            
            elif sliderProcess4 == "microphone":
                micVolume(volume4)

            elif sliderProcess == 'unmapped': # If not master, use ISimpleAudioVolume
                global unmappedList
                sessions = AudioUtilities.GetAllSessions() # Scans sessions and locates the one with a name matching the sliderProcess
                for session in sessions:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    # If an audio session is not assigned, change it's volume
                    if session.Process and session.Process.name() not in unmappedList:
                        volume.SetMasterVolume(volume4, None) # Send updated volume value

            else:
                sessions = AudioUtilities.GetAllSessions()
                for session in sessions: # Scans sessions and locates the one with a name matching the sliderProcess
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if session.Process and session.Process.name() == sliderProcess:
                        volume.SetMasterVolume(volume4, None)


#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    while True: # Infinite loop unless trigger variable is changed by stop_program()
        sleep(.002)
        if (ser.in_waiting > 0): # Checks if there is data in the serial buffer. Always true if connected

                # Create variables to store value to check against for change
                slider1previous = float()
                slider2previous = float()
                slider3previous = float()
                slider4previous = float()

                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())
                ser.reset_input_buffer()
                sleep(.002) # Necessary or the function will throw exception

                # Get numbers out of serial data. This will be empty if slider has no assignment
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())
                slider3str = ''.join(j for j in strstr.serial_conversion_3(line) if j.isdigit())
                slider4str = ''.join(k for k in strstr.serial_conversion_4(line) if k.isdigit())

                if (slider1str != '' or slider2str !='' or slider3str != '' or slider4str != ''): # Runs if any slider has process assignment
                    global slider1
                    global slider2
                    global slider3
                    global slider4
                    sleep(.002)
                    # Convert digit strings to integer, maps (0,100) input to (0,1) output and rounds to two decimal places
                    slider1 = float(float(slider1str) * .01) # The smallest number of sliders is 2 so this will always run. 
                    slider1 = round(slider1, 2)

                    slider2 = float(float(slider2str) * .01) # The smallest number of sliders is 2 so this will always run
                    slider2 = round(slider2, 2)

                    try: # Runs if there is a slider 3 with an assignment
                        slider3 = float(float(slider3str) * .01) 
                        slider3 = round(slider3, 2)
                    except ValueError: # If no slider or process assignment return 'null'
                        slider3 = 'null'

                    try: # Runs if there is a slider 4 with an assignment
                        slider4 = float(float(slider4str) * .01)
                        slider4 = round(slider4, 2)
                    except ValueError: # If no slider or process assignment return 'null'
                        slider4 = 'null'
                else: # Skip if no sliders or no process assignments
                    pass

                # print(slider1, "|", slider2, "|", slider3, "|", slider4)

                # Wait for buffer to fill
                sleep(.005)

                # Check new value against previous value and send new volume if it has changed
                if slider1 != slider1previous:
                    slider1previous = slider1
                    volumeSlider1(slider1)
                else:
                    pass
                if slider2 != slider2previous:
                    slider2previous = slider2
                    volumeSlider2(slider2)
                else:
                    pass
                if slider3 != slider3previous:
                    slider3previous = slider3
                    volumeSlider3(slider3)
                else:
                    pass
                if slider4!= slider4previous:
                    slider4previous = slider4
                    volumeSlider4(slider4)
                else: # If volume is the same as last iteration do nothing
                    pass
                
                # print(slider1, slider2, slider3, slider4)

                # Check variable to see if main program has requested termination. Loop must stop for thread to be ended.
                if running == False:
                    break
                else:
                    pass


# Used to end while loop in getValues(). Must be used before thread can terminate.
def stop_program():
    global ser
    global running
    running = False #Set trigger variable to false and loop will end on next iteration
    try: # Try to close the open port. If an exception is thrown we assume the port is already closed. Could be more specific.
        ser.close()
    except:
        pass