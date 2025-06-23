# the application will start from here
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import sys, os

# custom import
from masterGraphicalInterface import MasterGraphicalUserInterface
import Constants

def endScreen(splash : QSplashScreen, window : MasterGraphicalUserInterface):
    splash.finish(window)
    window.show()
    return

def generateSourceDirectories() -> None:
    """Creates Necessary folder if not exists"""
    try:
        tempPath = os.path.join(os.getcwd(), Constants.TEMP_PATH).replace("\\", "/")
        database_folder_location = os.path.join(os.getcwd(), Constants.DATA_BASE_FOLDER_LOCATION).replace(
            "\\", "/"
        )
        dummy_folder_location = os.path.join(os.getcwd(), Constants.DUMMY_RESOURCE_FOLDER).replace(
            "\\", "/"
        )
        if not os.path.exists(tempPath): os.mkdir(tempPath)
        if not os.path.exists(database_folder_location): os.mkdir(database_folder_location)
        if not os.path.exists(dummy_folder_location): os.mkdir(dummy_folder_location)
    except OSError: pass
    return

if __name__ == "__main__":
    generateSourceDirectories()
    Application = QApplication(sys.argv)
    StartingScreen = QPixmap(Constants.STARTING_SCREEN_PATH)
    splashScreen = QSplashScreen(StartingScreen)
    splashScreen.show()
    music_Miner_Bot = MasterGraphicalUserInterface()
    QTimer.singleShot(Constants.STARTING_SCREEN_SHOW_TIME, lambda : endScreen(splashScreen, music_Miner_Bot))
    Application.exec_()