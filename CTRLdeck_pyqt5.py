from random import triangular
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QLineEdit,
    QHBoxLayout,
    QSlider,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QLabel
)

from PyQt5.QtGui import QPalette, QColor

sliders = [1, 2, 3, 4]
macroKeys = []
sessionOptions = ["master", "chrome.exe", "firefox.exe", "discord.exe", "microphone", "unmapped", "Choose a file:" ]

class MainWindow(QMainWindow):
        
        def __init__ (self):
            super(MainWindow, self).__init__()

            central_widget = QWidget()
            layout = QVBoxLayout()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            self.setWindowTitle("CTRLdeck")
            self.setGeometry(500,250,1023,707)

            topMenu = TopMenu()
            leftMenu = LeftMenu()
            connectButton = ConnectButton()
            layout.addLayout(topMenu)
            layout.addWidget(leftMenu)
            layout.addWidget(connectButton)

            

def TopMenu():
    container = QHBoxLayout()
    topLabel_logo = QLabel()
    topLabel_space = QLabel()
    topImg = QPixmap('ctrldeck-title.png')
    topLabel_logo.setPixmap(topImg)
    topLabel_label = QLabel("Choose your port:")
    topLabel_comboBox = QComboBox()
    topLabel_comboBox.addItem("COM1")
    topLabel_comboBox.addItem("COM2")
    container.addWidget(topLabel_logo)
    container.addWidget(topLabel_space)
    container.addWidget(topLabel_label)
    container.addWidget(topLabel_comboBox)
    container.addStretch(1)
    return container

def ConnectButton():
    button_widget = QWidget()
    button_layout = QHBoxLayout()
    connect_button = QPushButton()
    connect_button.setText("Connect")
    connect_button.setObjectName("connect_button")
    button_label = QLabel()
    button_layout.addWidget(connect_button)
    button_layout.addWidget(button_label)
    button_layout.addWidget(button_label)
    button_widget.setLayout(button_layout)
    return button_widget

def LeftMenu():
    leftMenu = QTabWidget()
    leftMenu.setTabPosition(QTabWidget.West)
    leftMenu.setMovable(False)
    mainTab = QWidget()
    sliderTab = QWidget()
    macroTab = QWidget()
    leftMenu.addTab(mainTab, "Main Menu")
    leftMenu.addTab(sliderTab, "Sliders")
    leftMenu.addTab(macroTab, "Macro Keys")
    mainTab.setLayout(MainMenuUI())
    sliderTab.setLayout(SliderMenuUI())
    macroTab.setLayout(MacroKeysMenuUI())
    return leftMenu

    
def MainMenuUI():
    mainMenu = QHBoxLayout()
    process = QComboBox()
    for i in sessionOptions:
        process.addItem(i)
    mainMenu.addWidget(process)
    return mainMenu

def SliderMenuUI():
    layout = QGridLayout()
    for x in sliders:
        fader = QSlider(Qt.Vertical)
        fader.setTickPosition(QSlider.TicksLeft)
        fader.setMinimum(0)
        fader.setMaximum(100)
        fader.setTickInterval(1)
        layout.addWidget(fader, 2, x)
    return layout

def MacroKeysMenuUI():
    macroKeysMenu = QGridLayout()
    return macroKeysMenu

    
app = QApplication(sys.argv)

window = MainWindow()

with open("style.css", "r") as file:
    app.setStyleSheet(file.read())

window.show()

app.exec()