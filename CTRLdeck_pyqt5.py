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
    QTabWidget
)
from PyQt5.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
        
        def __init__ (self):
            super(MainWindow, self).__init__()

            self.setWindowTitle("CTRLdeck")
            self.setGeometry(500,250,1023,707)
            
            mainLayout = QVBoxLayout()

            mainWidget = leftMenu()
            mainWidget.setLayout(mainLayout)
            self.setCentralWidget(mainWidget)

def leftMenu():
    leftMenu = QTabWidget()
    leftMenu.setTabPosition(QTabWidget.West)
    leftMenu.setMovable(True)
    for n, menu in enumerate(["Main Menu", "Sliders", "Macro Keys"]):
            leftMenu.addTab(Color(menu), menu)
    return leftMenu

def MainMenu():
    # add main menu stuff here like profile, serial connection, etc...
    pass

def SliderMenu():
    # add slider animations and code for assignments here
    pass

def MacroKeysMenu():
    # Add code here to assign the macro keys to functions. Keyboard Macros, Open Programs, Scripting, etc...
    pass


    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()