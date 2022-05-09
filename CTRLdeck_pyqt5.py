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
    QStackedLayout,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QLabel,
)
from serial.serialutil import PortNotOpenError
import CTRLDeck 

sliders = CTRLDeck.sliders
macroKeys = []
sessionOptions = CTRLDeck.sessionOptions
labels = CTRLDeck.labels
global port

class MainWindow(QMainWindow):
        
        def __init__ (self):
            super(MainWindow, self).__init__()


            central_widget = QWidget() # Create central widget container to be displayed in window
            layout = QVBoxLayout() # Embed a box layout in the central widget container
            central_widget.setLayout(layout) 
            self.setCentralWidget(central_widget)

            self.setWindowTitle("CTRLdeck")
            self.setGeometry(500,250,1023,707)

            topMenu = TopMenu() # Create the Top Menu which contains the title bar and COMport connecter
            leftMenu = LeftMenu() # Attach tabbed menu for switching between main functions
            connectButton = ConnectButton() # Attach big connect button that's always visible
            layout.addLayout(topMenu)
            layout.addWidget(leftMenu)
            layout.addWidget(connectButton)

            

def TopMenu():

    # Create three widgets and embed them in a layout to be displayed at the top of the window
    container = QHBoxLayout()
    topLabel_logo = QLabel()
    topLabel_space = QLabel()
    topImg = QPixmap('ctrldeck-title.png')
    topLabel_logo.setPixmap(topImg)

    # Create port choice label and combobox for available 
    topLabel_label = QLabel("Choose your port:")
    global topLabel_comboBox
    topLabel_comboBox = QComboBox()
    for i in CTRLDeck.portOptions:
        topLabel_comboBox.addItem(i)
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
    CTRLDeck.lineList[0] = str(topLabel_comboBox.currentText())
    connect_button.clicked.connect(lambda: SavePort())
    # connect_button.clicked.connect()
    button_label = QLabel()
    button_layout.addWidget(connect_button)
    button_layout.addWidget(button_label)
    button_layout.addWidget(button_label)
    button_widget.setLayout(button_layout)
    return button_widget

def SavePort():
    CTRLDeck.lineList[0] = str(topLabel_comboBox.currentText())
    CTRLDeck.savePortChoice()

def LeftMenu():
    leftMenu = QTabWidget()
    leftMenu.setTabPosition(QTabWidget.West)
    leftMenu.setMovable(False)
    mainTab = QWidget()
    sliderTab = QWidget()
    macroTab = QWidget()
    leftMenu.addTab(mainTab, "Setup")
    leftMenu.addTab(sliderTab, "Sliders")
    leftMenu.addTab(macroTab, "Macro Keys")
    mainTab.setLayout(MainMenuUI())
    sliderTab.setLayout(SliderMenuUI())
    macroTab.setLayout(MacroKeysMenuUI())
    return leftMenu

    
def MainMenuUI():
    global setupPage
    setupPage = QStackedLayout()

    mainMenu1 = QWidget()
    mainMenu1_layout = QHBoxLayout()
    assignSlidersButton = QPushButton("Assign Sliders")
    assignSlidersButton.setObjectName('assignSliderButton')
    assignSlidersButton.pressed.connect(lambda: setupPage.setCurrentIndex(1))
    assignMacrosButton = QPushButton("Assign Macros")
    assignMacrosButton.setObjectName('assignMacrosButton')
    space = QWidget()
    mainMenu1_layout.addWidget(assignSlidersButton)
    mainMenu1_layout.addWidget(assignMacrosButton)
    mainMenu1.setLayout(mainMenu1_layout)
    mainMenu1_layout.addWidget(assignSlidersButton)
    mainMenu1_layout.addWidget(assignMacrosButton)
    mainMenu1.setLayout(mainMenu1_layout)

    mainMenu2 = QWidget()
    mainMenu2_layout = QVBoxLayout()
    for i in sliders:
        i = QLabel()
        mainMenu2_layout.addWidget(i)
    mainMenu2.setLayout(mainMenu2_layout)

#    process = QComboBox()
#    for i in sessionOptions:
#        process.addItem(i)

    setupPage.addWidget(mainMenu1)
    setupPage.addWidget(SliderAssign())

    setupPage.setCurrentIndex(0)

    return setupPage

def SliderAssign():
    assignSlider_widget = QWidget()
    assignSlider_layout = QGridLayout()
    slider1_label = QLabel("Slider 1")
    slider1_label.setObjectName('sliderlabel')
    slider2_label = QLabel("Slider 2")
    slider1_label.setObjectName('sliderlabel')
    slider3_label = QLabel("Slider 3")
    slider1_label.setObjectName('sliderlabel')
    slider4_label = QLabel("Slider 4")
    slider1_label.setObjectName('sliderlabel')
    slider1_comboBox = QComboBox()
    slider2_comboBox = QComboBox()
    slider3_comboBox = QComboBox()
    slider4_comboBox = QComboBox()

    for i in CTRLDeck.sessionOptions:
        slider1_comboBox.addItem(i)
    for i in CTRLDeck.sessionOptions:
        slider2_comboBox.addItem(i)
    for i in CTRLDeck.sessionOptions:
        slider3_comboBox.addItem(i)
    for i in CTRLDeck.sessionOptions:
        slider4_comboBox.addItem(i)

    assignSlider_layout.addWidget(slider1_label, 1, 1)
    assignSlider_layout.addWidget(slider1_comboBox, 2, 1)
    assignSlider_layout.addWidget(slider2_label, 1, 2)
    assignSlider_layout.addWidget(slider2_comboBox, 2, 2)
    assignSlider_layout.addWidget(slider3_label, 3, 1)
    assignSlider_layout.addWidget(slider3_comboBox, 4, 1)
    assignSlider_layout.addWidget(slider4_label, 3, 2)
    assignSlider_layout.addWidget(slider4_comboBox, 4, 2)

    assignSlider_widget.setLayout(assignSlider_layout)

    return assignSlider_widget


def SliderMenuUI():
    layout = QGridLayout()
    for x in sliders:
        fader = QSlider(Qt.Vertical)
        fader.setTickPosition(QSlider.TicksLeft)
        fader.setMinimum(0)
        fader.setMaximum(100)
        fader.setTickInterval(1)
        layout.addWidget(fader, 2, sliders.index(x))
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