import serial
from time import sleep
import strstr
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

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
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == sliderProcess1:
                volume.SetMasterVolume(volume1, None)
                

def volumeSlider2(volume2):
    if sliderProcess1 != None:
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
                print(slider1, slider2)

                if slider1 != slider1previous or slider2 != slider2previous:
                    slider1previous = slider1
                    slider2previous = slider2
                    volumeSlider1(slider1)
                    volumeSlider2(slider2)
                else:
                    pass


                # print(slider1, slider2)            
                


        else:
           print("The Serial port is no longer connected")
           break

connectSerial()
sleep(.01)
getValues()
