from ctypes import POINTER
from pycaw.pycaw import AudioUtilities

sessionsList = []

def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        sessionsList.append(session.Process.name())
    return(sessionsList)
    

if __name__ == "__main__":
    main()