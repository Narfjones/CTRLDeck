from random import triangular
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QLabel
)

from PyQt5.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
        
        def __init__ (self):
            super(MainWindow, self).__init__()

            self.setWindowTitle("CTRLdeck")
            self.setGeometry(500,250,1023,707)

            mainWidget = leftMenu()
            self.setCentralWidget(mainWidget)

def leftMenu():
    leftMenu = QTabWidget()
    leftMenu.setTabPosition(QTabWidget.West)
    leftMenu.setMovable(False)
    leftMenu.addTab(MainMenu(), "Main Menu")
    leftMenu.addTab(SliderMenu(), "Sliders")
    leftMenu.addTab(MacroKeysMenu(), "Macro Keys")
    return leftMenu

    
def MainMenu():
    mainMenu = QWidget()
    return mainMenu

def SliderMenu():
    sliderMenu = QWidget()
    return sliderMenu

def MacroKeysMenu():
    macroKeysMenu = QWidget()
    return macroKeysMenu

    
app = QApplication(sys.argv)

window = MainWindow()

with open("./inc/style.css", "r") as file:
    app.setStyleSheet(file.read())

window.show()

app.exec()