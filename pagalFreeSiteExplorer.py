# this file is responsible for navigating in pagalFreeWebsite, search song, getting links and downloading all the songs and other related operations

import requests
from bs4 import BeautifulSoup, element
from icecream import ic
# custom imports
import Constants

class PagalFreeSiteExplorer:
    def __init__(self):
        self.setProperties()
        pass

    # declare properties
    def setProperties(self) -> None:
        self.BASE = Constants.PAGALFREESITEURL
        self.searchQuery : str = None
        self.soup : BeautifulSoup = None
        return None
    
    def getParameterFromUser(self, textInput : str) -> None:
        self.searchQuery = textInput.replace(" ", Constants.SEARCH_DELIMITER)
        return None
    
    # search the query in the website if found then returns the list of the elements
    def searchInWebsite(self) -> list[element.Tag]:
        searchRequest = requests.get(self.BASE + Constants.SEARCH_END_POINT + self.searchQuery)
        if (searchRequest.status_code == 200):
            self.soup = BeautifulSoup(
                searchRequest.content.decode(Constants.PARSER_KEY), Constants.HTML_PARSER
            )
            return self.soup.find_all(Constants.DIV, id = Constants.ID_CATAGORY_CONTENT)
        else:
            return [Constants.NOT_FOUND_MESSAGE]
    
    # separates search query elemnts and sent them in a dictionary form
    def dataExtractFromSearchQuery(self, dataElement : list[element.Tag]) -> dict:
        songDataContainer = {
            Constants.LINK_TO_REDIRECT_TUNE_CONTAINER : [], # contains the link of the song
            Constants.LINK_TO_TUNE_POSTER_CONTAINER : [], # stores the link of the poster
            Constants.SONG_NAME : [] # stores the name of actual songs
        }
        for el in dataElement:
            songDataContainer[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER].append( el.find(Constants.A_TAG).get_attribute_list(Constants.HREF)[0])
            songDataContainer[Constants.LINK_TO_TUNE_POSTER_CONTAINER].append(el.find(Constants.IMG_TAG).get_attribute_list(Constants.SRC)[0])
            songDataContainer[Constants.SONG_NAME].append(str(el.find(Constants.DIV, class_ = Constants.MAIN_PAGE_SONG_TEXT).find(Constants.B_TAG).text).replace(" ", "").replace("\n", ""))
        return songDataContainer
    pass

# main method for testing operations
if __name__ == '__main__':
    bot = PagalFreeSiteExplorer()
    bot.getParameterFromUser(textInput = input("Enter song name:\t"))
    output = bot.dataExtractFromSearchQuery(bot.searchInWebsite())
    for i in range(20):
        print(
            "iterator\t",i,"\n",
            "Song name:\t",output[Constants.SONG_NAME][i],"\n",
            "Song link\t", output[Constants.LINK_TO_REDIRECT_TUNE_CONTAINER][i],"\n",
            "Image Link\t", output[Constants.LINK_TO_TUNE_POSTER_CONTAINER][i],"\n"
        )