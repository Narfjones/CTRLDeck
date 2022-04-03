from pynput import keyboard
import win32com.client as comclt
wsh= comclt.Dispatch("WScript.Shell")

keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
keysDict = {}

def init_macros():
    global keysDict
    portFile = open("macroKeys.dat", "r")
    lineList = portFile.readlines()
    for i in range(len(keys)):
        keysDict[keys[i]] = lineList[i]
    portFile.close()

current = set()

def function_1():
        print('Executed function_1')

def function_2():
    
    print('Executed function_2')

def function_3():
    print('Executed function_3')

def function_4():
    print('Executed function_4')

def function_5():
    print('Executed function_5')

def function_6():
    print('Executed function_6')

def function_7():
    print('Executed function_7')

def function_8():
    print('Executed function_8')

def function_9():
    print('Executed function_9')

def function_10():
    print('Executed function_10')

def function_11():
    print('Executed function_11')

def function_12():
    print('Executed function_12')

with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+<alt>+<f13>': function_1,
        '<ctrl>+<shift>+<alt>+<f14>': function_2,
        '<ctrl>+<shift>+<alt>+<f15>': function_3,
        '<ctrl>+<shift>+<alt>+<f16>': function_4,
        '<ctrl>+<shift>+<alt>+<f17>': function_5,
        '<ctrl>+<shift>+<alt>+<f18>': function_6,
        '<ctrl>+<shift>+<alt>+<f19>': function_7,
        '<ctrl>+<shift>+<alt>+<f20>': function_8,
        '<ctrl>+<shift>+<alt>+<f21>': function_9,
        '<ctrl>+<shift>+<alt>+<f22>': function_10,
        '<ctrl>+<shift>+<alt>+<f23>': function_11,
        '<ctrl>+<shift>+<alt>+<f24>': function_12,}) as h:
    h.join()

