# this file is mainly responsible for creating the Graphical user inerface of the software using pyqt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QScrollArea, QTableWidget, QAbstractItemView
from PyQt5.QtCore import Qt
import sys
# custom import
import Constants

class MasterGrapicalUserInterface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(Constants.SOFTWARE_TITLE)
        self.setFixedSize(Constants.SOFTWARE_WIDTH, Constants.SOFTWARE_HEIGHT)
        self._initializeUI()
        self._constuctUI()
        self._addAttributes()
        return

    def _initializeUI(self) -> None:
        '''this function must be called inside the  constructor so that when the class is called all the uI components get's loaded in the window'''
        self._buildFrames()
        self._buildScrollArea()
        self._buildLayouts()
        self._buildButtons()
        self._buildLineInput()
        self._buildTableWidget()
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
        
        self.masterLayoutInnerFrame = QFrame()
        self.masterLayoutInnerFrame.setFixedSize(Constants.SOFTWARE_WIDTH - 20, Constants.SOFTWARE_HEIGHT - 20)
        self.masterLayoutInnerFrame.setFrameShape(QFrame.Shape.WinPanel)
        
        self.searchSectionLayoutFrame = QFrame()
        self.searchSectionLayoutFrame.setFixedSize(Constants.SEARCH_SECTION_WIDTH, Constants.SEARCH_SECTION_HEIGHT)
        self.searchSectionLayoutFrame.setFrameShape(QFrame.Shape.WinPanel)

        self.controlSectionLayoutFrame = QFrame()
        self.controlSectionLayoutFrame.setFixedSize(Constants.CONTROL_SECTION_WIDTH, Constants.CONTROL_SECTION_HEIGHT)
        self.controlSectionLayoutFrame.setFrameShape(QFrame.Shape.WinPanel)
        self.separator_one = QFrame()
        self.separator_one.setFrameShape(QFrame.Shape.HLine)
        self.separator_two = QFrame()
        self.separator_two.setFrameShape(QFrame.Shape.HLine)
        self.separator_three = QFrame()
        self.separator_three.setFrameShape(QFrame.Shape.HLine)

        self.viewPanelLayoutFrame = QFrame()
        self.viewPanelLayoutFrame.setFixedSize(Constants.VIEW_PANEL_WIDTH, Constants.VIEW_PANEL_HEIGHT)
        self.viewPanelLayoutFrame.setFrameShape(QFrame.Shape.WinPanel)
        return
    
    def _buildScrollArea(self) -> None:
        self.tableScrollArea = QScrollArea()
        # self.tableScrollArea.setWindowOpacity(0.0)
        self.tableScrollArea.setWidgetResizable(True)
        self.tableScrollArea.setFixedSize(Constants.VIEW_PANEL_WIDTH -20, Constants.VIEW_PANEL_HEIGHT - 20)
        self.tableScrollArea.setStyleSheet("background-color: rgba(255, 255, 255, 10);")
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
        width, height = self.tableScrollArea.width()- 20, self.tableScrollArea.height()- 20
        self.songDetailExhibiterTable = QTableWidget()
        self.songDetailExhibiterTable.setFixedSize(width, height)
        self.songDetailExhibiterTable.setColumnCount(4)
        self.songDetailExhibiterTable.setColumnWidth(0, Constants.THUMBNAIL_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(1,Constants.SONG_NAME_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(2,Constants.SINGER_NAME_SIZE)
        self.songDetailExhibiterTable.setColumnWidth(3, Constants.DOWNLOAD_URL_SIZE)
        self.songDetailExhibiterTable.setHorizontalHeaderLabels(
            [Constants.THUMBNAIL, Constants.SONG_NAME, Constants.SINGER_NAME, Constants.DOWNLOAD_URL]
        )
        self.songDetailExhibiterTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        return

    def _buildButtons(self) -> None:
        # search Related
        self.searchButton = QPushButton(Constants.SEARCH_BUTTON)
        self.searchBySingerButton = QPushButton(Constants.SEARCH_BY_SINGER_BUTTON)

        # Control Related
        self.BackGroundbutton = QPushButton(Constants.CHANGE_BACKGROUND)
        self.BackGroundbutton.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        
        self.setDownloadDirectory = QPushButton(Constants.SET_DOWNLOAD_DIRECTORY)
        self.setDownloadDirectory.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        
        self.HighQualityEnableButton = QPushButton(Constants.SHOW_HIGH_QUALITY)
        self.HighQualityEnableButton.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        self.HighQualityEnableButton.setCheckable(True)
        
        self.lowQualityEnableButton = QPushButton(Constants.SHOW_LOW_QUALITY)
        self.lowQualityEnableButton.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        self.lowQualityEnableButton.setCheckable(True)
        
        self.showDownloadingHistory = QPushButton(Constants.SHOW_DOWNLOAD_HISTORY)
        self.showDownloadingHistory.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        
        self.deleteDownlaodingHistory = QPushButton(Constants.DELETE_DOWNLOAD_HISTORY)
        self.deleteDownlaodingHistory.setFixedSize(Constants.CONTROL_SECTION_WIDTH - 20, 40)
        return
    
    def _buildLineInput(self) -> None:
        self.inputField = QLineEdit(Constants.SEARCH_HERE)
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

        # View panel
        return
    pass


if __name__ == "__main__":
    Application = QApplication(sys.argv)
    music_Miner_Bot = MasterGrapicalUserInterface()
    music_Miner_Bot.show()
    Application.exec_()