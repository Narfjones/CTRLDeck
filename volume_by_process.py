from ctypes import POINTER
from pycaw.pycaw import AudioUtilities

sessionsList = []
chosenPort = str()

def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() != None:
            sessionsList.append(session.Process.name())
    return(sessionsList)

if __name__ == "__main__":
    main()