from __future__ import print_function
import serial
from time import sleep
import strstr
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

chosenPort = str()
ser = None
portFile = open("COMport.py", "r")
fileLines = portFile.readlines()
chosenPort = str(fileLines[0])
chosenPort = chosenPort.rstrip("\n")
sliderProcess1 = str(fileLines[1])
sliderProcess1 = sliderProcess1.rstrip("\n")
sliderProcess2 = str(fileLines[2])
sliderProcess2 = sliderProcess2.rstrip("\n")

substring = ".exe"

# Create serial connect with chosen COM port and store in global serial variable
def connectSerial():
    global ser
    ser = serial.Serial(
    port = chosenPort,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
    sleep(.01)
    print("connected to: " + chosenPort)

def volumeSlider1(volume1):    
    if sliderProcess1 != None:
        
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess1 == "master":
            
            # Take input of (0, 1) and map values to (-20, 0). Similar to arduino map() function
            volume2 = float( (volume2 - 0)*(0 - -20) / (1 - 0) + -20)
            volume2 = round(volume2, 1)
            
            # Get the devices for the system. Always returns active speaker device
            devices = AudioUtilities.GetSpeakers()
            
            # Activate the interface with the speaker device so you can get and set volume.
            interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Send volume value to device. Must be float or int(min = -20, max = 0)
            volume.SetMasterVolumeLevel(volume1, None)
            
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess1:
                    volume.SetMasterVolume(volume1, None)

                

def volumeSlider2(volume2):
    if sliderProcess1 != None:
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess2 == "master":
            volume2 = float( (volume2 - 0)*(0 - -20) / (1 - 0) + -20)
            volume2 = round(volume2, 1)
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevel(volume2, None)
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess2:
                    volume.SetMasterVolume(volume2, None)
                


#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    while True: 
        sleep(.01)
        if (ser.in_waiting > 0):

                slider1previous = float()
                slider2previous = float()

                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())
                ser.reset_input_buffer()
                sleep(.01)

                # Get numbers out of serial data
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())

                if (slider1str != '' or slider2str !=''): 
                    # Convert digit strings to integers
                    global slider1
                    global slider2
                    slider1 = float(float(slider1str) * .01)
                    slider1 = round(slider1, 2)
                    slider2 = float(float(slider2str) * .01)
                    slider2 = round(slider2, 2)
                else:
                    pass

                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.01)
                # print(slider1, slider2)

                if slider1 != slider1previous or slider2 != slider2previous:
                    slider1previous = slider1
                    slider2previous = slider2
                    volumeSlider1(slider1)
                    volumeSlider2(slider2)
                else:
                    pass


                # print(slider1, slider2)            
                


        #else:
           #print("The Serial port is no longer connected")
           #break

connectSerial()
sleep(.01)
getValues()
