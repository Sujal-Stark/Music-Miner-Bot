# the application will start from here
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
import time, sys

# custom import
from masterGraphicalInterface import MasterGrapicalUserInterface
import Constants
if __name__ == "__main__":
    Application = QApplication(sys.argv)
    StartingScreen = QPixmap(Constants.STARTING_SCREEN_PATH)
    splashScreen = QSplashScreen(StartingScreen)
    splashScreen.show()
    time.sleep(Constants.STARTING_SCREEN_SHOW_TIME)
    music_Miner_Bot = MasterGrapicalUserInterface()
    music_Miner_Bot.show()
    Application.exec_()