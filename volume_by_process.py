from ctypes import POINTER
from pycaw.pycaw import AudioUtilities

sessionsList = []

def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        print(session.Process)
        sessionsList.append(session.Process.name())
        print(sessionsList)
        
if __name__ == "__main__":
    main()