# Using this file the selected song will be downloaded in the system

from PyQt5.QtCore import QThread, pyqtSignal
import os
from icecream import ic

# custom imports
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
import Constants

class TuneDownloaderThread(QThread):
    messageSignal = pyqtSignal(str) # sends message to the main UI
    threadFinishedSignal = pyqtSignal(bool) # Returns true if the thread action is finished
    def __init__(self):
        self.engine = PagalFreeSiteExplorer() # this engine will download song
        super().__init__()

    def getInstructions(self, downloadingDirectory : str, songName : str, url : str) -> None:
        self.downloadingDirectory = downloadingDirectory
        self.songName = songName
        self.url = url
        return
    
    def run(self):
        if (os.path.exists(self.downloadingDirectory) and os.path.isdir(self.downloadingDirectory)):
            if self.engine.downloadSongFromLink(self.url, self.songName, self.downloadingDirectory, 1):
                self.messageSignal.emit(Constants.DOWNLOAD_SUCCEED)
            else: self.messageSignal.emit(Constants.DOWNLOAD_FAILED) # Download Fails for internal error
        else: self.messageSignal.emit(Constants.INVALID_DIRECTORY) # Current downloading directory doesn't exist
        self.threadFinishedSignal.emit(True)
        super().run()
    
    def cleanMemory(self):
        '''nullify all the Variables after the thread is finished'''
        self.downloadingDirectory = None
        self.songName = None
        self.url = None
        return
    pass
