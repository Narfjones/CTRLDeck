import sys
from types import NoneType
from PyQt5.QtCore import Qt, QSignalMapper
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
    QLabel
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
            btnMapper = QSignalMapper

            self.setWindowTitle("CTRLdeck")
            self.setGeometry(500,250,1023,707)

            topMenu = self.TopMenu() # Create the Top Menu which contains the title bar and COMport connecter
            leftMenu = self.LeftMenu() # Attach tabbed menu for switching between main functions
            connectButton = self.ConnectButton() # Attach big connect button that's always visible
            layout.addLayout(topMenu)
            layout.addWidget(leftMenu)
            layout.addWidget(connectButton)

        def TopMenu(self):

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


        def ConnectButton(self):
            button_widget = QWidget()
            button_layout = QHBoxLayout()
            connect_button = QPushButton()
            connect_button.setText("Connect")
            connect_button.setObjectName("connect_button")
            lineList[0] = str(topLabel_comboBox.currentText())
            connect_button.clicked.connect(lambda: MainWindow.SavePort())
            # connect_button.clicked.connect()
            button_label = QLabel()
            button_layout.addWidget(connect_button)
            button_layout.addWidget(button_label)
            button_layout.addWidget(button_label)
            button_widget.setLayout(button_layout)
            return button_widget

        def SavePort():
            lineList[0] = str(topLabel_comboBox.currentText())

            for val in range(len(slider_listBoxes)):
                # lineList[i+1] = "\n" + slider_listBoxes[i+1].currentText()
                value = next( v for i, v in enumerate(slider_listBoxes.values()) if i == val )
                lineList[val+1] = "\n"
                for j in range(value.count()):
                    lineList[val+1] += str(value.item(j).text()) + ","
                    print(lineList)
                
            MainWindow.saveSlidertoFile()
            CTRLDeck.start_clicked()
            

            

        def LeftMenu(self):
            leftMenu = QTabWidget()
            leftMenu.setTabPosition(QTabWidget.West)
            leftMenu.setMovable(False)
            mainTab = QWidget()
            sliderTab = QWidget()
            macroTab = QWidget()
            leftMenu.addTab(mainTab, "Setup")
            leftMenu.addTab(sliderTab, "Sliders")
            leftMenu.addTab(macroTab, "Macro Keys")
            mainTab.setLayout(MainWindow.MainMenuUI())
            sliderTab.setLayout(MainWindow.SliderMenuUI())
            macroTab.setLayout(MainWindow.MacroKeysMenuUI())
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
            setupPage.addWidget(MainWindow.SliderAssign())

            setupPage.setCurrentIndex(0)

            return setupPage


        def SliderAssign():
            # Create widget and and insert a grid layout
            assignSlider_widget = QWidget()
            assignSlider_layout = QGridLayout()
            assignSlider_layout.cellRect(4, 2)
            
            slider_labels = []
            slider_widgets = []
            slider_choiceLayouts = []
            global slider_listBoxes
            slider_listBoxes = {}
            slider_comboBoxes = {}
            slider_addButtons = {}

            sum = 1 # Enumerator for adding dictionary keys

            for i in CTRLDeck.sliders:
                label = QLabel("Slider" + str(i))
                widget = QWidget()
                choiceLayout = QHBoxLayout()
                listBox = QListWidget()
                comboBox = QComboBox()
                for j in CTRLDeck.sessionOptions:
                    comboBox.addItem(j)
                addButton = QPushButton("add")
                addButton.setObjectName('%d' % sum)
                slider_labels.append(label)
                slider_widgets.append(widget)
                slider_choiceLayouts.append(choiceLayout)
                slider_listBoxes["listBox{0}".format(sum)] = listBox
                slider_comboBoxes["comboBox{0}".format(sum)] = comboBox
                slider_addButtons["button{0}".format(sum)] = addButton
                slider_addButtons["button{0}".format(sum)].released.connect(lambda i=sum: slider_listBoxes["listBox{0}".format(i)].addItem(slider_comboBoxes["comboBox{0}".format(i)].currentText()))

                if sum < 4:
                    sum = sum + 1
                else:
                    sum = 4

            widgetsNum = len(slider_choiceLayouts)

            for i in range(widgetsNum):
                slider_choiceLayouts[i].addWidget(slider_comboBoxes["comboBox{0}".format(i+1)])
                slider_choiceLayouts[i].addWidget(slider_addButtons["button{0}".format(i+1)])
            
            for i in range(widgetsNum):
                slider_widgets[i].setLayout(slider_choiceLayouts[i])
            
            global row
            global col
            row = 1
            col = 1

            for i in range(widgetsNum):
                assignSlider_layout.addWidget(slider_labels[i], row, col)
                row = row + 1
                assignSlider_layout.addWidget(slider_widgets[i], row, col)
                row = row + 1
                assignSlider_layout.addWidget(slider_listBoxes["listBox{0}".format(i+1)], row, col)
                if  row == 3 and col == 2:
                    row = 4
                    col = 1
                elif row == 6 and col == 1:
                    row = 4
                    col = col + 1
                else:
                    row = 1
                    col = col + 1

            assignSlider_widget.setLayout(assignSlider_layout)

            return assignSlider_widget


        def saveSlidertoFile():
            
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