from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QScrollArea, QTableWidget
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5. QtGui import QFont

import Constants

class DataBaseManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Constants.DB_MANAGER_WINDOW_TITLE)
        self.setFixedSize(Constants.DB_MANAGER_WINDOW_WIDTH, Constants.DB_MANAGER_WINDOW_HEIGHT)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.setModal(True)

        self._createUIElements()
        self._constructUI()
        self._addAttributes()
        self._loadStyleSheet()
        return

    def _createUIElements(self) -> None:
        """
            Creates all the UI Elements all together
            :return: None
        """
        self._buildLayouts()
        self._buildFrames()
        self._buildScrollArea()
        self._buildTableWidget()
        self._buildLabels()
        return

    def _buildLayouts(self) -> None:
        self.innerMasterLayout = QVBoxLayout()

        self.titleLayout = QHBoxLayout()

        self.bodyLayout = QVBoxLayout()
        return

    def _buildFrames(self) -> None:
        self.masterLayoutFrame = QFrame()
        self.masterLayoutFrame.setObjectName(Constants.DB_MAIN_FRAME_OBJECT_NAME)
        self.masterLayoutFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.masterLayoutFrame.setFixedSize(Constants.DB_MAIN_FRAME_WIDTH, Constants.DB_MAIN_FRAME_HEIGHT)
        return

    def _buildScrollArea(self) -> None:
        self.historyScrollArea = QScrollArea()
        self.historyScrollArea.setWidgetResizable(True)
        self.historyScrollArea.setObjectName(Constants.DB_SCROLL_AREA_OBJECT_NAME)
        self.historyScrollArea.setFixedSize(
            Constants.DB_BODY_LAYOUT_SCROLL_AREA_WIDTH, Constants.DB_BODY_LAYOUT_SCROLL_AREA_HEIGHT
        )
        self.historyScrollArea.setStyleSheet("QScrollBar{height:0px; width:0px;}")
        return

    def _buildTableWidget(self) -> None:
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            [Constants.DB_TABLE_SL, Constants.DB_TABLE_SONG_NAME, Constants.DB_TABLE_DATE]
        )
        self.table.setColumnWidth(0, 20)
        self.table.setColumnWidth(1, 340)
        self.table.setColumnWidth(2, 128)
        self.table.setRowCount(25)
        return

    def _buildLabels(self) -> None:
        self.titleLabel = QLabel("Download History")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setFont(QFont("Georgia", 20))
        return

    def _constructUI(self) -> None:
        self.masterLayout.addWidget(self.masterLayoutFrame, Qt.AlignmentFlag.AlignCenter)
        self.masterLayoutFrame.setLayout(self.innerMasterLayout)

        self.innerMasterLayout.addLayout(self.titleLayout, stretch = 10)

        self.innerMasterLayout.addLayout(self.bodyLayout, 90)
        return

    def _addAttributes(self) -> None:
        self.titleLayout.addWidget(self.titleLabel, Qt.AlignmentFlag.AlignCenter)

        self.bodyLayout.addWidget(self.historyScrollArea, Qt.AlignmentFlag.AlignCenter)
        self.historyScrollArea.setWidget(self.table)
        return

    def _loadStyleSheet(self) -> None:
        """Should be called in the constructor, and it loads the style sheet from qml file"""
        try:
            file = QFile(Constants.DB_UI_QSS_PATH)
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error

    ###################################### INTERFACING ###############################################
    pass


if __name__ == '__main__':
    app = QApplication([])
    window = DataBaseManager()
    window.show()
    app.exec_()
    pass