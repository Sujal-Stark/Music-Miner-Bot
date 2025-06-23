import os

from PyQt5.QtWidgets import (QDialog, QApplication, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QScrollArea,
QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QFile, QIODevice
from PyQt5. QtGui import QFont, QIcon
from datetime import  date
import sqlite3
from sqlite3 import DatabaseError, OperationalError, ProgrammingError, InterfaceError

import Constants

class DataBaseManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Constants.DB_MANAGER_WINDOW_TITLE)
        self.setFixedSize(Constants.DB_MANAGER_WINDOW_WIDTH, Constants.DB_MANAGER_WINDOW_HEIGHT)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)
        self.setWindowIcon(QIcon(Constants.ICON_PATH))
        self.setModal(True)

        self._createProperties()
        self._createUIElements()
        self._constructUI()
        self._addAttributes()

        self._createDataBase()
        self._createTableInDataBase()

        self._loadStyleSheet()
        return

    def _createProperties(self) -> None:
        """
            All Properties related to class which are confidential are created here
            :return: None
        """
        self.DATABASE_FILE_LOCATION = os.getcwd().replace("\\", "/") + "/Databases/historyDataBases.db"
        self.connection : sqlite3.Connection = None # connection to the database But initially referring to NULL
        self.dbCursor : sqlite3.Connection.cursor = None # cursor to the database
        self.TABLE_NAME = "History"
        self.COL_SERIAL = "serial"
        self.COL_SONG_NAME = "SongName"
        self.COL_DATE = "Date_of_Download"
        return None

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
        self.table.setHorizontalHeaderLabels([Constants.DB_TABLE_SONG_NAME, Constants.DB_TABLE_DATE])
        self.table.setColumnWidth(0, 360)
        self.table.setColumnWidth(1, 150)
        self.table.setRowCount(0)
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
            file = QFile(os.path.join(os.getcwd(), Constants.DB_UI_QSS_PATH))
            if file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                qss = file.readAll().data().decode(Constants.PARSER_KEY)
                self.setStyleSheet(qss)
        except (OSError, MemoryError, PermissionError, FileNotFoundError): return # handles loading error

    ###################################### INTERFACING ###############################################
    def _createDataBase(self) -> None:
        """
            Creates a Database File named "historyDataBases" if not exists and creates a connection to the file
            :return: None
        """
        try:
            self.connection = sqlite3.connect(self.DATABASE_FILE_LOCATION)
            self.dbCursor = self.connection.cursor()
        except(DatabaseError, OperationalError, PermissionError):
            print("Unable to Create Database")
        return

    def _createTableInDataBase(self) -> None:
        """
            Creates a Table inside the "historyDataBases.db" file.
            Table will have 1. serial Number, 2. SongName, 3. Date Of Download this 3 fields
            IF the table all ready exists it do nothing
            :return:None
        """
        try:
            if self.connection:
                self.dbCursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME}(" +
                        f"{self.COL_SERIAL} INTEGER PRIMARY KEY AUTOINCREMENT," +
                        f"{self.COL_SONG_NAME} TEXT," +
                        f"{self.COL_DATE} TEXT" +
                    ")"
                )
            else:
                print("Data base doesn't exist")
        except(ProgrammingError, InterfaceError, OperationalError, DatabaseError):
            print("Unable to create tables")
        return None

    def insertIntoTable(self, songName : str) -> None:
        """
            Takes the input songName, and put it into the Table with Primary Key as Serial Number
             and Date of download
            :param songName: String Argument
            :return: None
        """
        try:
            if self.connection:
                self.dbCursor.execute(
                    f"INSERT INTO {self.TABLE_NAME}({self.COL_SONG_NAME}, {self.COL_DATE})" +
                    f"VALUES('{songName}', '{date.today()}')"
                )
                self.connection.commit()
            else:
                print("Connection is not established")
        except(OperationalError, DatabaseError, ProgrammingError, InterfaceError):
            print("Unable to insert Data")
        return None

    def displayData(self) -> None:
        """
            Populates the Table using Data from database
            :return: None
        """
        try:
            if self.connection:
                self.dbCursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME}"
                )
                rows : list = self.dbCursor.fetchall()
                self.table.setRowCount(len(rows))
                for rowIndex in range(len(rows)):
                    self.table.setItem(rowIndex, 0, QTableWidgetItem(rows[rowIndex][1]))
                    self.table.setItem(rowIndex, 1, QTableWidgetItem(rows[rowIndex][2]))
            else:
                print("Connection is not established")
        except(OperationalError, DatabaseError, ProgrammingError, InterfaceError):
            print("Unable to read data")
        return None

    def truncateTableFromDataBase(self) -> None:
        """
            If the table exists this Method will truncate that table
            :return: None
        """
        try:
            if self.connection:
                self.dbCursor.execute(
                    f"DELETE FROM {self.TABLE_NAME}"
                )
                self.connection.commit()
            else:
                print("Database doesn't exists")
        except(ProgrammingError, InterfaceError, OperationalError, DatabaseError):
            print("Unable to Remove data")
        return None

    def close(self):
        self.table.setRowCount(0) # Clears The Table
        return super().close()
    pass


if __name__ == '__main__':
    app = QApplication([])
    window = DataBaseManager()
    window.show()
    app.exec_()
    pass