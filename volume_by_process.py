from __future__ import print_function

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Create list and string variables to store and transport processes
sessionsList = []
chosenPort = str()

#-------------------------------------------------------------------------------------------------
#       Gets active audio processes. I don't think we need to do this as we can just create a
#       list of common processes and an option for the user to add custom process to the list.
#       Ideally and 'add your own' would pop a file finder window.
#-------------------------------------------------------------------------------------------------
def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() != None:
            sessionsList.append(session.Process.name())
    
    # 'master' uses EndpointVolume while processes are done with SimpleAudioVolume
    sessionsList.append("master")
    
    # return the list to CTRLDeck_Python.py
    return(sessionsList)

if __name__ == "__main__":
    main()