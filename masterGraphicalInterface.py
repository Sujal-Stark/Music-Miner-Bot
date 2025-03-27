# this file is mainly responsible for creating the Graphical user inerface of the software using pyqt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QLabel, QScrollArea, QTableWidget, QTableWidgetItem, QAbstractItemView, QToolTip, QSplashScreen
import time
from PyQt5.QtCore import Qt, QThread, QFile, QIODevice
from PyQt5.QtGui import QIcon, QPixmap, QFont
from icecream import ic
import sys

# custom import
import Constants
from ImageModifierEngine import ImageModifier
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
from TablePopulatorThreadClass import TableDataStreamer
from TuneDownloaderThreadForPW import TuneDownloaderThread

class MasterGrapicalUserInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(Constants.SOFTWARE_TITLE) # application name
        self.setWindowIcon(QIcon(Constants.ICON_PATH)) # icon for the application
        self.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT) # application max size
        self._initializeUI() # builds all the components
        self._constuctUI() # form the layouts together
        self._addAttributes() # add widgets to the layouts
        self._setResponse()
        self.setPosterAtTableView() # shows the poster in TableView
        self._loadStyleSheet() # loads the Qss
        self._setUpToolTip() # initialize tool tips
        self.searchEngine = PagalFreeSiteExplorer() # initializing the search engine 
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
        self.DOWNLOADING_DIRECTORY = "D:\Test" # setting the downloading directory temporarily
        return

    def _preferences(self) -> None:
        '''Preferences help to sort out the required results for the users'''
        self.SEARCH_BY_SINGER_ENABLE = False # enables when user wants to search singer's name
        self.SEARCH_HIGH_QUALITY = False # enables  when user only want's high quality search results
        self.SEARCH_LOW_QUALITY = False # enables when the user only want's low quality search Results
        return

    def _setResponse(self)-> None:
        '''Predefines all the actions to their respected Widgets'''
        self.searchButton.clicked.connect(self.searchButtonAction)
        self.searchBySingerButton.clicked.connect(lambda : self._showClickedState())

        self.HighQualityEnableButton.clicked.connect(lambda : self._showClickedState())
        self.lowQualityEnableButton.clicked.connect(lambda : self._showClickedState())
        self.resetViewPanel.clicked.connect(self._resetPanelAction)
        return

    def _buildFrames(self) -> None:
        '''This method must be called inside initializeUI method to load all the frames using in the UI, no relevent extternal use'''
        # holds an masterLayout and holds an image for the GUI
        self.masterLayoutFrame = QFrame()
        self.masterLayoutFrame.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT)
        self.masterLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterLayoutFrame.setObjectName("master_layout_frame")
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
        self.songDetailExhibiterTable = QTableWidget() # holds the scraped Data
        self.songDetailExhibiterTable.setFixedSize(self.tableScrollArea.width()- 20, self.tableScrollArea.height()- 20) # dimentions
        self.songDetailExhibiterTable.setColumnCount(4) # column counts are always fixed
        self.songDetailExhibiterTable.setWordWrap(True)
        # column width Must be constants
        self.songDetailExhibiterTable.setColumnWidth(0, Constants.THUMBNAIL_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(1,Constants.SONG_NAME_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(2,Constants.SINGER_NAME_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(3, Constants.DOWNLOAD_URL_SIZE)
        
        self.songDetailExhibiterTable.setHorizontalHeaderLabels( # column headings
            [Constants.THUMBNAIL, Constants.DOWNLOAD_URL, Constants.SONG_NAME, Constants.SINGER_NAME]
        )
        self.songDetailExhibiterTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # read only mode
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

        self.resetViewPanel = QPushButton(Constants.RESET_VIEW_PANEL)
        self.resetViewPanel.setFixedSize(Constants.CONTROL_SECTION_BUTTON_WIDTH, Constants.CONTROL_SECTION_BUTTON_HEIGHT)
        self.resetViewPanel.setToolTip(Constants.RESET_PANEL_BUTTON_TOOL_TIP)
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
        self.controlSectionInnerLayout.addWidget(self.resetViewPanel, alignment = Qt.AlignmentFlag.AlignTop)
        # View panel
        self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)
        return
    
    # INTERFACING    
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
        self.default_label.hide()
        self.default_label.setParent(None)
        self.tableHolderLayout.addWidget(self.songDetailExhibiterTable, alignment = Qt.AlignmentFlag.AlignCenter)
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
        ic(self.SEARCH_LOW_QUALITY, self.SEARCH_BY_SINGER_ENABLE, self.SEARCH_HIGH_QUALITY)
        return
    
    def _downloadSelectedSong(self) -> None:
        sender = self.sender()
        self.tuneDownlaoderThread = TuneDownloaderThread(
            self.DOWNLOADING_DIRECTORY, sender.property(Constants.SONG_NAME), sender.property(Constants.HREF)
        )
        self.tuneDownlaoderThread.messageSignal.connect(lambda message : print(message))
        self.tuneDownlaoderThread.start()
        return


    def _addItemToTable(self, index : int, song_name : str, singer_name : str, href : str, picture : QPixmap) -> None:
        '''This method acts as Signal Acceptor. Accepts table Items from the Thread class(TablePopulatorThreadClass) and exhibit in the table'''
        self.songDetailExhibiterTable.insertRow(index) # row defination
        self.songDetailExhibiterTable.setRowHeight(index, 150)
        if(picture): # if poster is found out only then poster will be shown
            label = QLabel()
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setPixmap(picture)
            self.songDetailExhibiterTable.setCellWidget(index, 0, label)
        button = QPushButton(Constants.DOWNLOAD_BUTTON_TEXT) # button
        button.setStyleSheet(Constants.DOWNLOAD_BUTTON_STYLE)
        button.setProperty(Constants.HREF, href) # href holds the link for the downloading page
        button.setProperty(Constants.SONG_NAME, song_name)
        button.clicked.connect(self._downloadSelectedSong)
        self.songDetailExhibiterTable.setCellWidget(index, 1, button)
        self.songDetailExhibiterTable.setItem(index, 2, QTableWidgetItem(song_name)) # song name
        self.songDetailExhibiterTable.setItem(index, 3, QTableWidgetItem(singer_name)) # singer's name
        return

    def searchButtonAction(self) -> None:
        '''Works after search button is pressed. Handles searchBySinger & searchBySong Both the action'''
        if(self.inputField.text() != "" and self.resourceFreeFlag): # no search if input field is empty
            try:
                if(self.SEARCH_BY_SINGER_ENABLE): # if singer name search is enabled
                    pass
                else: # if only song search is queried
                    self.alterPosterView() # table will be show
                    self.songDetailExhibiterTable.clearContents() # clearing the table
                    self.songDetailExhibiterTable.setRowCount(0)
                    self.streamer = TableDataStreamer(self.inputField.text())
                    self.streamer.dataOnFly.connect(self._addItemToTable)
                    self.streamer.start()
            except (TypeError): pass
            self.resourceFreeFlag = False # resources are occupied
        return
    
    def _resetPanelAction(self) -> None:
        '''Clears memory of the data structures and also removes the table and set the poster'''
        if(self.songDetailExhibiterTable.parent()):
            self.songDetailExhibiterTable.setParent(None)
            self.songDetailExhibiterTable.clearContents() # table data are removed
            self.songDetailExhibiterTable.setRowCount(0)
            self.searchEngine._cleanAllMemory() # all resources are free
            self.tableHolderLayout.addWidget(self.default_label, alignment = Qt.AlignmentFlag.AlignCenter)
            self.resourceFreeFlag = True # resouces are free
            self.default_label.show() # poster will be shown instead of table
        return
    pass


if __name__ == "__main__":
    # Application = QApplication(sys.argv)
    # StartingScreen = QPixmap(Constants.STARTING_SCREEN_PATH)
    # splashScreen = QSplashScreen(StartingScreen)
    # splashScreen.show()
    # time.sleep(Constants.STARTING_SCREEN_SHOW_TIME)
    # splashScreen.close()
    # music_Miner_Bot = MasterGrapicalUserInterface()
    # music_Miner_Bot.show()
    # Application.exec_()
    pass