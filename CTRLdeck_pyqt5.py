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
    QListWidget,
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
lineList = CTRLDeck.lineList
sliderNum = []
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
    # Create widget and and insert a grid layout
    assignSlider_widget = QWidget()
    assignSlider_layout = QGridLayout()
    assignSlider_layout.cellRect(6, 2)
    
    # Create labels and assign them an object name to style
    slider1_label = QLabel("Slider 1")
    slider1_label.setObjectName('sliderlabel')
    slider2_label = QLabel("Slider 2")
    slider1_label.setObjectName('sliderlabel')
    slider3_label = QLabel("Slider 3")
    slider3_label.setObjectName('sliderlabel')
    slider4_label = QLabel("Slider 4")
    slider4_label.setObjectName('sliderlabel')
    
    slider_labels = []
    slider_widgets = []
    slider_choiceLayouts = []
    slider_listBoxes = []
    slider_comboBoxes = []
    slider_addButtons = []

    for i in CTRLDeck.sliders:
        label = QLabel("Slider" + str(i))
        widget = QWidget()
        choiceLayout = QHBoxLayout()
        listBox = QListWidget()
        comboBox = QComboBox()
        for j in CTRLDeck.sessionOptions:
            comboBox.addItem(j)
        addButton = QPushButton("add")
        slider_labels.append(label)
        slider_widgets.append(widget)
        slider_choiceLayouts.append(choiceLayout)
        slider_listBoxes.append(listBox)
        slider_comboBoxes.append(comboBox)
        slider_addButtons.append(addButton)
    
    widgetsNum = len(slider_choiceLayouts)
    
    for i in range(widgetsNum):
        slider_addButtons[i].clicked.connect(lambda: print(CTRLDeck.sliders.index(i)) and slider_listBoxes[i].addItem(slider_comboBoxes[i].currentText()))
    
    for i in range(widgetsNum):
        slider_choiceLayouts[i].addWidget(slider_comboBoxes[i])
        slider_choiceLayouts[i].addWidget(slider_addButtons[i])
    
    for i in range(widgetsNum):
        slider_widgets[i].setLayout(slider_choiceLayouts[i])
    
    for i in range(widgetsNum):
        assignSlider_layout.addWidget(slider_labels[i])
        assignSlider_layout.addWidget(slider_widgets[i])
        assignSlider_layout.addWidget(slider_listBoxes[i])
    
    assignSlider_widget.setLayout(assignSlider_layout)

    # These are container widgets to hold the combobox and 'add' button layout
    slider1_widget = QWidget()
    slider2_widget = QWidget()
    slider3_widget = QWidget()
    slider4_widget = QWidget()
    
    # These are the layouts to put the combobox and add button widgets
    slider1_choiceLayout = QHBoxLayout()
    slider2_choiceLayout = QHBoxLayout()
    slider3_choiceLayout = QHBoxLayout()
    slider4_choiceLayout = QHBoxLayout()
    
    # Create combobox elements to hold the process list
    global slider1_comboBox
    global slider2_comboBox
    global slider3_comboBox
    global slider4_comboBox
    slider1_comboBox = QComboBox()
    slider2_comboBox = QComboBox()
    slider3_comboBox = QComboBox()
    slider4_comboBox = QComboBox()

    # Add all items from SessionOptions to our combo boxes
    for i in CTRLDeck.sessionOptions:
        slider1_comboBox.addItem(i)
    slider1_comboBox.addAction
    for i in CTRLDeck.sessionOptions:
        slider2_comboBox.addItem(i)
    for i in CTRLDeck.sessionOptions:
        slider3_comboBox.addItem(i)
    for i in CTRLDeck.sessionOptions:
        slider4_comboBox.addItem(i)
        
    # Create buttons to add the process to sliders
    slider1_addButton = QPushButton("add")
    slider1_addButton.clicked.connect(lambda: saveSlidertoFile(1) and slider1_listBox.addItem(slider1_comboBox.currentText()))
    slider2_addButton = QPushButton("add")
    slider2_addButton.clicked.connect(lambda: saveSlidertoFile(2) and slider2_listBox.addItem(slider2_comboBox.currentText()))
    slider3_addButton = QPushButton("add")
    slider3_addButton.clicked.connect(lambda: saveSlidertoFile(3) and slider3_listBox.addItem(slider3_comboBox.currentText()))
    slider4_addButton = QPushButton("add")
    slider4_addButton.clicked.connect(lambda: saveSlidertoFile(4) and slider4_listBox.addItem(slider4_comboBox.currentText()))
    
    # Create listboxes to hold the assigned processes
    global slider1_listBox
    global slider2_listBox
    global slider3_listBox
    global slider4_listBox
    slider1_listBox = QListWidget()
    slider2_listBox = QListWidget()
    slider3_listBox = QListWidget()
    slider4_listBox = QListWidget()
    
    # Create single slider assignment box to insert into the grid
 #   slider1_choiceLayout.addWidget(slider1_comboBox)
 #   slider1_choiceLayout.addWidget(slider1_addButton)
 #   slider1_widget.setLayout(slider1_choiceLayout)
 #   assignSlider_layout.addWidget(slider1_label, 1, 1)
 #   assignSlider_layout.addWidget(slider1_widget, 2, 1)
 #   assignSlider_layout.addWidget(slider1_listBox, 3, 1)
    
    # Create single slider assignment box to insert into the grid
 #   slider2_choiceLayout.addWidget(slider2_comboBox)
 #   slider2_choiceLayout.addWidget(slider2_addButton)
 #   slider2_widget.setLayout(slider2_choiceLayout)
 #   assignSlider_layout.addWidget(slider2_label, 1, 2)
 #   assignSlider_layout.addWidget(slider2_widget, 2, 2)
 #   assignSlider_layout.addWidget(slider2_listBox, 3, 2)
    
    # Create single slider assignment box to insert into the grid
 #   slider3_choiceLayout.addWidget(slider3_comboBox)
 #   slider3_choiceLayout.addWidget(slider3_addButton)
 #   slider3_widget.setLayout(slider3_choiceLayout)
 #   assignSlider_layout.addWidget(slider4_label, 4, 1)
 #   assignSlider_layout.addWidget(slider3_widget, 5, 1)
 #   assignSlider_layout.addWidget(slider3_listBox, 6, 1)
    
    # Create single slider assignment box to insert into the grid
 #   slider4_choiceLayout.addWidget(slider4_comboBox)
 #   slider4_choiceLayout.addWidget(slider4_addButton)
 #   slider4_widget.setLayout(slider4_choiceLayout)
 #   assignSlider_layout.addWidget(slider4_label, 4, 2)
 #   assignSlider_layout.addWidget(slider4_widget, 5, 2)
 #   assignSlider_layout.addWidget(slider4_listBox, 6, 2)

    # Insert all widgets into layout for 'Assign Sliders' main Menu
 #   assignSlider_widget.setLayout(assignSlider_layout)

    return assignSlider_widget

def saveSlidertoFile(sliderNum):
    global lineList
    sliderStr = ''
    if sliderNum == 1:
        slider1_listBox.addItem(slider1_comboBox.currentText())
        for i in range(slider1_listBox.count()):
            sliderStr += (str(slider1_listBox.item(i).text()) + ",")
    elif sliderNum == 2:
        slider2_listBox.addItem(slider1_comboBox.currentText())
        for i in slider2_listBox.count():
            sliderStr += (str(slider2_listBox.item(i).text()) + ",")
    elif sliderNum == 3:
        slider3_listBox.addItem(slider1_comboBox.currentText())
        for i in slider1_listBox.count():
            sliderStr += (str(slider3_listBox.item(i).text()) + ",")
    elif sliderNum == 4:
        slider4_listBox.addItem(slider1_comboBox.currentText())
        for i in slider1_listBox.count():
            sliderStr += (str(slider4_listBox.item(i).text()) + ",")
            

    lineList[sliderNum] = "\n" + sliderStr

    try:
        portFile = open("COMport", "w")
        portFile.writelines(lineList)
        portFile.close()
        # CTRLDeck.serialValuetoVolume.init()
    except:
        print("process was not added to slider")


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