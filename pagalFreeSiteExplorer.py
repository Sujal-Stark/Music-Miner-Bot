# this file is responsible for navigating in pagalFreeWebsite, search song, getting links and downloading all the songs and other related operations

import requests
from bs4 import BeautifulSoup, element
from PyQt5.QtGui import QImage
from PIL import Image
from io import BytesIO
from icecream import ic

# custom imports
import Constants

class PagalFreeSiteExplorer:
    def __init__(self):
        self._setProperties()
        pass

    # declare properties
    def _setProperties(self) -> None:
        '''this method is called internally while initialising the class object to instantiate necessary data structures and variable or objects'''
        self.BASE = Constants.PAGALFREESITEURL # base url for pagalfree website
        self.searchQuery : str = None # the name of the song shall be stored here, input given by user
        self.soup : BeautifulSoup = None # soup content
        self.songDataContainer = {
            Constants.LINK_TO_REDIRECT_TUNE_CONTAINER : [], # contains the link of the song
            Constants.LINK_TO_TUNE_POSTER_CONTAINER : [], # stores the link of the poster
            Constants.SONG_NAME : [], # stores the name of actual songs
            Constants.SINGER_NAME : [] # The singer name is being stored here
        }
        self.downloadableLinks : list[str] = None # actual links to download songs is stored here, none to abort
        self.resourceOccupiedFlag : bool = False # denotes if the resources are free or not
        return None
    
    def getParameterFromUser(self, textInput : str) -> None:
        '''Take input from user as string  format and store it in self.searchQuery field'''
        self.searchQuery = textInput.replace(" ", Constants.SEARCH_DELIMITER)
        return None
    
    def searchForSinger(self, textInput : str) -> list[str]:
        '''takes string input from the user and returns the dictionary of list
            data format => dict {[contains link of downlaod page], [song name], [url to the poster]}
        '''
        textInput = textInput.replace(" ", Constants.SEARCH_DELIMITER)
        searchResponse = requests.get(self.BASE + Constants.SEARCH_END_POINT + textInput)
        if(searchResponse.status_code == Constants.STATUSCODE_SUCCEED):
            self.soup = BeautifulSoup(searchResponse.content.decode(Constants.PARSER_KEY), Constants.HTML_PARSER)
            return self.dataExtractFromSearchQuery(self.soup.find_all(Constants.DIV, id = Constants.ID_CATAGORY_CONTENT))
        else:
            return [Constants.NOT_FOUND_MESSAGE]

    # search the query in the website if found then returns the list of the elements
    def searchInWebsite(self) -> list[element.Tag]:
        '''searches the user query in the website and returns a web element list.
            should be used as a argument for self.dataExtractFromSearchQuery()
        '''
        searchRequest = requests.get(self.BASE + Constants.SEARCH_END_POINT + self.searchQuery)
        if (searchRequest.status_code == Constants.STATUSCODE_SUCCEED):
            self.soup = BeautifulSoup(
                searchRequest.content.decode(Constants.PARSER_KEY), Constants.HTML_PARSER
            )
            return self.soup.find_all(Constants.DIV, id = Constants.ID_CATAGORY_CONTENT)
        else:
            return [Constants.NOT_FOUND_MESSAGE]
    
    # separates search query elemnts and sent them in a dictionary form
    def dataExtractFromSearchQuery(self, dataElement : list[element.Tag]) -> dict:
        '''Takes self.searchInWebsite() as input and provides a dictionary as output
            output format => dict {[link to download page], [song name], [singer name]. [url to the poster]}
        '''
        if(self.resourceOccupiedFlag == False): # if resources are not previously occupied only then extract data
            for el in dataElement:
                self.songDataContainer[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER].append( el.find(Constants.A_TAG).get_attribute_list(Constants.HREF)[0])
                self.songDataContainer[Constants.LINK_TO_TUNE_POSTER_CONTAINER].append(el.find(Constants.IMG_TAG).get_attribute_list(Constants.SRC)[0])
                self.songDataContainer[Constants.SONG_NAME].append(
                    str(el.find(Constants.DIV, class_ = Constants.MAIN_PAGE_SONG_TEXT).find(Constants.B_TAG).text).replace(" ", "").replace("\n", "")
                )
                self.songDataContainer[Constants.SINGER_NAME].append(
                    str(el.find(Constants.DIV, class_ = Constants.MAIN_PAGE_SONG_TEXT).find_all(Constants.DIV)[1].text).replace(" ", "").replace("\n", "")
                )
            if(len(self.songDataContainer[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER]) > 0): self.resourceOccupiedFlag = True # resource occupied
        return self.songDataContainer
    
    def getDownloadingUrl(self, index : int) -> None:
        '''Takes one integer input from user to get the page link and retrieves 2 link for download'''
        try:
            if self.songDataContainer:
                pageResponse = requests.get(self.songDataContainer[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER][index])
                if(pageResponse.status_code == 200):
                    self.soup = BeautifulSoup(pageResponse.content.decode(Constants.PARSER_KEY), Constants.HTML_PARSER)
                    tagContainingLink : list[element.Tag] = self.soup.find_all(Constants.A_TAG, class_ = Constants.BTN_DOWNLOAD)
                    self.downloadableLinks = [a.get_attribute_list(key = Constants.HREF)[0] for a in tagContainingLink]
        except IndexError:
            return
        return
    
    def downloadSongFromLink(self,urlIndex : int,  downloadIndex : int) -> bool:
        '''Takes one integer index from user as 0 or 1 0 -> 180 kbps download and 1 -> 320kbps downloads'''
        try:
            self.getDownloadingUrl(urlIndex)
            if(self.downloadableLinks):
                downloadResponse = requests.get(self.downloadableLinks[downloadIndex])
                songName : str = self.downloadableLinks[downloadIndex].split("/")[-1]
                if(downloadResponse.status_code == 200):
                    with open(fr"D:\Music Lib\{songName}", "wb") as tune:
                        for chunk in downloadResponse.iter_content(chunk_size = 1024):
                            tune.write(chunk)
                    return True
        except IndexError:
            return False
        return False
    
    def loadImagesFromLink(self) -> list[QImage]:
        '''Takes no input but provides the QImageObject of the song posters based upon search results.
            returns none if any link is broken or not found
        '''
        container = [] # stores the out going image link
        for imageLink in self.songDataContainer[Constants.LINK_TO_TUNE_POSTER_CONTAINER]:
            try:
                posterReq = requests.get(imageLink)
                if(posterReq.status_code == Constants.STATUSCODE_SUCCEED):
                    container.append(
                        QImage(
                            Image.open(BytesIO(posterReq.content)).convert(Constants.RGBA_LITERAL).tobytes(Constants.RAW_LITERAL), 200, 200, QImage.Format.Format_RGBA8888
                        )
                    )
                else: container.append(None) # if data can't be fetched 
            except requests.exceptions: container.append(None)
        return container
    
    def _cleanAllMemory(self) -> None:
        '''When data is no longer required from engine then release the data useing this method'''
        self.songDataContainer = {
            Constants.LINK_TO_REDIRECT_TUNE_CONTAINER : [],
            Constants.LINK_TO_TUNE_POSTER_CONTAINER : [],
            Constants.SONG_NAME : [],
            Constants.SINGER_NAME : []
        }
        self.searchQuery : str = None
        self.downloadableLinks : list[str] = None
        self.resourceOccupiedFlag = False # resources are no longer occupied
    pass

# main method for testing operations
if __name__ == '__main__':
    bot = PagalFreeSiteExplorer()
    bot.getParameterFromUser(textInput = input("Enter song name:\t"))
    output = bot.dataExtractFromSearchQuery(bot.searchInWebsite())
    pass