# this file is mainly responsible for creating the Graphical user inerface of the software using pyqt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLineEdit, QLabel
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
        self._buildLayouts()
        self._buildButtons()
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

        self.viewPanelLayoutFrame = QFrame()
        self.viewPanelLayoutFrame.setFixedSize(Constants.VIEW_PANEL_WIDTH, Constants.VIEW_PANEL_HEIGHT)
        self.viewPanelLayoutFrame.setFrameShape(QFrame.Shape.WinPanel)
        return
    
    def _buildLayouts(self) -> None:
        '''Must be called inside _initializeUI method. it is used to build the Layouts'''
        self.masterLayout = QVBoxLayout()
        self.bodyLayout = QVBoxLayout()
        self.searchSectionLayout = QHBoxLayout()
        self.searchSectionLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.actionLayout = QHBoxLayout()
        self.controlSectionLayout = QVBoxLayout()
        self.controlSectionLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewPanelLayout = QHBoxLayout()
        self.viewPanelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return
    
    def _buildButtons(self) -> None:
        self.searchButton = QPushButton(Constants.SEARCH_BUTTON)
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

        #ACTION SECTION
        self.bodyLayout.addLayout(self.actionLayout)

        #CONTROL PANEL
        self.actionLayout.addLayout(self.controlSectionLayout)
        self.controlSectionLayout.addWidget(self.controlSectionLayoutFrame, Qt.AlignmentFlag.AlignCenter)

        #VIEW PANEL
        self.actionLayout.addLayout(self.viewPanelLayout)
        self.viewPanelLayout.addWidget(self.viewPanelLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        return
    
    def _addAttributes(self):
        # self.searchSectionLayout.addWidget(self.searchButton, alignment = Qt.AlignmentFlag.AlignLeft)
        return
    pass


if __name__ == "__main__":
    Application = QApplication(sys.argv)
    music_Miner_Bot = MasterGrapicalUserInterface()
    music_Miner_Bot.show()
    Application.exec_()