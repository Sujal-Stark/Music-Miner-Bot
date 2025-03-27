# Using this file the selected song will be downloaded in the system

from PyQt5.QtCore import QThread, pyqtSignal
import os

# custom imports
from pagalFreeSiteExplorer import PagalFreeSiteExplorer
import Constants

class TuneDownloaderThread(QThread):
    messageSignal = pyqtSignal(str) # sends message to the main UI
    def __init__(self, downloadingDirectory : str, songName : str, url : str):
        self.downloadingDirectory = downloadingDirectory
        self.songName = songName
        self.url = url
        self.engine = PagalFreeSiteExplorer() # this engine will download song
        super().__init__()

    def run(self):
        if (os.path.exists(self.downloadingDirectory) and os.path.isdir(self.downloadingDirectory)):
            if self.engine.downloadSongFromLink(self.url, self.songName, self.downloadingDirectory, 1):
                self.messageSignal.emit(Constants.DOWNLOAD_SUCCEED)
            else:
                self.messageSignal.emit(Constants.DOWNLOAD_FAILED)
        else:
            self.messageSignal.emit(Constants.INVALID_DIRECTORY)
        super().run()
    pass
