from pycaw.pycaw import AudioUtilities


def main():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        print(session.Process)
        print(type(session.Process))


if __name__ == "__main__":
    main()