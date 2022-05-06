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
    topLabel_label = QLabel("Choose your port:")
    topLabel_comboBox = QComboBox()
    for i in CTRLDeck.portOptions:
        topLabel_comboBox.addItem(i)
    global port
    port = str(topLabel_comboBox.currentText())
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
    connect_button.clicked.connect(CTRLDeck.savePortChoice(port))
    # connect_button.clicked.connect()
    print(port)
    print(type(port))
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
    leftMenu.addTab(mainTab, "Setup")
    leftMenu.addTab(sliderTab, "Sliders")
    leftMenu.addTab(macroTab, "Macro Keys")
    mainTab.setLayout(MainMenuUI())
    sliderTab.setLayout(SliderMenuUI())
    macroTab.setLayout(MacroKeysMenuUI())
    return leftMenu

    
def MainMenuUI():
    setupPage = QStackedLayout()

    mainMenu1 = QWidget()
    mainMenu1_layout = QHBoxLayout()
    assignSlidersButton = QPushButton("Assign Sliders")
    assignSlidersButton.setObjectName('assignSliderButton')
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
    setupPage.addWidget(mainMenu2)
    return setupPage

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