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
sliderProcess3 = str(fileLines[3])
sliderProcess3 = sliderProcess3.rstrip("\n")
sliderProcess4 = str(fileLines[4])
sliderProcess4 = sliderProcess4.rstrip("\n")
slider1 = 0
slider2 = 0
slider3 = 0
slider4 = 0
volume1 = 0
volume2 = 0
volume3 = 0
volume4 = 0

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
    sleep(.001)
    print("connected to: " + chosenPort)

def masterVolume(volume5):
    # Take input of (0, 1) and map values to (-20, 0). Similar to arduino map() function
            volume5 = float( (volume5 - 0)*(0 - -50) / (1 - 0) + -50)
            volume5 = round(volume5, 1)
            
            # Get the devices for the system. Always returns active speaker device
            devices = AudioUtilities.GetSpeakers()
            
            # Activate the interface with the speaker device so you can get and set volume.
            interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Send volume value to device. Must be float or int(min = -20, max = 0)
            volume.SetMasterVolumeLevel(volume5, None)


def volumeSlider1(volume1):    
    if sliderProcess1 != None:
        
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess1 == "master":
            masterVolume(volume1)  

        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess1:
                    volume.SetMasterVolume(volume1, None)

                

def volumeSlider2(volume2):
    if sliderProcess2 != None:
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess2 == "master":
            masterVolume(volume2)  
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess2:
                    volume.SetMasterVolume(volume2, None)

def volumeSlider3(volume3):
    if sliderProcess3 != None:
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess3 == "master":
            masterVolume(volume3)  
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess3:
                    volume.SetMasterVolume(volume3, None)
                
def volumeSlider4(volume4):
    if sliderProcess4 != None:
        # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
        if sliderProcess4 == "master":
            masterVolume(volume4)  
        else:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                if session.Process and session.Process.name() == sliderProcess4:
                    volume.SetMasterVolume(4, None)


#------------------------------------------------------------------
#       Create function to retrieve variables and 
#               store them as integers
#------------------------------------------------------------------

def getValues():
    while True: 
        sleep(.002)
        if (ser.in_waiting > 0):

                slider1previous = float()
                slider2previous = float()
                slider3previous = float()
                slider4previous = float()

                # create string, convert serial input data to a string a store it
                line =  str(ser.readline())
                ser.reset_input_buffer()
                sleep(.005)

                # Get numbers out of serial data
                slider1str = ''.join(x for x in strstr.serial_conversion_1(line) if x.isdigit())
                slider2str = ''.join(i for i in strstr.serial_conversion_2(line) if i.isdigit())
                slider3str = ''.join(j for j in strstr.serial_conversion_3(line) if j.isdigit())
                slider4str = ''.join(k for k in strstr.serial_conversion_4(line) if k.isdigit())

                if (slider1str != '' or slider2str !='' or slider3str != '' or slider4str != ''): 
                    global slider1
                    global slider2
                    global slider3
                    global slider4
                    # Convert digit strings to integer
                    slider1 = float(float(slider1str) * .01)
                    slider1 = round(slider1, 2)
                    slider2 = float(float(slider2str) * .01)
                    slider2 = round(slider2, 2)
                    slider3 = float(float(slider3str) * .01)
                    slider3 = round(slider3, 2)
                    slider4 = float(float(slider4str) * .01)
                    slider4 = round(slider4, 2)
                else:
                    pass

                # sleep for .02 seconds because arduino is outputting every 10 milliseconds
                sleep(.005)

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
                else:
                    pass
                
                print(slider1, slider2, slider3, slider4)
                       
                


        #else:
           #print("The Serial port is no longer connected")
           #break

connectSerial()
sleep(.002)
getValues()
