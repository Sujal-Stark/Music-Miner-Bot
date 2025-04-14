from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFrame, QFileDialog, QPushButton, QLabel
from PyQt5.QtCore import Qt, QFile, QIODevice, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
import os
# Custom Imports
import Constants
from DummyWindow import DummyPreview

import sys
class SelectWallpaperUI(QDialog):
    fileSelectedSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.setWindowTitle(Constants.WALLPAPER_PREVIEW_TITLE)
        self.setFixedSize(Constants.WALLPAPER_PREVIEW_WIDTH, Constants.WALLPAPER_PREVIEW_HEIGHT)
        self.setWindowIcon(QIcon(Constants.ICON_PATH))
        self.masterLayout = QVBoxLayout(self)

        self._initializeUI()
        self._constructUI()
        self._addAttributes()
        self._loadStyleSheet()
        return
    
    def _initializeUI(self) -> None:
        '''Initialiss all the attributes and layouts used in this UI'''
        self._buildPreviewWallpaper()
        self._setProperties()
        self._buildLayouts()
        self._buildFrames()
        self._buildPushButtons()
        self._buildLabels()
        self._setResponses()
        return

    def  _setProperties(self) -> None:
        self.selectedFile_Name : str = None
        return

    def _setResponses(self) -> None:
        self.selectFromDevice.clicked.connect(self._setPreviewWithDeviceImage)
        self.useInApplication.clicked.connect(self._closeWindow)
        return

    def _buildPreviewWallpaper(self) -> None:
        self.previewUI = DummyPreview()
        return

    def _buildLayouts(self)-> None:
        '''Creates all the layouts used in this UI'''
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

    # INTERFACEING
    def _loadStyleSheet(self) -> None:
        '''Should be called in the constructor and it loads the style sheet from qml file'''
        try:
            file = QFile(Constants.WALLPAPER_PREVIEW_STYLE_PATH)
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # doesn't change anything if   file not found
        return
    
    def _generateWallpaperLabel(self, location : str = None):
        label = ClickableLabel()
        label.setFixedSize(100, 100)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if(location):
            label.setProperty(Constants.LOCATION_PROP, location)
            pixmap = QPixmap(location).scaled(label.size())
            label.setPixmap(pixmap)
        else: label.setText(Constants.UNABLE_TO_LOAD) 
        return label
    
    def _passWallpaperLocation(self, loc : str = None):
        if(loc):
            self.selectedFile_Name = loc
            self.previewUI.resizeGivenWallpaper(loc)
        return

    def _setPreviewWithDeviceImage(self) -> None:
        file_Name = QFileDialog.getOpenFileName(
            self, caption= Constants.SELECT_FROM_DEVICE, filter="Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if(file_Name and os.path.exists(file_Name[0])): 
            self.previewUI.resizeGivenWallpaper(file_Name[0])
            self.selectedFile_Name = file_Name[0]
        return
    
    def _closeWindow(self) -> str:
        if(self.selectedFile_Name): self.fileSelectedSignal.emit(self.selectedFile_Name)
        return self.close()
    pass

class ClickableLabel(QLabel):
    location_signal = pyqtSignal(str)
    
    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        if(ev.button() == Qt.MouseButton.LeftButton):
            self.location_signal.emit(self.property(Constants.LOCATION_PROP))
            return
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SelectWallpaperUI()
    window.show()
    app.exec_()
    pass