# Using this file the selected song will be downloaded in the system

from PyQt5.QtCore import QThread, pyqtSignal
import os
from icecream import ic

# custom imports
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
import Constants

class TuneDownloaderThread(QThread):
    messageSignal = pyqtSignal(str) # sends message to the main UI
    threadFinishedSignal = pyqtSignal(bool)  # Returns true if the thread action is finished
    currentlyDownloadedSongName = pyqtSignal(str) # after downloading the song the name of the song is returned

    # Constructor
    def __init__(self):
        self.engine = PagalFreeSiteExplorer() # this engine will download song

        # user given information
        self.downloadingDirectory = None
        self.songName = None
        self.url = None

        super().__init__()
        return

    def getInstructions(self, downloadingDirectory : str, songName : str, url : str) -> None:
        """Should be run before start method so that these parameters can be used by the run method"""
        self.downloadingDirectory = downloadingDirectory
        self.songName = songName
        self.url = url
        return

    def run(self):
        if os.path.exists(self.downloadingDirectory) and os.path.isdir(self.downloadingDirectory):
            downloadingIndex = 0 # default value is set to 0 and low quality song will be downloaded
            if Constants.KBPS_128 in self.songName: downloadingIndex = 0 # 128 Kbps
            if Constants.KBPS_320 in self.songName: downloadingIndex = 1 # 320 kbps

            if self.engine.downloadSongFromLink(self.url, self.songName, self.downloadingDirectory, downloadingIndex):
                self.threadFinishedSignal.emit(True) # Thread Finished successfully
                self.currentlyDownloadedSongName.emit(self.songName) # returning Song name to save in memory
                return
            else:
                self.messageSignal.emit(Constants.DOWNLOAD_FAILED) #internal error
                return
        else:
            self.messageSignal.emit(Constants.INVALID_DIRECTORY) # downloading directory doesn't exist
        return
    
    def cleanMemory(self):
        """nullify all the Variables after the thread is finished"""
        self.downloadingDirectory = None
        self.songName = None
        self.url = None
        return
    pass
