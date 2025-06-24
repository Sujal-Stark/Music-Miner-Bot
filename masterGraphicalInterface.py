# this file is mainly responsible for creating the Graphical user interface of the software using pyqt5
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QLabel,
QScrollArea, QTableWidget, QAbstractItemView, QToolTip, QFileDialog, QShortcut)
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtGui import QIcon, QPixmap, QFont, QKeySequence
import os

# custom import
import Constants
from ImageModifierEngine import ImageModifier
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
from TablePopulatorThreadClass import TableDataStreamer
from TuneDownloaderThreadForPW import TuneDownloaderThread
from UserInformationHandler import ConfigFileHandler
from WallPaperPreview import SelectWallpaperUI
from SongCard import SongCard
from DataBaseManager import DataBaseManager
from utility import Utility


class MasterGraphicalUserInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(Constants.SOFTWARE_TITLE) # application name
        self.setWindowIcon(QIcon(Constants.ICON_PATH)) # icon for the application
        self.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT) # application max size
        self.configFileHandler = ConfigFileHandler()  # create and update Config Details

        self._initializeUI() # builds all the components
        self._constructUI() # form the layouts together
        self._addAttributes() # add widgets to the layouts
        self.setPosterAtTableView() # shows the poster in TableView
        self._loadStyleSheet() # loads the Qss

        self._initializeHelperClassConstructor() # all useful classes are Initialised with parameters if any
        self._createKeySequence()
        self._setUpToolTip() # initialize tool tips
        self._setResponse() # all Actions and Signals are bind with UI Elements

        # initial Action
        self._generateConfigFiles() # Throughout system all files regarding user preferences and choices will be generated
        self._configFileExistAction() # use Config file styles and data
        self._colorFileExistsAction() # use Colors file styles and data
        return

    def _initializeHelperClassConstructor(self) -> None:
        """
            This method initializes all the important classes to work with in a one go
        """
        self.searchEngine = PagalFreeSiteExplorer() # initializing the search engine
        self.streamer = TableDataStreamer() # Populate the table with Song data
        self.tuneDownloaderThread = TuneDownloaderThread() # Download a particular song
        self.imageModifierEngine = ImageModifier() # handles UI image related Actions
        self.databaseManager = DataBaseManager() # Manage all crud operation related to Downloading History
        return

    def _initializeUI(self) -> None:
        """
            this function must be called inside the  constructor so that when the class is called,
            all the UI components gets loaded in the window
        """
        self._properties()
        self._buildFrames()
        self._buildScrollArea()
        self._buildLayouts()
        self._buildButtons()
        self._buildLabels()
        self._buildLineInput()
        self._buildTableWidget()
        self._preferences()
        return

    def _properties(self) -> None:
        self.resourceFreeFlag = True # if false then no data will be passed to this classes data from engine
        self.generatedConfigLocation : str = None # if config file exists this str object will store the address
        self.staticContent = [
            "./static/arora1.jpg",
            "./static/blackHole.jpeg",
            "./static/desert.jpeg",
            "static/dragon.jpeg",
            "./static/icon.png",
            "./static/planet.jpeg",
            "./static/startingScreen.png",
            "./static/tagline.png"
        ] # Static content of the application

        # config related information
        self.WALLPAPER_LOCATION = None
        self.USER_NAME = None
        self.CURRENT_DOWNLOADING_DIRECTORY = None
        return

    def _preferences(self) -> None:
        """Preferences help to sort out the required results for the users"""
        self.SEARCH_BY_SINGER_ENABLE = False # enables when user wants to search singer's name
        self.SEARCH_HIGH_QUALITY = False # enables  when user only want's high quality search results
        self.SEARCH_LOW_QUALITY = False # enables when the user only want's low quality search Results
        return

    def _setResponse(self)-> None:
        """Predefines all the actions to their respected Widgets"""
        # search section buttons
        self.searchButton.clicked.connect(self.searchButtonAction) #Start Searching internet, Retrieve data and show it
        self.searchBySingerButton.clicked.connect(lambda : self._showClickedState()) # NOT IN WORKING STATE

        # control section buttons
        self.BackGroundButton.clicked.connect(self.backGroundButtonAction) # change wallpaper
        self.setDownloadDirectory.clicked.connect(self._selectDownloadingDirectory) # To choose Downloading Directory
        self.HighQualityEnableButton.clicked.connect(self.applyQualityFiler) # only Show High Quality Songs
        self.lowQualityEnableButton.clicked.connect(self.applyQualityFiler) # only Show Low Quality Songs
        self.showDownloadingHistory.clicked.connect(self._showDownloadingHistory) # Display downloading History
        self.deleteDownloadingHistory.clicked.connect(self.databaseManager.truncateTableFromDataBase)
        self.deleteButton.clicked.connect(self._resetPanelAction) # Delete The Search Result

        # Signal Response Addition
        self.streamer.dataOnFly.connect(self._addItemToTable) # Accept data from Populator Thread
        self.streamer.outputSignal.connect(self._setMessageForUser) # Shows information to the user
        self.tuneDownloaderThread.messageSignal.connect(self._setMessageForUser) # Shows download Status
        return

    def _createKeySequence(self) -> None:
        """
            All required key Sequence for this UI are built here
            :return: None
        """
        self.enterKeyAction = QShortcut(QKeySequence(Qt.Key.Key_Enter), self)
        self.enterKeyAction.setObjectName(Constants.ENTER_KEY_SHORTCUT)
        self.enterKeyAction.activated.connect(lambda: self.searchButtonAction())
        return None

    def _buildFrames(self) -> None:
        """This method must be called inside initializeUI method to load all the frames using in the UI, no relevant
         external use"""
        # holds an masterLayout and holds an image for the GUI
        self.masterLayoutFrame = QFrame()
        self.masterLayoutFrame.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT)
        self.masterLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterLayoutFrame.setObjectName(Constants.MASTER_FRAME_OBJECT_NAME)
        self.masterLayoutFrame.setStyleSheet("""
            #master_layout_frame{
                background-repeat: repeat;
                background-position: center;
            }
        """)
        
        self.masterLayoutInnerFrame = QFrame() # provides shape to the master layout
        self.masterLayoutInnerFrame.setFixedSize(Constants.SOFTWARE_WIDTH - 20, Constants.SOFTWARE_HEIGHT - 20)
        self.masterLayoutInnerFrame.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.searchSectionLayoutFrame = QFrame() # provides shape to SearchSectionLayout
        self.searchSectionLayoutFrame.setFixedSize(Constants.SEARCH_SECTION_WIDTH, Constants.SEARCH_SECTION_HEIGHT)
        self.searchSectionLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        self.controlSectionLayoutFrame = QFrame() # Provides shape to ControlSectionLayout
        self.controlSectionLayoutFrame.setFixedSize(Constants.CONTROL_SECTION_WIDTH, Constants.CONTROL_SECTION_HEIGHT)
        self.controlSectionLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)

        self.viewPanelLayoutFrame = QFrame() # provides shape to the ViewPanelLayout
        self.viewPanelLayoutFrame.setFixedSize(Constants.VIEW_PANEL_WIDTH, Constants.VIEW_PANEL_HEIGHT)
        self.viewPanelLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        
        # Horizontal Separators
        self.separator_one = QFrame() # separates Background edit option
        self.separator_one.setFrameShape(QFrame.Shape.HLine)
        self.separator_two = QFrame() # separates quality control options
        self.separator_two.setFrameShape(QFrame.Shape.HLine)
        self.separator_three = QFrame() # not used til now just made
        self.separator_three.setFrameShape(QFrame.Shape.HLine)
        return
    
    def _buildScrollArea(self) -> None:
        """Should be used in _initializeUI method. This method build scroll areas"""
        self.tableScrollArea = QScrollArea() # provides scroll area to the table view
        self.tableScrollArea.setWidgetResizable(True)
        self.tableScrollArea.setFixedSize(Constants.VIEW_PANEL_WIDTH -20, Constants.VIEW_PANEL_HEIGHT - 20)
        self.tableScrollArea.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.tableScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return

    def _buildLayouts(self) -> None:
        """Must be called inside _initializeUI method. it is used to build the Layouts"""
        self.masterLayout = QVBoxLayout() # master layout for central widget
        self.bodyLayout = QVBoxLayout() # boy layout holds all functioning layouts
        
        self.searchSectionLayout = QHBoxLayout() # search field
        self.searchSectionInnerLayout =  QVBoxLayout() # held by frame
        self.searchFieldLayout = QHBoxLayout() # holds the search bar
        self.searchRelatedButtonLayout = QHBoxLayout() # holds the other butten related to search
        
        self.actionLayout = QHBoxLayout() # holds Control section and view table

        self.controlSectionLayout = QVBoxLayout()
        self.controlSectionInnerLayout = QVBoxLayout() # holds the control widgets

        self.viewPanelLayout = QHBoxLayout() # stores the song details
        self.viewPanelInnerLayout = QHBoxLayout() # stores the table Scroll Widget
        self.tableHolderLayout = QHBoxLayout() # holds the table

        self.informationLayout = QHBoxLayout() # shows the signals given by methods
        return
    
    def _buildTableWidget(self) -> None:
        """Meant to be  called under _initializeUI method builds the table view of the generated song data"""
        self.mainTable = QTableWidget() # holds the scraped Data
        self.mainTable.setFixedSize(self.tableScrollArea.width()- 20, self.tableScrollArea.height()- 20) # dimensions
        self.mainTable.setColumnCount(1) # column counts are always fixed
        self.mainTable.setWordWrap(True)
        # column width Must be constants
        self.mainTable.setColumnWidth(0, Constants.SONG_CARD_WIDTH) # HOLDS PIXMAP POSTER
        
        self.mainTable.setHorizontalHeaderLabels( # column headings
            [Constants.SEARCH_RESULT]
        )
        self.mainTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # read only mode
        return

    def _buildButtons(self) -> None:
        # search Related
        self.searchButton = QPushButton(Constants.SEARCH_BUTTON) # search Button
        self.searchButton.setFixedHeight(Constants.SEARCH_SECTION_BUTTON_HEIGHT)
        self.searchButton.setToolTip(Constants.SEARCH_BUTTON_TOOL_TIP)

        self.searchBySingerButton = QPushButton(Constants.SEARCH_BY_SINGER_BUTTON) # use singer name
        self.searchBySingerButton.setObjectName(Constants.SEARCH_BY_SINGER_BUTTON)
        self.searchBySingerButton.setFixedHeight(Constants.SEARCH_SECTION_BUTTON_HEIGHT)
        self.searchBySingerButton.setToolTip(Constants.SEARCH_BY_SINGER_TOOL_TIP)
        self.searchBySingerButton.setCheckable(True)
        

        # Control Related
        self.BackGroundButton = QPushButton(Constants.CHANGE_BACKGROUND) # change BackGround
        self.BackGroundButton.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.BackGroundButton.setToolTip(Constants.BACKGROUND_BUTTON_TOOL_TIP)
        
        self.setDownloadDirectory = QPushButton(Constants.SET_DOWNLOAD_DIRECTORY) # change Download directory
        self.setDownloadDirectory.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.setDownloadDirectory.setToolTip(Constants.DOWNLOAD_DIRECTORY_BUTTON_TOOL_TIP)
        
        self.HighQualityEnableButton = QPushButton(Constants.SHOW_HIGH_QUALITY) # only filter High Quality songs
        self.HighQualityEnableButton.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.HighQualityEnableButton.setToolTip(Constants.HIGH_QUALITY_ENABLE_BUTTON_TOOL_TIP)
        self.HighQualityEnableButton.setCheckable(True)
        self.HighQualityEnableButton.setObjectName(Constants.SHOW_HIGH_QUALITY)
        
        self.lowQualityEnableButton = QPushButton(Constants.SHOW_LOW_QUALITY) # only filter Low Quality songs
        self.lowQualityEnableButton.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.lowQualityEnableButton.setToolTip(Constants.LOW_QUALITY_ENABLE_BUTTON_TOOL_TIP)
        self.lowQualityEnableButton.setCheckable(True)
        self.lowQualityEnableButton.setObjectName(Constants.SHOW_LOW_QUALITY)
        
        self.showDownloadingHistory = QPushButton(Constants.SHOW_DOWNLOAD_HISTORY) # shows how many songs are downloaded
        self.showDownloadingHistory.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.showDownloadingHistory.setToolTip(Constants.DOWNLOAD_HISTORY_BUTTON_TOOL_TIP)
        
        self.deleteDownloadingHistory = QPushButton(Constants.DELETE_DOWNLOAD_HISTORY) # delete all downloading history
        self.deleteDownloadingHistory.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT
        )
        self.deleteDownloadingHistory.setToolTip(Constants.DELETE_DOWNLOAD_HISTORY_BUTTON_TOOL_TIP)

        self.deleteButton = QPushButton(Constants.RESET_VIEW_PANEL) # Removes the Search Result From table
        self.deleteButton.setFixedSize(
            Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT        )
        self.deleteButton.setToolTip(Constants.RESET_PANEL_BUTTON_TOOL_TIP)
        return
    
    def _buildLabels(self) -> None:
        """Meant to be called in the _constructUI method and forms QLabels"""
        self.default_label = QLabel() # holds the poster image
        
        self.default_label.setToolTip(Constants.LABEL_POSTER_TOOL_TIP) # shows tool tip for each buttons
        
        self.infoLabel = QLabel(Constants.WELCOME) # holds information
        self.infoLabel.setFixedSize(Constants.INFORMATION_SECTION_WIDTH, 40)
        self.infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infoLabel.setStyleSheet("QLabel{color : #FFFFFF}")

        # indicator buttons
        self.highQualityEnableLabel = QLabel("H") # indicates state of High Quality Search
        self.highQualityEnableLabel.setFixedWidth(Constants.INDICATOR_WIDTH)
        self.highQualityEnableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.highQualityEnableLabel.setStyleSheet(self.indicatorDisableStyle())

        self.lowQualityEnableLabel = QLabel("L") # indicate state of Low quality search
        self.lowQualityEnableLabel.setFixedWidth(Constants.INDICATOR_WIDTH)
        self.lowQualityEnableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lowQualityEnableLabel.setStyleSheet(self.indicatorDisableStyle())

        self.searchForSignerEnableLabel = QLabel("S") # indicate state of Singer related Search
        self.searchForSignerEnableLabel.setFixedWidth(Constants.INDICATOR_WIDTH)
        self.searchForSignerEnableLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.searchForSignerEnableLabel.setStyleSheet(self.indicatorDisableStyle())
        return
    
    def _buildLineInput(self) -> None:
        self.inputField = QLineEdit() # takes input from user
        self.inputField.setPlaceholderText(Constants.SEARCH_HERE)
        return

    def _constructUI(self) -> None:
        """This method must be run after the _buildFrames method inside the constructor to form the GUI using the components"""
        #MAIN WINDOW
        self.setCentralWidget(self.masterLayoutFrame)
        self.masterLayoutFrame.setLayout(self.masterLayout)
        self.masterLayout.addWidget(self.masterLayoutInnerFrame, Qt.AlignmentFlag.AlignCenter)
        self.masterLayoutInnerFrame.setLayout(self.bodyLayout)
        
        #INPUT SECTION
        self.bodyLayout.addLayout(self.searchSectionLayout)
        self.searchSectionLayout.addWidget(self.searchSectionLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.searchSectionLayoutFrame.setLayout(self.searchSectionInnerLayout)
        self.searchSectionInnerLayout.addLayout(self.searchFieldLayout, Qt.AlignmentFlag.AlignCenter)
        self.searchSectionInnerLayout.addLayout(self.searchRelatedButtonLayout, Qt.AlignmentFlag.AlignCenter)

        #ACTION SECTION
        self.bodyLayout.addLayout(self.actionLayout)

        #CONTROL PANEL
        self.actionLayout.addLayout(self.controlSectionLayout, Qt.AlignmentFlag.AlignCenter)
        self.controlSectionLayout.addWidget(self.controlSectionLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.controlSectionLayoutFrame.setLayout(self.controlSectionInnerLayout)

        #VIEW PANEL
        self.actionLayout.addLayout(self.viewPanelLayout)
        self.viewPanelLayout.addWidget(self.viewPanelLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.viewPanelLayoutFrame.setLayout(self.viewPanelInnerLayout)
        self.viewPanelInnerLayout.addWidget(self.tableScrollArea)
        self.tableScrollArea.setLayout(self.tableHolderLayout)

        # INFORMATION HOLDER
        self.bodyLayout.addLayout(self.informationLayout)
        return
    
    def _addAttributes(self):
        """Packs all the widgets in their holder layouts"""
        # search Section
        self.searchFieldLayout.addWidget(self.highQualityEnableLabel, Qt.AlignmentFlag.AlignLeft) # indicator
        self.searchFieldLayout.addWidget(self.lowQualityEnableLabel, Qt.AlignmentFlag.AlignLeft) # indicator
        self.searchFieldLayout.addWidget(self.searchForSignerEnableLabel, Qt.AlignmentFlag.AlignLeft) # indicator
        self.searchFieldLayout.addWidget(self.inputField, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchBySingerButton, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchButton, Qt.AlignmentFlag.AlignCenter)

        # Control Section
        self.controlSectionInnerLayout.addWidget(self.BackGroundButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_one, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.HighQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.lowQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_two, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.setDownloadDirectory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.showDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_three, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteButton, alignment = Qt.AlignmentFlag.AlignTop)

        # View panel
        self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)

        # information Section
        self.informationLayout.addWidget(self.infoLabel, alignment = Qt.AlignmentFlag.AlignCenter)
        return

    def _loadStyleSheet(self) -> None:
        """Should be called in the constructor, and it loads the style sheet from qml file"""
        try:
            file = QFile(Utility.getResourcePath(Constants.MAIN_QML_PATH))
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error


    ############################################## INTERFACING ################################################
    # GUI Related action
    @staticmethod
    def _setUpToolTip() -> None:
        QToolTip.setFont(QFont("Georgia", 10))
        return

    # @pyqtSlot()
    def _setMessageForUser(self, msg : str = None) -> None:
        self.infoLabel.setText(msg)
        return
    
    def _showClickedState(self) -> None:
        """Change the clicked and unclicked state for all the checkable buttons"""
        if self.sender().objectName() == Constants.SEARCH_BY_SINGER_BUTTON:
            if self.searchBySingerButton.isChecked():
                self.searchBySingerButton.setCheckable(False)
                self.SEARCH_BY_SINGER_ENABLE = True # control change
                self.searchForSignerEnableLabel.setStyleSheet(self.indicatorEnabledStyle())
            else:
                self.searchBySingerButton.setCheckable(True)
                self.SEARCH_BY_SINGER_ENABLE = False # control changed
                self.searchForSignerEnableLabel.setStyleSheet(self.indicatorDisableStyle())
        
        elif self.sender().objectName() == Constants.SHOW_HIGH_QUALITY:
            if self.HighQualityEnableButton.isChecked():
                self.HighQualityEnableButton.setCheckable(False)
                self.SEARCH_HIGH_QUALITY = True # control changed
                self.highQualityEnableLabel.setStyleSheet(self.indicatorEnabledStyle())
            else:
                self.HighQualityEnableButton.setCheckable(True)
                self.SEARCH_HIGH_QUALITY = False # control changed
                self.highQualityEnableLabel.setStyleSheet(self.indicatorDisableStyle())
        
        elif self.sender().objectName() == Constants.SHOW_LOW_QUALITY:
            if self.lowQualityEnableButton.isChecked():
                self.lowQualityEnableButton.setCheckable(False)
                self.SEARCH_LOW_QUALITY = True # control change
                self.lowQualityEnableLabel.setStyleSheet(self.indicatorEnabledStyle())
            else:
                self.lowQualityEnableButton.setCheckable(True)
                self.SEARCH_LOW_QUALITY = False # control change
                self.lowQualityEnableLabel.setStyleSheet(self.indicatorDisableStyle())
        return

    @staticmethod
    def indicatorEnabledStyle() -> str:
        return """
            QLabel {
                color: #ffffff;
                background-color: #15e661;
                border-radius : 5px;
            }
        """

    @staticmethod
    def indicatorDisableStyle() -> str:
        return """
            QLabel {
                color: #000000;
                background-color: #ffffff;
                border-radius : 5px;
            }
        """

    # Music related
    def setPosterAtTableView(self) -> None:
        """Alter table method removes the table from the table view and put poster image"""
        self.default_label.hide()  # for safety purposes
        try:
            table_default_poster = QPixmap(Constants.TABLE_DEFAULT_LABEL)
            table_default_poster = table_default_poster.scaled(
                Constants.VIEW_PANEL_WIDTH - 40, Constants.VIEW_PANEL_HEIGHT - 40
            )
            self.default_label.setPixmap(table_default_poster)
        except (OSError, PermissionError, ValueError, MemoryError, TypeError, FileNotFoundError):
            return
        self.default_label.show()  # shows the image in the table view
        return

    def alterPosterView(self) -> None:
        """Removes the poster and show the  table containing data"""
        if self.mainTable.parent() is None:  # only post the table if it is not posted
            self.default_label.hide()
            self.default_label.setParent(None)
            self.tableHolderLayout.addWidget(self.mainTable, alignment=Qt.AlignmentFlag.AlignCenter)
        return

    def _downloadSelectedSong(self) -> None:
        """uses An Thread in the background and downloads the asked song in the Chosen directory"""
        sender = self.sender()
        self._setMessageForUser(Constants.DOWNLOAD_CONTINUES)
        self.tuneDownloaderThread = TuneDownloaderThread()
        self.tuneDownloaderThread.getInstructions(
            self.configFileHandler.getDownloadingDirectory(),
            sender.property(Constants.SONG_NAME),
            sender.property(Constants.HREF)
        ) # takes information like name directory and link

        self.tuneDownloaderThread.threadFinishedSignal.connect(
            self.downloadingFinishedSignalAction
        )  # cleans thread class variables
        self.tuneDownloaderThread.currentlyDownloadedSongName.connect(
            lambda songName : self.databaseManager.insertIntoTable(songName)
        ) # returns the song name and this method save it in Database
        self.tuneDownloaderThread.start()
        return

    def _addItemToTable(
            self, index: int, song_name: str, singer_name: str, href: str, picture: QPixmap
    ) -> None:
        """This method acts as Signal Acceptor. Accepts table Items from the Thread class(TablePopulatorThreadClass)
         and exhibit in the table"""
        self.mainTable.insertRow(index)  # row definition
        self.mainTable.setRowHeight(index, Constants.SONG_CARD_HEIGHT)
        songCard = SongCard()
        if picture:  # if poster is found out only then poster will be shown
            songCard.setImageToCard(picture)
        songCard.set_data(song_name, singer_name, href)
        songCard.downloadButton.clicked.connect(self._downloadSelectedSong)  # response Added
        self.mainTable.setCellWidget(index, 0, songCard)
        songCard.show()
        return

    def searchButtonAction(self) -> None:
        """Works after search button is pressed. Handles searchBySinger & searchBySong Both the action"""
        sender_ObjectName = self.sender().objectName()
        print(sender_ObjectName)
        if(self.inputField.text() != "" and (
            sender_ObjectName == Constants.SHOW_HIGH_QUALITY or
            sender_ObjectName == Constants.SHOW_LOW_QUALITY or
            sender_ObjectName == Constants.ENTER_KEY_SHORTCUT or
            self.resourceFreeFlag
        )): # no search if input field is empty
            try:
                controlSignalList = {
                    self.streamer.SEARCH_BY_SINGER: self.SEARCH_BY_SINGER_ENABLE,
                    self.streamer.FILTER_HIGH_QUALITY: self.SEARCH_HIGH_QUALITY,
                    self.streamer.FILTER_LOW_QUALITY: self.SEARCH_LOW_QUALITY
                }
                self.streamer.getInputs(self.inputField.text(), controlSignalList)  # provides input to populate table
                self._setMessageForUser(Constants.SEARCH_MSG) # Showing Info
                self.streamer.start()
                self._clearTable()
                self.alterPosterView()  # table will be shown
            except TypeError: self._setMessageForUser(Constants.UNEXPECTED_ERROR_MESSAGE) # showing error
            self.resourceFreeFlag = False # resources are occupied
        else: self._setMessageForUser(Constants.CLEAN_REQ_MESSAGE)
    
    def applyQualityFiler(self) -> None:
        """Again Rearranges the data in the table using background Threads according to user preference"""
        self._showClickedState() # set and reset control variables and button states
        self.searchButtonAction() # re-arrange data
        return

    def _clearTable(self) -> None:
        """Delete all rows from a table and removes all widgets in it OverAll TC O(n*m)"""
        self.mainTable.clearContents() # clearing the table
        self.mainTable.setRowCount(0) # cleaning the table
        return

    def _resetPanelAction(self) -> None:
        """Clears memory of the data structures and also removes the table and set the poster"""
        if self.mainTable.parent():
            self.mainTable.setParent(None)
            self._clearTable()
            self.resourceFreeFlag = True # resources are free
            self.searchEngine._cleanAllMemory() # all resources are free
            self.streamer.releaseResources() # all the resources will be released
            self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.default_label.show() # poster will be shown instead of table
        return

    def _selectDownloadingDirectory(self) -> None:
        """Changes the downloading directory as per user's Choice"""
        if os.path.exists(os.path.join(os.getcwd(), Constants.FILE_NAME)):
            downloadingPath = QFileDialog.getExistingDirectory(caption = Constants.SELECT_DIRECTORY)
            if downloadingPath != "": self.configFileHandler.setDownloadingDirectory(downloadingPath)
        else: pass
        return

    def downloadingFinishedSignalAction(self, completed : bool):
        if completed:
            self._setMessageForUser(Constants.DOWNLOAD_SUCCEED)
            self.tuneDownloaderThread.cleanMemory()
        return

    # Wallpaper related action
    def backGroundButtonAction(self) -> None:
        """
            Open Preview Window binds signals with methods and show the preview window
            :return: None
        """
        self.wallpaperPreview = SelectWallpaperUI(self.WALLPAPER_LOCATION)# creates separate window to preview wallpaper
        self.wallpaperPreview.fileSelectedSignal.connect(self._setWallpaper)  # set the wallpaper for background
        self.wallpaperPreview.wallpaperChangeAbortAction.connect(
            self.wallpaperPreview.previewUI.clearDummyResourceFolder
        ) # cleans the temp folder except wallpaper file
        self.wallpaperPreview.show()
        return

    def _setWallpaper(self, loc : str = None) -> None:
        """
            Change the wallpaper of the window with given image location
            :param loc: String [Valid image location]
            :return: None
        """
        if os.path.exists(loc):
            # full destination path for newly generated wallpaper
            destination_path = os.path.join(os.getcwd(),"temp/",loc.split("/")[-1]).replace("\\", "/")

            # changing style
            self._resizeGivenWallpaper(loc, dpath = destination_path)
            style = "#master_layout_frame{background-image: url(" + destination_path + ");}"
            self.masterLayoutFrame.setStyleSheet(style)
            self._changeButtonColor(
                    list(self.imageModifierEngine.computeAVGColor(destination_path))
                )

            # permanent setting
            self.configFileHandler.setWallpaperLocation(destination_path)
            self.imageModifierEngine.clearTempDirectory(destination_path)
        return

    def _resizeGivenWallpaper(self, loc : str = None, dpath : str = None) -> None:
        """
            For the background of the application this method resizes the currently selected
            image from the static path and saves it. If any error occurred then sends a signal to the application
        """
        if loc is None: loc = self.configFileHandler.getCurrentWallpaperLocation() # input is not given
        if loc: self.imageModifierEngine.resizeImage(imagePath = loc, dPath = dpath)
        else: self._setMessageForUser(Constants.FAILED_TO_COMMIT_CHANGE)
        return

    def _changeButtonColor(self, color : list = None) -> bool:
        if color is None or len(color) != 3: return False # no action needed for invalid Input
        if not isinstance(color, list): color = list(color)
        self.configFileHandler.setColorValueIntoFile(Constants.BUTTON_COLOR_CONFIG, color) # saving color value
        if color: self._alterColorStyle(self.generateSupportingColor(color))
        return True
    
    def _alterColorStyle(self, colorList : list[list]) -> bool:
        """Parameters: colorList -> list[str], unpack the string values and set them as Background
         color and text color in the main UI, maintaining other Styles same"""
        self.setStyleSheet(
            "QWidget {" + 
                "font-family: Georgia, Arial, sans-serif;" +
            "}" +
            "QPushButton {" + 
                f"background-color:rgb{tuple(colorList[0])};" + 
                f"color:rgb{tuple(colorList[1])};" +
                "border-radius: 5px;" +
                "border: 1px solid rgb(255, 255, 255);" + 
            "}" + 
            "QPushButton:hover {" +
                f"background-color: rgb{tuple(colorList[2])};"
            "}"
            "QPushButton:pressed {" + 
                f"background-color: rgb{tuple(colorList[3])};" +
            "}"
            "QFrame {" + 
                "border: 1px solid rgb(100, 100, 100);"
                "border-radius: 5px;"
            "}"
        )
        self.update()
        return False

    @staticmethod
    def generateSupportingColor(color : tuple[int, int, int]) -> list[list]:
        """Parameters: color: tuple[int, int, int] - RGB values (0-255).
            Returns: list[str]: [
                background color,   text (inverse) color,   hover effect color, clicked effect color
            ]
        """
        hoverColor : list = [min(i + 20, 255) for i in color] # RGB color value to animate hover effect
        clickedColor : list = [min(i + 40, 255) for i in color] # RGB color value to animate clicked effect
        inverseColor : list = [(255 - i) for i in color] # inverse color for text

        colorList : list = [color, inverseColor, hoverColor, clickedColor]
        return colorList

    # Config related action
    def _generateConfigFiles(self) -> None:
        """IF Software doesn't have any config data file then This method generate config file"""
        self.configFileHandler.generateConfigFile() # configFileLocation is set
        self.configFileHandler.generateColorFile() # generates colors.json file
        return

    def _configFileExistAction(self) -> None:
        if os.path.exists(os.path.join(os.getcwd(), Constants.FILE_NAME)):
            self.WALLPAPER_LOCATION = self.configFileHandler.getCurrentWallpaperLocation()
            if not os.path.exists(self.WALLPAPER_LOCATION):
                self.WALLPAPER_LOCATION = Constants.DEFAULT_WALLPAPER_LOCATION
            style = "#master_layout_frame{background-image: url(" + self.WALLPAPER_LOCATION + ");}"
            self.imageModifierEngine.getCurrentlyUsedImageLocation(self.WALLPAPER_LOCATION)
            self.masterLayoutFrame.setStyleSheet(style)
        else:
            self.masterLayoutFrame.setStyleSheet(
                "#master_layout_frame{background-image: url(./static/arora1.jpg);}"
            )
        return

    def _colorFileExistsAction(self) -> None:
        """If color file exists then this method fetch user preferences from file and inject in the UI style"""
        if os.path.exists(os.path.join(os.getcwd(), Constants.COLOR_FILE_REL_PATH)):
            color = self.configFileHandler.getColorValueFromFile(Constants.BUTTON_COLOR_CONFIG)
            if color: self._alterColorStyle(self.generateSupportingColor(color))
        return

    ######################################## Database Related Operations #####################################
    def _showDownloadingHistory(self) -> None:
        """
            Shows the Database in a separate window
            :return: None
        """
        self.databaseManager.show()
        self.databaseManager.displayData()
        return None
    pass


if __name__ == "__main__":
    pass