from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import  QPixmap, QFontMetrics
from PyQt5.QtCore import Qt, QFile, QIODevice, QTimer
import os
# custom Import
import Constants
from utility import Utility


class SongCard(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(Constants.SONG_CARD_WIDTH, Constants.SONG_CARD_HEIGHT)
        self.setObjectName("SongCard")
        self.master_Layout = QHBoxLayout()
        self.setLayout(self.master_Layout)
        self.index = 0
        self.timer_nameHolder = QTimer(self)
        self.timer_nameHolder.start(500) # to maintain marquee effect on name holder label
        self.timer_singerNameHolder = QTimer(self)
        self.timer_singerNameHolder.start(500) # to maintain marquee effect on singer name holder label

        self._initUi()
        self._constructUI()
        self._addAttributes()
        self._loadStyleSheet()
        return

    def _initUi(self) -> None:
        """
            All function calls related to defining new widgets are called here
            :return: None
        """
        self._buildLayouts()
        self._buildLabels()
        self._buildButtons()
        return

    def _buildLayouts(self) -> None:
        """
            All Layouts are built here
            :return: None
        """
        self.imageHolderLayout = QVBoxLayout()

        self.dataHolderLayout = QVBoxLayout()
        return

    def _buildLabels(self) -> None:
        """
            All Labels are built here
            :return: None
        """
        self.imageHolderLabel = QLabel("Image")
        self.imageHolderLabel.setObjectName("coverArt")
        self.imageHolderLabel.setAlignment(Qt.AlignCenter)

        self.nameHolderLabel = QLabel("Song name")
        self.nameHolderLabel.setObjectName("songTitle")
        self.nameHolderLabel.setFixedSize(Constants.SONG_CARD_NAME_LABEL_WIDTH, 40)
        self.nameHolderLabel.setStyleSheet(
            "font-size: 18px;"
        )

        self.singerHolderLabel = QLabel("SingerName")
        self.singerHolderLabel.setObjectName("artistName")
        self.singerHolderLabel.setFixedSize(Constants.SONG_CARD_NAME_LABEL_WIDTH, 30)
        self.singerHolderLabel.setStyleSheet(
            "font-size: 12px;"
        )
        return

    def _buildButtons(self) -> None:
        """
            All Buttons are built here
        :return: None
        """
        self.downloadButton = QPushButton()
        self.downloadButton.setObjectName("downloadBtn")
        self.downloadButton.setText(Constants.DOWNLOAD_BUTTON_TEXT)
        self.downloadButton.setFixedSize(150, 40)
        return

    def _constructUI(self) -> None:
        """
            Layouts and frames are bind together here
            :return: None
        """
        self.master_Layout.addLayout(self.imageHolderLayout, 25)

        self.master_Layout.addLayout(self.dataHolderLayout, 75)
        return

    def _addAttributes(self) -> None:
        """
            All widgets are bind with frames and layouts
            :return: None
        """
        self.imageHolderLayout.addWidget(self.imageHolderLabel, Qt.AlignmentFlag.AlignCenter)

        self.dataHolderLayout.addWidget(self.nameHolderLabel,40, Qt.AlignmentFlag.AlignLeft)
        self.dataHolderLayout.addWidget(self.singerHolderLabel, 20, Qt.AlignmentFlag.AlignLeft)
        self.dataHolderLayout.addWidget(self.downloadButton, 40, Qt.AlignmentFlag.AlignLeft)
        return

    def _loadStyleSheet(self) -> None:
        """Should be called in the constructor, and it loads the style sheet from qml file"""
        try:
            file = QFile(Utility.getResourcePath(Constants.SONG_CARD_QSS_LOCATION))
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error



    ############################################## INTERFACING #######################################################
    def set_data(self, songName : str, singerName : str, href : str):
        """
            Use these inputs as parametric values of each song card
            :param songName: (String)
            :param singerName: (Singer name)
            :param href: (String) Song Url
            :return: None
        """
        separator = "         "
        self.nameHolderLabel.setText(songName + separator) # song name
        if SongCard.willTextOverFlow(self.nameHolderLabel):
            self.timer_nameHolder.timeout.connect(lambda: self.scrollText(self.nameHolderLabel))

        self.singerHolderLabel.setText(singerName) # Singer name
        if SongCard.willTextOverFlow(self.singerHolderLabel):
            self.timer_singerNameHolder.timeout.connect(lambda: self.scrollText(self.singerHolderLabel))

        self.downloadButton.setProperty(Constants.HREF, href) # setting URL as property
        self.downloadButton.setProperty(Constants.SONG_NAME, songName) # setting song name as property
        return

    def setImageToCard(self, pixmap: QPixmap) -> None:
        """
            Use pixmap(Already Scaled) as poster of each song card
            :param pixmap: QPixmap object of the poster
            :return: None
        """
        self.imageHolderLabel.hide()
        self.imageHolderLabel.setPixmap(pixmap)
        self.imageHolderLabel.show()
        return

    @staticmethod
    def willTextOverFlow(label : QLabel) -> bool:
        """
            Checks if The text inside the label overflows or not
            :param label: Qlabel of this class
            :return: true if text overflows else false
        """
        font_metrics = QFontMetrics(label.font())
        return font_metrics.horizontalAdvance(label.text()) > Constants.SONG_CARD_NAME_LABEL_WIDTH

    def scrollText(self, label : QLabel) -> None:
        full_text = label.text()
        display_text = full_text[self.index:] + full_text[:self.index]
        label.setText(display_text)
        self.index = (self.index + 1) % len(full_text)
    pass

if __name__ == '__main__':
    pass