# This thread class generate the QTableWidgetItems on the fly and them them as pyqt Signals
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from pagalFreeSiteExplorer import PagalFreeSiteExplorer
import  Constants

class TableDataStreamer(QThread):
    dataOnFly = pyqtSignal(int, str, str, str, QPixmap) # sends singal to the main thread so that objects can be passed on
    def __init__(self, searchInput : str):
        self.engine = PagalFreeSiteExplorer() # this engine scrape out the song from the web site
        self.searchInput = searchInput # ionput from the user interface
        super().__init__()
        return
    
    def run(self):
        '''For each data entry run method sends a singal to the UI and the UI takes this as input and show in the tablej'''
        self.engine.searchQuery = self.searchInput
        output = self.engine.dataExtractFromSearchQuery(self.engine.searchInWebsite())
        if(output):
            items = len(output[Constants.SONG_NAME])
            for i in range(items):
                songName = output[Constants.SONG_NAME][i]
                singerName = output[Constants.SINGER_NAME][i]
                posterImage = self.engine.loadImagesFromLink(output[Constants.LINK_TO_TUNE_POSTER_CONTAINER][i])
                href = output[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER]
                self.dataOnFly.emit(i, songName, singerName, href[i], posterImage) # sends data to the UI
        return
    pass