# this file is mainly responsible for creating the Graphical user inerface of the software using pyqt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import os, icecream
# custom import
import Constants
from ImageModifierEngine import ImageModifier

class DummyPreview(QWidget):
    def __init__(self, factor : int = 2) -> None:
        super().__init__()
        self.masterLayout = QVBoxLayout(self)
        self.setFixedSize(Constants.DUMMY_WINDOW_WIDTH, Constants.DUMMY_WINDOW_HEIGHT)
        self.factor = factor
        self._initializeUI() # initialises all the UI material
        self._constuctUI() # apply ui material in window
        self._addAttributes() # addning all Widgets
        self.resizeGivenWallpaper("./static/arora1.jpg") # relative path is given instead of real path
        self._loadStyleSheet() # Applying Style in The UI
        return
    
    def _initializeUI(self) -> None:
        '''this function must be called inside the  constructor so that when the class is called all the uI components get's loaded in the window'''
        self._buildFrames()
        self._buildLayouts()
        self._buildButtons()
        self._buildLineInput()
        return

    def _buildFrames(self) -> None:
        '''This method must be called inside initializeUI method to load all the frames using in the UI, no relevent extternal use'''
        # main Frame that holds master Layout
        self.masterLayoutInnerFrame = QFrame()
        self.masterLayoutInnerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterLayoutInnerFrame.setObjectName("master_inner_layout_frame")
        self.masterLayoutInnerFrame.setStyleSheet("""
            #master_inner_layout_frame{
                background-repeat: repeat;
                background-position: center;
            }
        """)
        
        # Search Zone
        self.searchSectionLayoutFrame = QFrame()
        self.searchSectionLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # Control Button Area
        self.controlSectionLayoutFrame = QFrame()
        self.controlSectionLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # Table Widget Area
        self.viewPanelLayoutFrame = QFrame()
        self.viewPanelLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        return

    def _buildLayouts(self) -> None:
        '''Must be called inside _initializeUI method. it is used to build the Layouts'''

        # main Layout 
        self.bodyLayout = QVBoxLayout()
        
        # search Zone
        self.searchSectionLayout = QHBoxLayout() # Holder
        self.searchSectionInnerLayout =  QVBoxLayout()
        self.searchFieldLayout = QHBoxLayout()  # Search Bar
        self.searchRelatedButtonLayout = QHBoxLayout() # Buttons
        
        self.actionLayout = QHBoxLayout() # Control Section + View Section

        # control Section
        self.controlSectionLayout = QVBoxLayout()
        self.controlSectionInnerLayout = QVBoxLayout()

        # view Section
        self.viewPanelLayout = QHBoxLayout()
        self.viewPanelInnerLayout = QHBoxLayout()
        self.tableHolderLayout = QHBoxLayout()
        return
    
    def _buildButtons(self) -> None:
        # search Related
        self.searchButton = QPushButton()

        self.searchBySingerButton = QPushButton()

        # Control Related
        self.BackGroundbutton = QPushButton()
        
        self.setDownloadDirectory = QPushButton()
        
        self.HighQualityEnableButton = QPushButton()
        
        self.lowQualityEnableButton = QPushButton()
        
        self.showDownloadingHistory = QPushButton()
        
        self.deleteDownlaodingHistory = QPushButton()

        self.deleteButton = QPushButton()
        return
    
    def _buildLineInput(self) -> None:
        self.inputField = QLineEdit()
        self.inputField.setDisabled(True) # for preview purpose no need to take input
        return

    def _constuctUI(self) -> None:
        '''This method must be run after the _buildFrames method inside the constructor to form the GUI using the components'''
        #MAIN WINDOW
        self.masterLayout.addWidget(self.masterLayoutInnerFrame, Qt.AlignmentFlag.AlignCenter)
        self.masterLayoutInnerFrame.setLayout(self.bodyLayout)
        
        #INPUT SECTION
        self.bodyLayout.addLayout(self.searchSectionLayout, 10)
        self.searchSectionLayout.addWidget(self.searchSectionLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.searchSectionLayoutFrame.setLayout(self.searchSectionInnerLayout)
        self.searchSectionInnerLayout.addLayout(self.searchFieldLayout, 50)
        self.searchSectionInnerLayout.addLayout(self.searchRelatedButtonLayout, 50)

        #ACTION SECTION
        self.bodyLayout.addLayout(self.actionLayout, 90)

        #CONTROL PANEL
        self.actionLayout.addLayout(self.controlSectionLayout, 20)
        self.controlSectionLayout.addWidget(self.controlSectionLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.controlSectionLayoutFrame.setLayout(self.controlSectionInnerLayout)

        #VIEW PANEL
        self.actionLayout.addLayout(self.viewPanelLayout, 80)
        self.viewPanelLayout.addWidget(self.viewPanelLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.viewPanelLayoutFrame.setLayout(self.viewPanelInnerLayout)
        return
    
    def _addAttributes(self):
        '''Packs all the widgets in their holder layouts'''
        # search Section
        self.searchFieldLayout.addWidget(self.inputField, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchBySingerButton, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchButton, Qt.AlignmentFlag.AlignCenter)

        # Control Section
        self.controlSectionInnerLayout.addWidget(self.BackGroundbutton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.HighQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.lowQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.setDownloadDirectory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.showDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteDownlaodingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteButton, alignment = Qt.AlignmentFlag.AlignTop)
        return
    
    # INTERFACING
    def resizeGivenWallpaper(self, loc : str = None) -> None:
        '''For the back ground of the application this method resizes the currently selected image from the static path and saves it. If any error occurred then sends a signal to the application'''
        if(loc):
            self._clearTempDirectory()
            loc = loc.replace("\\", "/")
            fileName = loc.split("/")[-1]
            savingPath = os.path.join(os.getcwd() + Constants.TEMP_PATH + fileName)
            ImageModifier.resizeImage(loc, Constants.DUMMY_WINDOW_WIDTH, Constants.DUMMY_WINDOW_HEIGHT, savingPath)
            if(os.path.exists(savingPath)):
                self.masterLayoutInnerFrame.setStyleSheet(
                    "#master_inner_layout_frame{background-image: url(./temp/" + fileName + ");}"
                )
        return
    
    def _clearTempDirectory(self) -> None:
        '''After Completing wallpaper Changing operation use this method to keep Temp folder Clean.'''
        for tempFile in os.listdir("./temp"):
            os.remove(os.path.join("./temp", tempFile))
        return
    
    def _loadStyleSheet(self) -> None:
        '''Should be called in the constructor and it loads the style sheet from qml file'''
        try:
            file = QFile(Constants.DUMMY_FILE_STYLE_PATH) # Creating File Objects
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY) # extracting Style
                self.setStyleSheet(qss) # adding Style
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error
        return
    pass

if __name__ == '__main__':
    app = QApplication([])
    window = DummyPreview()
    window.show()
    app.exec_()