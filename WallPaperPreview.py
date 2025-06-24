import icecream
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFrame, QFileDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt, QFile, QIODevice, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import os
# Custom Imports
import Constants
from DummyWindow import DummyPreview

import sys

from utility import Utility


class SelectWallpaperUI(QDialog):
    # Signal Declaration
    fileSelectedSignal = pyqtSignal(str)
    wallpaperChangeAbortAction = pyqtSignal(bool)

    def __init__(self, wallpaper_location : str):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle(Constants.WALLPAPER_PREVIEW_TITLE)
        self.setFixedSize(Constants.WALLPAPER_PREVIEW_WIDTH, Constants.WALLPAPER_PREVIEW_HEIGHT)
        self.setWindowIcon(QIcon(Constants.ICON_PATH))
        self.masterLayout = QVBoxLayout(self)

        self.currentWallpaperLocationFromMainWindow(wallpaper_location) # The wallpaper user currently using

        self._setProperties()
        self._initializeUI()
        self._constructUI()
        self._addAttributes()
        self._loadStyleSheet()
        return

    # Overridden Methods
    def show(self):
        # show method is Overridden so that Each time this window is used the preview UI becomes ready again
        self.previewUI.show()
        return super().show()

    def closeEvent(self, a0):
        # Notify main application that this class is terminated
        self.wallpaperChangeAbortAction.emit(True) # sends true if the window is closed
        a0.accept()
        return

    # Setting parameters or getting values
    def  _setProperties(self) -> None:
        """
            All Class related parameters are generated here
            :return: None
        """
        self.selectedFile_Name : str = None
        return

    def currentWallpaperLocationFromMainWindow(self, location : str):
        """
            Takes location of user's currently using image and set this as class'es own parameter
            :param location: String [Valid Image location in system]
            :return: None
        """
        self.currentWallpaperLocation = location if os.path.exists(location) else Constants.DEFAULT_WALLPAPER_LOCATION
        return

    def _setResponses(self) -> None:
        """
            define response for the inputs given to the GUI of this class
            :return: None
        """
        self.selectFromDevice.clicked.connect(self._setPreviewWithDeviceImage)
        self.useInApplication.clicked.connect(self._closeWindow)
        return

    # Build UI
    def _initializeUI(self) -> None:
        """
            Initialise all the attributes and layouts used in this UI
            :return: None
        """
        self._buildPreviewWallpaper()
        self._buildLayouts()
        self._buildFrames()
        self._buildPushButtons()
        self._buildLabels()
        self._setResponses()
        return

    def _buildPreviewWallpaper(self) -> None:
        """
            Instantiate the Dummy window here
            :return: None
        """
        self.previewUI = DummyPreview()
        self.previewUI.getTestingWallpaperLocation(self.currentWallpaperLocation)
        return

    def _buildLayouts(self)-> None:
        """
            Creates all the layouts used in this UI
            :return: None
        """
        # main Layout
        self.innerMasterLayout = QVBoxLayout()

        # PreView
        self.previewLayout = QHBoxLayout()
        self.innerPreviewLayout = QVBoxLayout()

        # application wallpaper layout
        self.customWallpaperLayout = QVBoxLayout() # parent
        self.customWallpaper_LabelLayout = QHBoxLayout() # holds the label
        self.applicationWallpaperHolderLayout = QHBoxLayout() # holds wallpaper

        # File selection Section
        self.selectionLayout = QHBoxLayout() # parent
        self.selectionInnerLayout = QHBoxLayout() # actual holder
        return

    def _buildFrames(self) ->None:
        # main frame holds everything inside it
        self.mainFrame = QFrame()
        self.mainFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # Preview 
        self.previewFrame = QFrame()
        self.previewFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # application wallpaper section
        self.wallpaperHolderFrame = QFrame()
        self.wallpaperHolderFrame.setFrameShape(QFrame.Shape.StyledPanel)

        # File selection Section
        self.selectionFrame = QFrame()
        self.selectionFrame.setFrameShape(QFrame.Shape.StyledPanel)
        return

    def _buildLabels(self) -> None:
        # preview Section
        self.previewLabel = QLabel(Constants.SCREEN_PREVIEW)
        self.previewLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # custom wallpaper section
        self.customWallpapers = QLabel(Constants.CUSTOM_WALLPAPER)
        self.customWallpapers.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.customWallpapers.setStyleSheet("QLabel{color : #ffffff}")

        # custom wallpaper Labels
        self.wallpaper_arora : ClickableLabel = self._generateWallpaperLabel(Constants.WALLPAPER_ARORA)
        self.wallpaper_arora.location_signal.connect(self._passWallpaperLocation)
        self.wallpaper_black_hole : ClickableLabel = self._generateWallpaperLabel(Constants.WALLPAPER_BLACK_HOLE)
        self.wallpaper_black_hole.location_signal.connect(self._passWallpaperLocation)
        self.desert_wallpaper_label = self._generateWallpaperLabel(Constants.WALLPAPER_DESERT)
        self.desert_wallpaper_label.location_signal.connect(self._passWallpaperLocation)
        self.dragon_wallpaper_label = self._generateWallpaperLabel(Constants.WALLPAPER_DRAGON)
        self.dragon_wallpaper_label.location_signal.connect(self._passWallpaperLocation)
        self.planet_wallpaper_label = self._generateWallpaperLabel(Constants.WALLPAPER_PLANET)
        self.planet_wallpaper_label.location_signal.connect(self._passWallpaperLocation)
        return

    def _buildPushButtons(self) -> None:
        self.useInApplication = QPushButton(Constants.USE)
        self.useInApplication.setFixedSize(Constants.WALLPAPER_PREVIEW_BUTTON_WIDTH, Constants.WALLPAPER_PREVIEW_BUTTON_HEIGHT)

        self.selectFromDevice = QPushButton(Constants.SELECT_FROM_DEVICE)
        self.selectFromDevice.setFixedSize(Constants.WALLPAPER_PREVIEW_BUTTON_WIDTH, Constants.WALLPAPER_PREVIEW_BUTTON_HEIGHT)
        return

    def _constructUI(self) -> None:
        # Initializing main layout
        self.masterLayout.addWidget(self.mainFrame, alignment = Qt.AlignmentFlag.AlignCenter)
        self.mainFrame.setLayout(self.innerMasterLayout)

        # Preview
        self.innerMasterLayout.addLayout(self.previewLayout)
        self.previewLayout.addWidget(self.previewFrame, alignment = Qt.AlignmentFlag.AlignHCenter)
        self.previewFrame.setLayout(self.innerPreviewLayout)

        # custom wallpaper section
        self.innerMasterLayout.addLayout(self.customWallpaperLayout)
        self.customWallpaperLayout.addLayout(self.customWallpaper_LabelLayout, stretch = 10)
        self.customWallpaperLayout.addWidget(self.wallpaperHolderFrame, stretch = 90, alignment = Qt.AlignmentFlag.AlignCenter)
        self.wallpaperHolderFrame.setLayout(self.applicationWallpaperHolderLayout)

        # selection panel
        self.innerMasterLayout.addLayout(self.selectionLayout)
        self.selectionLayout.addWidget(self.selectionFrame)
        self.selectionFrame.setLayout(self.selectionInnerLayout)
        return

    def _addAttributes(self) -> None:
        # Preview 
        self.innerPreviewLayout.addWidget(self.previewLabel, stretch = 10, alignment = Qt.AlignmentFlag.AlignCenter)
        self.innerPreviewLayout.addWidget(self.previewUI, stretch = 90, alignment = Qt.AlignmentFlag.AlignCenter)

        # custom wallpaper section
        self.customWallpaper_LabelLayout.addWidget(self.customWallpapers, alignment = Qt.AlignmentFlag.AlignTop)
        self.applicationWallpaperHolderLayout.addWidget(self.wallpaper_arora, alignment = Qt.AlignmentFlag.AlignCenter)
        self.applicationWallpaperHolderLayout.addWidget(self.wallpaper_black_hole, alignment = Qt.AlignmentFlag.AlignCenter)
        self.applicationWallpaperHolderLayout.addWidget(self.desert_wallpaper_label, alignment = Qt.AlignmentFlag.AlignCenter)
        self.applicationWallpaperHolderLayout.addWidget(self.dragon_wallpaper_label, alignment = Qt.AlignmentFlag.AlignCenter)
        self.applicationWallpaperHolderLayout.addWidget(self.planet_wallpaper_label, alignment = Qt.AlignmentFlag.AlignCenter)

        # Selection section
        self.selectionInnerLayout.addWidget(self.useInApplication, alignment = Qt.AlignmentFlag.AlignLeft)
        self.selectionInnerLayout.addWidget(self.selectFromDevice, alignment = Qt.AlignmentFlag.AlignRight)
        return

    def _loadStyleSheet(self) -> None:
        """
            Read the QML file and load the style for this window
            :return: None
        """
        try:
            file = QFile(Utility.getResourcePath(Constants.WALLPAPER_PREVIEW_STYLE_PATH))
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # doesn't change anything if file not found
        return


    ########################################## INTERFACING ########################################################
    # Wallpaper related
    @staticmethod
    def _generateWallpaperLabel(location : str = None):
        """
            Creates a Label that holds wallpaper location in static folder and when clicked it sends the wallpaper
            location as pyqt signal
            :param location: String [valid Image location]
            :return: ClickableLabel
        """
        label = ClickableLabel() # instantiate
        label.setFixedSize(100, 100) # size
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if location: # if location is correct
            label.setProperty(Constants.LOCATION_PROP, location)
            pixmap = QPixmap(location).scaled(label.size())
            label.setPixmap(pixmap)
        else: label.setText(Constants.UNABLE_TO_LOAD) # No image will be loaded
        return label

    def _passWallpaperLocation(self, loc : str = None):
        """
            with the given image location path this method set the  wallpaper of dummy window
            :param loc: String [valid Image location]
            :return: None
        """
        if loc:
            self.selectedFile_Name = loc # to send the chosen wallpaper to main window
            self.previewUI.getTestingWallpaperLocation(self.selectedFile_Name)
            self.previewUI.setWallpaper()
        return

    def _setPreviewWithDeviceImage(self) -> None:
        """
            Takes Image location from device and use as wallpaper in dummy window
            :return: None
        """
        file_Name = QFileDialog.getOpenFileName(
            self, caption= Constants.SELECT_FROM_DEVICE, filter="Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        ) # image location from file
        if file_Name and os.path.exists(file_Name[0]):
            self.previewUI.getTestingWallpaperLocation(file_Name[0]) # sent new Location to PreviewUI
            self.previewUI.setWallpaper() # wallpaper is set in previewUI
            self.selectedFile_Name = file_Name[0] # new location is ready to set
        return

    #GUI related
    def _closeWindow(self) -> bool:
        """
            Closes this window send the selected file name to the application and remove everything from
            DummyResourceFolder
            :return: None
        """
        if self.selectedFile_Name: self.fileSelectedSignal.emit(self.selectedFile_Name)
        self.previewUI.clearDummyResourceFolder()
        self.previewUI.close()
        return self.close()
    pass

class ClickableLabel(QLabel):
    #PyQt Signal
    location_signal = pyqtSignal(str)
    
    def mousePressEvent(self, ev):
        """
            When this label is clicked it sends the location of the Image which is assigned to it as property
            :param ev: Event like click event
            :return: None
        """
        super().mousePressEvent(ev)
        if ev.button() == Qt.MouseButton.LeftButton:
            self.location_signal.emit(self.property(Constants.LOCATION_PROP))
            return
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SelectWallpaperUI()
    window.show()
    app.exec_()
    pass