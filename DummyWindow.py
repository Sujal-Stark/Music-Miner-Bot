# this file is mainly responsible for creating the Graphical user interface of the software using pyqt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QFile, QIODevice
import os

# custom import
import Constants
from ImageModifierEngine import ImageModifier

class DummyPreview(QWidget):
    def __init__(self, factor : int = 2) -> None:
        super().__init__()
        self.masterDummyLayout = QVBoxLayout(self)
        self.setFixedSize(Constants.DUMMY_WINDOW_WIDTH, Constants.DUMMY_WINDOW_HEIGHT)
        self.factor = factor
        self._initializeUI() # initialises all the UI material
        self._constructUI() # apply ui material in window
        self._addAttributes() # adding all Widgets
        self._createMainClassAttributes() # create all attributes that hold Main class Attribute values
        self._initializeHelperClasses()
        self._loadStyleSheet() # Applying Style in The UI
        return

    def _initializeHelperClasses(self) -> None:
        """
            Any class that are needed to run for this class is initialized here except rarely used one
        """
        self.imageModifierEngine = ImageModifier() # handles image related modifications
        return

    def _createMainClassAttributes(self) -> None:
        """
            Inside This method Some Class Variables are declared which use to accept values from main GUI so that this
            dummy window can be initialized.
            This Method should be called inside init to initialize with None values or any initial values
        """
        self.currentWallpaperLocation : str = Constants.DEFAULT_WALLPAPER_LOCATION
        return

    def getTestingWallpaperLocation(self, location : str) -> None:
        """
            Accepts applications current wallpaper location
            :param location: Holds the address of wallpaper
            :return: None
        """
        self.currentWallpaperLocation = location
        return

    def _initializeUI(self) -> None:
        """
            this function must be called inside the  constructor so that when the class is called all the uI components
            gets loaded in the window
         """
        self._buildFrames()
        self._buildLayouts()
        self._buildButtons()
        self._buildLineInput()
        return

    def _buildFrames(self) -> None:
        """
            This method must be called inside initializeUI method to load all the frames using in the UI, no relevant
            external use
        """
        # main Frame that holds master Layout
        self.masterDummyLayoutInnerFrame = QFrame()
        self.masterDummyLayoutInnerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterDummyLayoutInnerFrame.setObjectName("master_inner_layout_frame")
        self.masterDummyLayoutInnerFrame.setStyleSheet("""
            #master_inner_layout_frame{
                background-repeat: repeat;
                background-position: center;
            }
        """)
        
        # Search Zone
        self.searchSectionDummyLayoutFrame = QFrame()
        self.searchSectionDummyLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # Control Button Area
        self.controlSectionDummyLayoutFrame = QFrame()
        self.controlSectionDummyLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # Table Widget Area
        self.viewPanelDummyLayoutFrame = QFrame()
        self.viewPanelDummyLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        return

    def _buildLayouts(self) -> None:
        """Must be called inside _initializeUI method. it is used to build the Layouts"""
        # main Layout 
        self.bodyDummyLayout = QVBoxLayout()
        
        # search Zone
        self.searchSectionDummyLayout = QHBoxLayout() # Holder
        self.searchSectionInnerDummyLayout =  QVBoxLayout()
        self.searchFieldDummyLayout = QHBoxLayout()  # Search Bar
        self.searchRelatedButtonDummyLayout = QHBoxLayout() # Buttons
        
        self.actionDummyLayout = QHBoxLayout() # Control Section + View Section

        # control Section
        self.controlSectionDummyLayout = QVBoxLayout()
        self.controlSectionInnerDummyLayout = QVBoxLayout()

        # view Section
        self.viewPanelDummyLayout = QHBoxLayout()
        self.viewPanelInnerDummyLayout = QHBoxLayout()
        self.tableHolderDummyLayout = QHBoxLayout()
        return
    
    def _buildButtons(self) -> None:
        # search Related
        self.searchButton = QPushButton()
        self.searchBySingerButton = QPushButton()

        # Control Related
        self.BackGroundButton = QPushButton()
        self.setDownloadDirectory = QPushButton()
        self.HighQualityEnableButton = QPushButton()
        self.lowQualityEnableButton = QPushButton()
        self.showDownloadingHistory = QPushButton()
        self.deleteDownloadingHistory = QPushButton()
        self.deleteButton = QPushButton()
        return
    
    def _buildLineInput(self) -> None:
        self.inputField = QLineEdit()
        self.inputField.setDisabled(True) # for preview purpose no need to take input
        return

    def _constructUI(self) -> None:
        """
            This method must be run after the _buildFrames method
            inside the constructor to form the GUI using the components
        """
        #MAIN WINDOW
        self.masterDummyLayout.addWidget(self.masterDummyLayoutInnerFrame, Qt.AlignmentFlag.AlignCenter)
        self.masterDummyLayoutInnerFrame.setLayout(self.bodyDummyLayout)
        
        #INPUT SECTION
        self.bodyDummyLayout.addLayout(self.searchSectionDummyLayout, 10)
        self.searchSectionDummyLayout.addWidget(self.searchSectionDummyLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.searchSectionDummyLayoutFrame.setLayout(self.searchSectionInnerDummyLayout)
        self.searchSectionInnerDummyLayout.addLayout(self.searchFieldDummyLayout, 50)
        self.searchSectionInnerDummyLayout.addLayout(self.searchRelatedButtonDummyLayout, 50)

        #ACTION SECTION
        self.bodyDummyLayout.addLayout(self.actionDummyLayout, 90)

        #CONTROL PANEL
        self.actionDummyLayout.addLayout(self.controlSectionDummyLayout, 20)
        self.controlSectionDummyLayout.addWidget(self.controlSectionDummyLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.controlSectionDummyLayoutFrame.setLayout(self.controlSectionInnerDummyLayout)

        #VIEW PANEL
        self.actionDummyLayout.addLayout(self.viewPanelDummyLayout, 80)
        self.viewPanelDummyLayout.addWidget(self.viewPanelDummyLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.viewPanelDummyLayoutFrame.setLayout(self.viewPanelInnerDummyLayout)
        return
    
    def _addAttributes(self):
        """
            Packs all the widgets in their holder layouts
        """
        # search Section
        self.searchFieldDummyLayout.addWidget(self.inputField, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonDummyLayout.addWidget(self.searchBySingerButton, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonDummyLayout.addWidget(self.searchButton, Qt.AlignmentFlag.AlignCenter)

        # Control Section
        self.controlSectionInnerDummyLayout.addWidget(self.BackGroundButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.HighQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.lowQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.setDownloadDirectory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.showDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.deleteDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerDummyLayout.addWidget(self.deleteButton, alignment = Qt.AlignmentFlag.AlignTop)
        return

    def _loadStyleSheet(self) -> None:
        """
            Read the QML file and load the style for this window
            :return:
        """
        try:
            file = QFile(os.path.join(os.getcwd(), Constants.DUMMY_FILE_STYLE_PATH)) # Creating File Objects
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY) # extracting Style
                self.setStyleSheet(qss) # adding Style
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error
        return

    ############################################# Interfacing #######################################################
    def show(self):
        # show method is overridden to reset the wallpaper to arora1.jpg
        self.setWallpaper()
        return super().show()

    #### wallpaper related operations
    def setWallpaper(self) -> None:
        """
            Check's if the currentWallpaperLocation exists or not. IF doesn't exist then default location is given and
            default wallpaper is set to the Dummy Interface
            :return: None
        """
        if not os.path.exists(self.currentWallpaperLocation):
            self.currentWallpaperLocation = Constants.DEFAULT_WALLPAPER_LOCATION

        saving_directory = self.resizeGivenWallpaper(self.currentWallpaperLocation)

        if saving_directory: # if final_path is a valid path only then wallpaper will change
            self.masterDummyLayoutInnerFrame.setStyleSheet(
                "#master_inner_layout_frame{background-image: url(" + saving_directory + ");}"
            )
        else: # if final_path is not valid then default wallpaper will be set
            self.masterDummyLayoutInnerFrame.setStyleSheet(
                "#master_inner_layout_frame{background-image: url(" + Constants.DEFAULT_WALLPAPER_LOCATION + ");}"
            )
        return None


    def resizeGivenWallpaper(self, location : str = None) -> str | None:
        """
            This method resizes the currently selected image from the static path or any other image form the system
            and saves it in temp. If any error occurred then sends a signal to the application
        """
        if location: # checking validity of location
            location = location.replace("\\", "/")
            savingPath = (os.path.join(os.getcwd(), "DummyResourceFolder/", location.split("/")[-1])
                .replace("\\", "/"))

            self.imageModifierEngine.resizeImage(
                location, Constants.DUMMY_WINDOW_WIDTH, Constants.DUMMY_WINDOW_HEIGHT, savingPath
            ) # resizing to fit with window dimension

            if os.path.exists(savingPath): return savingPath
            else: return None
        else: return None

    ##### Dummy Resource folder related operations
    @staticmethod
    def clearDummyResourceFolder() -> None:
        """
            After performing any os related operation in DummyResourceFolder clear the dummy resource folder
            :return: None
        """
        try:
            dummy_resource_folder = os.path.join(os.getcwd(), Constants.DUMMY_RESOURCE_FOLDER).replace(
                "\\", "/"
            )
            for file in os.listdir(dummy_resource_folder):
                os.remove(os.path.join(dummy_resource_folder, file))
        except (OSError, PermissionError, FileNotFoundError):
            print("got Error")
    pass

if __name__ == '__main__':
    app = QApplication([])
    window = DummyPreview()
    window.show()
    app.exec_()