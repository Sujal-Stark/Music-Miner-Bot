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
    pass

# main method for testing operations
if __name__ == '__main__':
    bot = PagalFreeSiteExplorer()
    bot.getParameterFromUser(textInput = input("Enter song name:\t"))
    bot.searchInWebsite()