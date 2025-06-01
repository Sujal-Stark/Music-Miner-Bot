# the application will start from here
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
import time, sys

# custom import
from masterGraphicalInterface import MasterGraphicalUserInterface
import Constants

def endScreen(splash : QSplashScreen, window : MasterGraphicalUserInterface):
    splash.finish(window)
    window.show()
    return

if __name__ == "__main__":
    Application = QApplication(sys.argv)
    StartingScreen = QPixmap(Constants.STARTING_SCREEN_PATH)
    splashScreen = QSplashScreen(StartingScreen)
    splashScreen.show()
    music_Miner_Bot = MasterGraphicalUserInterface()
    QTimer.singleShot(Constants.STARTING_SCREEN_SHOW_TIME, lambda : endScreen(splashScreen, music_Miner_Bot))
    Application.exec_()