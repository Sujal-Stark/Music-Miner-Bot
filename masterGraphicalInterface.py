# this file is mainly responsible for creating the Graphical user inerface of the software using pyqt5
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QLabel, QScrollArea, QTableWidget, QTableWidgetItem, QAbstractItemView, QToolTip, QFileDialog
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5.QtGui import QIcon, QPixmap, QFont
from icecream import ic
import os

# custom import
import Constants
from ImageModifierEngine import ImageModifier
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
from TablePopulatorThreadClass import TableDataStreamer
from TuneDownloaderThreadForPW import TuneDownloaderThread
from UserInformationHandler import ConfigFileHandler

class MasterGrapicalUserInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(Constants.SOFTWARE_TITLE) # application name
        self.setWindowIcon(QIcon(Constants.ICON_PATH)) # icon for the application
        self.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT) # application max size
        self._initializeHelperClassConstructor() # all useful classes are Initialised with parameters if any
        self._initializeUI() # builds all the components
        self._constuctUI() # form the layouts together
        self._addAttributes() # add widgets to the layouts
        self.setPosterAtTableView() # shows the poster in TableView
        self._loadStyleSheet() # loads the Qss
        self._setUpToolTip() # initialize tool tips
        self._setResponse() # all Actions and Signals are bind with UI Elements
        self._generateConfigFile()
        return

    def _initializeHelperClassConstructor(self) -> None:
        '''This method initializes all the important classes to work with in a one go'''
        self.searchEngine = PagalFreeSiteExplorer() # initializing the search engine
        self.configFileHander = ConfigFileHandler() # create and update Config Details
        self.streamer = TableDataStreamer() # Populate the table with Song data
        self.tuneDownlaoderThread = TuneDownloaderThread() # Download a particular song
        self.imageModifierEngine = ImageModifier() # handles UI image related Actions
        return

    def _initializeUI(self) -> None:
        '''this function must be called inside the  constructor so that when the class is called all the uI components get's loaded in the window'''
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
        self.resourceFreeFlag = True # if false then no data will be passed to this class'es data from engine
        self.posterLabels : list[QPixmap] = None
        self.generatedConfigLocation : str = None # if config file exists this str object will store the address
        self.DOWNLOADING_DIRECTORY = "D:\\Music Lib" # setting the downloading directory temporarily
        return

    def _preferences(self) -> None:
        '''Preferences help to sort out the required results for the users'''
        self.SEARCH_BY_SINGER_ENABLE = False # enables when user wants to search singer's name
        self.SEARCH_HIGH_QUALITY = False # enables  when user only want's high quality search results
        self.SEARCH_LOW_QUALITY = False # enables when the user only want's low quality search Results
        return

    def _setResponse(self)-> None:
        '''Predefines all the actions to their respected Widgets'''
        self.searchButton.clicked.connect(self.searchButtonAction) #Start Searching internet, Retrieve data and show it
        self.searchBySingerButton.clicked.connect(lambda : self._showClickedState()) # NOT IN WORKING STATE

        self.setDownloadDirectory.clicked.connect(self._selectDownloadingDirectory) # To choose Downloading Directory
        self.HighQualityEnableButton.clicked.connect(self.applyQualityFiler) # only Show High Quality Songs
        self.lowQualityEnableButton.clicked.connect(self.applyQualityFiler) # only Show Low Quality Songs
        self.deleteButton.clicked.connect(self._resetPanelAction) # Delete The Search Result

        # Signal Response Addition
        self.streamer.dataOnFly.connect(self._addItemToTable) # Accept data from Populator Thread
        self.tuneDownlaoderThread.messageSignal.connect(lambda message : print(message)) # Shows download Status
        return

    def _buildFrames(self) -> None:
        '''This method must be called inside initializeUI method to load all the frames using in the UI, no relevent extternal use'''
        # holds an masterLayout and holds an image for the GUI
        self.masterLayoutFrame = QFrame()
        self.masterLayoutFrame.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT)
        self.masterLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterLayoutFrame.setObjectName("master_layout_frame")
        self._resizeGivenWallpaper()
        self.masterLayoutFrame.setStyleSheet("""
            #master_layout_frame{
                background-image: url(./static/arora1.jpg);
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

        self.viewPanelLayoutFrame = QFrame() # provides shape to the ViewPanellayout
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
        '''Should be used in _initializeUI method. This method buils scrol areas'''
        self.tableScrollArea = QScrollArea() # provides scroll area to the table view
        self.tableScrollArea.setWidgetResizable(True)
        self.tableScrollArea.setFixedSize(Constants.VIEW_PANEL_WIDTH -20, Constants.VIEW_PANEL_HEIGHT - 20)
        self.tableScrollArea.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
        self.tableScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return

    def _buildLayouts(self) -> None:
        '''Must be called inside _initializeUI method. it is used to build the Layouts'''
        self.masterLayout = QVBoxLayout() # master layout for centeral widget
        self.bodyLayout = QVBoxLayout() # boy layout holds all functioning layouts
        
        self.searchSectionLayout = QHBoxLayout() # search field
        self.searchSectionInnerLayout =  QVBoxLayout() # held by frame
        self.searchFieldLayout = QHBoxLayout() # holds the search bar
        self.searchRelatedButtonLayout = QHBoxLayout() # holds the other butten related to search
        
        self.actionLayout = QHBoxLayout() # holds Control sectio and view table

        self.controlSectionLayout = QVBoxLayout()
        self.controlSectionInnerLayout = QVBoxLayout() # holds the control widgets

        self.viewPanelLayout = QHBoxLayout() # stores the song details
        self.viewPanelInnerLayout = QHBoxLayout() # stores the table Scroll Widget
        self.tableHolderLayout = QHBoxLayout() # holds the table
        return
    
    def _buildTableWidget(self) -> None:
        '''Mean't to be  called under _initailizeUI method builds the table view of the generated song data'''
        self.mainTable = QTableWidget() # holds the scraped Data
        self.mainTable.setFixedSize(self.tableScrollArea.width()- 20, self.tableScrollArea.height()- 20) # dimentions
        self.mainTable.setColumnCount(4) # column counts are always fixed
        self.mainTable.setWordWrap(True)
        # column width Must be constants
        self.mainTable.setColumnWidth(0, Constants.THUMBNAIL_SIZE) # HOLDS PIXMAP POSTER
        self.mainTable.setColumnWidth(1,Constants.SONG_NAME_SIZE) # SONG NAME WITH BIT RATE
        self.mainTable.setColumnWidth(2,Constants.SINGER_NAME_SIZE) # SINGER NAME
        self.mainTable.setColumnWidth(3, Constants.DOWNLOAD_URL_SIZE) # BUTTON 
        
        self.mainTable.setHorizontalHeaderLabels( # column headings
            [Constants.THUMBNAIL, Constants.DOWNLOAD_URL, Constants.SONG_NAME, Constants.SINGER_NAME]
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
        self.BackGroundbutton = QPushButton(Constants.CHANGE_BACKGROUND) # change BackGround
        self.BackGroundbutton.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH,
        Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.BackGroundbutton.setToolTip(Constants.BACKROUND_BUTTON_TOOL_TIP)
        
        self.setDownloadDirectory = QPushButton(Constants.SET_DOWNLOAD_DIRECTORY) # change Download directory
        self.setDownloadDirectory.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.setDownloadDirectory.setToolTip(Constants.DOWNLOAD_DIRECTORY_BUTTON_TOOL_TIP)
        
        self.HighQualityEnableButton = QPushButton(Constants.SHOW_HIGH_QUALITY) # only filter High Quality songs
        self.HighQualityEnableButton.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.HighQualityEnableButton.setToolTip(Constants.HIGH_QUALITY_ENABLE_BUTTON_TOOL_TIP)
        self.HighQualityEnableButton.setCheckable(True)
        self.HighQualityEnableButton.setObjectName(Constants.SHOW_HIGH_QUALITY)
        
        self.lowQualityEnableButton = QPushButton(Constants.SHOW_LOW_QUALITY) # only filter Low Quality songs
        self.lowQualityEnableButton.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.lowQualityEnableButton.setToolTip(Constants.LOW_QUALITY_ENABLE_BUTTON_TOOL_TIP)
        self.lowQualityEnableButton.setCheckable(True)
        self.lowQualityEnableButton.setObjectName(Constants.SHOW_LOW_QUALITY)
        
        self.showDownloadingHistory = QPushButton(Constants.SHOW_DOWNLOAD_HISTORY) # shows how many songs are downloaded
        self.showDownloadingHistory.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.showDownloadingHistory.setToolTip(Constants.DOWNLOAD_HISTORY_BUTTON_TOOL_TIP)
        
        self.deleteDownlaodingHistory = QPushButton(Constants.DELETE_DOWNLOAD_HISTORY) # delete all the downloading history
        self.deleteDownlaodingHistory.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.deleteDownlaodingHistory.setToolTip(Constants.DELETE_DOWNLOAD_HISTORY_BUTTON_TOOL_TIP)

        self.deleteButton = QPushButton(Constants.RESET_VIEW_PANEL) # Removes the Seaarch Result From table
        self.deleteButton.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.deleteButton.setToolTip(Constants.RESET_PANEL_BUTTON_TOOL_TIP)
        return
    
    def _buildLabels(self) -> None:
        '''Meant to be called in the _constructUI method and forms QLabels'''
        self.default_label = QLabel() # holdsthe poster image
        self.default_label.setToolTip(Constants.LABEL_POSTER_TOOL_TIP)
        return
    
    def _buildLineInput(self) -> None:
        self.inputField = QLineEdit() # takes input from user
        self.inputField.setPlaceholderText(Constants.SEARCH_HERE)
        return

    def _constuctUI(self) -> None:
        '''This method must be run after the _buildFrames method inside the constructor to form the GUI using the components'''
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
        return
    
    def _addAttributes(self):
        '''Packs all the widgets in their holder layouts'''
        # search Section
        self.searchFieldLayout.addWidget(self.inputField, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchBySingerButton, Qt.AlignmentFlag.AlignCenter)
        self.searchRelatedButtonLayout.addWidget(self.searchButton, Qt.AlignmentFlag.AlignCenter)

        # Control Section
        self.controlSectionInnerLayout.addWidget(self.BackGroundbutton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_one, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.HighQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.lowQualityEnableButton, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_two, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.setDownloadDirectory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.showDownloadingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteDownlaodingHistory, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.separator_three, alignment=Qt.AlignmentFlag.AlignTop)
        self.controlSectionInnerLayout.addWidget(self.deleteButton, alignment = Qt.AlignmentFlag.AlignTop)
        # View panel
        self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    # INTERFACING
    def _resizeGivenWallpaper(self) -> None:
        '''For the back ground of the application this method resizes the currently selected image from the static path and saves it. If any error occurred then sends a signal to the application'''
        if(loc:= self.configFileHander.getCurrentWallpaperLocation()):
            self.imageModifierEngine.resizeImage(loc)
        else:
            pass # signal will be added later
        return
    
    def setPosterAtTableView(self)-> None:
        '''Alter table method removes the table from the table view and put poster image'''
        self.default_label.hide() # for safety purposes
        try:
            table_default_poster = QPixmap(Constants.TABLE_DEFAULT_LABEL)
            table_default_poster = table_default_poster.scaled(
                Constants.VIEW_PANEL_WIDTH - 40, Constants.VIEW_PANEL_HEIGHT - 40
            )
            self.default_label.setPixmap(table_default_poster)
        except (OSError, PermissionError, ValueError, MemoryError, TypeError, FileNotFoundError): return # handles file related errors
        self.default_label.show() # shows the image in the table view
        return
    
    def alterPosterView(self) -> None:
        '''Removes the poster and show the  table containing data'''
        if(self.mainTable.parent() == None): # only psot the table if it is not posted
            self.default_label.hide()
            self.default_label.setParent(None)
            self.tableHolderLayout.addWidget(self.mainTable, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    def _loadStyleSheet(self) -> None:
        '''Should be called in the constructor and it loads the style sheet from qml file'''
        try:
            file = QFile(Constants.MAIN_QML_PATH)
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error
        return
    
    def _setUpToolTip(self) -> None:
        QToolTip.setFont(QFont("Georgia", 10))
        return
    
    def _showClickedState(self) -> None:
        '''Change the clicked and unclicked state for all the checkable buttons'''
        if(self.sender().objectName() == Constants.SEARCH_BY_SINGER_BUTTON):
            if self.searchBySingerButton.isChecked():
                self.searchBySingerButton.setStyleSheet(Constants.SET_CHECKED_STYLE)
                self.searchBySingerButton.setCheckable(False)
                self.SEARCH_BY_SINGER_ENABLE = True # constrol change
            else:
                self.searchBySingerButton.setStyleSheet(Constants.SET_UNCHECKED_STYLE)
                self.searchBySingerButton.setCheckable(True)
                self.SEARCH_BY_SINGER_ENABLE = False # control changed
        
        elif(self.sender().objectName() == Constants.SHOW_HIGH_QUALITY):
            if(self.HighQualityEnableButton.isChecked()):
                self.HighQualityEnableButton.setStyleSheet(Constants.SET_CHECKED_STYLE)
                self.HighQualityEnableButton.setCheckable(False)
                self.SEARCH_HIGH_QUALITY = True # control changed
            else:
                self.HighQualityEnableButton.setStyleSheet(Constants.SET_UNCHECKED_STYLE)
                self.HighQualityEnableButton.setCheckable(True)
                self.SEARCH_HIGH_QUALITY = False # control changed
        
        elif(self.sender().objectName() == Constants.SHOW_LOW_QUALITY):
            if(self.lowQualityEnableButton.isChecked()):
                self.lowQualityEnableButton.setStyleSheet(Constants.SET_CHECKED_STYLE)
                self.lowQualityEnableButton.setCheckable(False)
                self.SEARCH_LOW_QUALITY = True # control change
            else:
                self.lowQualityEnableButton.setStyleSheet(Constants.SET_UNCHECKED_STYLE)
                self.lowQualityEnableButton.setCheckable(True)
                self.SEARCH_LOW_QUALITY = False # control change
        return
    
    def _downloadSelectedSong(self) -> None:
        '''uses An Thread in the background and downloads the asked song in the Chosen directory'''
        sender = self.sender()
        self.tuneDownlaoderThread.getInstructions(
            self.configFileHander.getDownloadingDirectory(),
            sender.property(Constants.SONG_NAME),
            sender.property(Constants.HREF)
        ) # takes infortation like name directory and link
        self.tuneDownlaoderThread.start()
        return


    def _addItemToTable(self, index : int, song_name : str, singer_name : str, href : str, picture : QPixmap) -> None:
        '''This method acts as Signal Acceptor. Accepts table Items from the Thread class(TablePopulatorThreadClass) and exhibit in the table'''
        self.mainTable.insertRow(index) # row defination
        self.mainTable.setRowHeight(index, Constants.ROW_HEIGHT)
        if(picture): # if poster is found out only then poster will be shown
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setPixmap(picture)
            self.mainTable.setCellWidget(index, 0, label)
        
        button = QPushButton(Constants.DOWNLOAD_BUTTON_TEXT) # button
        button.setStyleSheet(Constants.DOWNLOAD_BUTTON_STYLE)
        button.setProperty(Constants.HREF, href) # href holds the link for the downloading page
        button.setProperty(Constants.SONG_NAME, song_name)
        button.clicked.connect(self._downloadSelectedSong) # Temporary Button that's why can't Put this action in response method
        
        self.mainTable.setCellWidget(index, 1, button)
        self.mainTable.setItem(index, 2, QTableWidgetItem(song_name)) # song name
        self.mainTable.setItem(index, 3, QTableWidgetItem(singer_name)) # singer's name
        return

    def searchButtonAction(self) -> None:
        '''Works after search button is pressed. Handles searchBySinger & searchBySong Both the action'''
        sender_ObjectName = self.sender().objectName()
        if(self.inputField.text() != "" and (
            sender_ObjectName == Constants.SHOW_HIGH_QUALITY or sender_ObjectName == Constants.SHOW_LOW_QUALITY or self.resourceFreeFlag
        )): # no search if input field is empty
            try:
                if(self.SEARCH_BY_SINGER_ENABLE): # if singer name search is enabled
                    pass
                else: # if only song search is queried
                    self._clearTable()
                    self.alterPosterView() # table will be show
                    controlSignalList = {
                        self.streamer.SEARCH_BY_SINGER : self.SEARCH_BY_SINGER_ENABLE,
                        self.streamer.FILTER_HIGH_QUALITY : self.SEARCH_HIGH_QUALITY,
                        self.streamer.FILTER_LOW_QUALITY : self.SEARCH_LOW_QUALITY
                    }
                    self.streamer.getInputs(self.inputField.text(), controlSignalList) # provides input to populate table
                    self.streamer.start()
            except (TypeError): pass
            self.resourceFreeFlag = False # resources are occupied
        return
    
    def applyQualityFiler(self) -> None:
        '''Again Rearranges the data in the table using background Threads according to user preference'''
        self._showClickedState() # set and reset control varibles and button states
        self.searchButtonAction() # re-arrange data
        return

    def _clearTable(self) -> None:
        self.mainTable.clearContents() # clearing the table
        self.mainTable.setRowCount(0) # cleaning the table
        return

    def _resetPanelAction(self) -> None:
        '''Clears memory of the data structures and also removes the table and set the poster'''
        if(self.mainTable.parent()):
            self.mainTable.setParent(None)
            self._clearTable()
            self.resourceFreeFlag = True # resouces are free
            self.searchEngine._cleanAllMemory() # all resources are free
            self.streamer.releaseResources() # all the resources will be released
            self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.default_label.show() # poster will be shown instead of table
        return
    
    def _generateConfigFile(self) -> None:
        '''IF Software doesn.t have any config file then This method generate config file'''
        self.generatedConfigLocation = self.configFileHander.generateConfigFile() # configFileLocation is set
        return

    def _selectDownloadingDirectory(self) -> None:
        '''Changes the downloading directory as per user's Choice'''
        if(os.path.exists(self.generatedConfigLocation)):
            explorer = QFileDialog.getExistingDirectory(caption = Constants.SELECT_DIRECTORY)
            if(explorer != ""): self.configFileHander.setDownloadingDirectory(explorer)
        else: pass
        return
    pass


if __name__ == "__main__":
    pass