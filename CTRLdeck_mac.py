import profile
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from inc.getCOM import serial_ports
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import inc.serialValuetoVolume as serialValuetoVolume
import threading
import logging
from time import sleep
from numpy import interp
from getCOMmac import findDeck