# This thread class generate the QTableWidgetItems on the fly and them them as pyqt Signals
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

from pagalFreeSiteExplorer import PagalFreeSiteExplorer
import  Constants

class TableDataStreamer(QThread):
    dataOnFly = pyqtSignal(int, str, str, str, QPixmap) # sends singal to the main thread so that objects can be passed on
    def __init__(self):
        self.engine = PagalFreeSiteExplorer() # this engine scrape out the song from the web site
        self._controlSignalDeclaration()
        self._properties()
        super().__init__()
        return
    
    def run(self):
        self.getResults()
        return
    
    def _controlSignalDeclaration(self) -> None:
        self.SEARCH_BY_SINGER = "Search By Singer"
        self.FILTER_HIGH_QUALITY = "Filter High Quality"
        self.FILTER_LOW_QUALITY = "Filter Low Quality"
        return

    def getInputs(self, searchInput : str, controlSignals : dict) -> None:
        '''Asks for search Input and other control signals so that it can Search Song Efficiently
            Control Signals ---->
            "Search By Singer" : boolean,
            "Filter High Quality" : boolean,
            "Filter Low Quality" : boolean
        '''
        self.searchInput = searchInput  # ionput from the user interface
        self.controlInputs  = controlSignals # control signals will specify how to extract data
        return

    def _properties(self) -> None:
        '''Instantiate all the necessary variables and Data strucutures at once'''
        self.DOES_DATA_EXISTS: bool = False # if it's true that means no need to extract data from the first only filtering should be done
        self.output_object : dict = None # The output Given by Engine Will be Given here
        return

    def releaseResources(self) -> None:
        '''Call this method to Reset all the data structures in there Initial state ready for next search'''
        self.DOES_DATA_EXISTS = False
        self.output_object = None
        self.engine._cleanAllMemory()
        return
    
    def emitData(self, index : int, songName : str, singerName : str, imageLink : str, href : str):
        posterImage = self.engine.loadImagesFromLink(imageLink)
        self.dataOnFly.emit(index, songName, singerName, href, posterImage) # sends data to the UI
        return

    def getResults(self) -> None:
        '''For each data entry run method sends a singal to the UI and the UI takes this as input and show in the table'''
        if(not self.DOES_DATA_EXISTS):
            self.engine.searchQuery = self.searchInput
            self.output_object = None
            self.output_object = self.engine.dataExtractFromSearchQuery(self.engine.searchInWebsite())
            self.DOES_DATA_EXISTS = True # now data exit's no need to read again
        if(self.output_object):
            items = len(self.output_object[Constants.SONG_NAME])
            index = 0
            # Only Filters High Quality Song
            if(self.controlInputs[self.FILTER_HIGH_QUALITY] and self.controlInputs[self.FILTER_LOW_QUALITY] == False):
                for i in range(items):
                    if(Constants.KBPS_320 in str(self.output_object[Constants.SONG_NAME][i])):
                        self.emitData(
                            index, self.output_object[Constants.SONG_NAME][i], self.output_object[Constants.SINGER_NAME][i],
                            self.output_object[Constants.LINK_TO_TUNE_POSTER_CONTAINER][i],
                            self.output_object[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER][i]
                        )
                        index += 1
            
            # only Filters Low Quality Song
            elif(self.controlInputs[self.FILTER_LOW_QUALITY] and self.controlInputs[self.FILTER_HIGH_QUALITY] == False):
                for i in range(items):
                    if(Constants.KBPS_128 in str(self.output_object[Constants.SONG_NAME][i])):
                        self.emitData(
                            index, self.output_object[Constants.SONG_NAME][i], self.output_object[Constants.SINGER_NAME][i],
                            self.output_object[Constants.LINK_TO_TUNE_POSTER_CONTAINER][i],
                            self.output_object[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER][i]
                        )
                        index += 1
            
            # Shows All the song
            else:
                for i in range(items):
                    self.emitData(
                        i, self.output_object[Constants.SONG_NAME][i], self.output_object[Constants.SINGER_NAME][i],
                        self.output_object[Constants.LINK_TO_TUNE_POSTER_CONTAINER][i],
                        self.output_object[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER][i]
                    )
        else: return
    pass