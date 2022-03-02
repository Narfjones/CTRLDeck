from __future__ import print_function

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

sessionsList = []
chosenPort = str()

def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() != None:
            sessionsList.append(session.Process.name())
            sessionsList.append("master")
    return(sessionsList)

if __name__ == "__main__":
    main()