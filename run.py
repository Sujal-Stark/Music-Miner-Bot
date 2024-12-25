# this file is responsible for implementing all the processes that are created in other files of this directory
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from PagalworldDataScraper import PagalWorldDataScraperBot
from icecream import ic
import Constants
from utility import Utility

try:
    with PagalWorldDataScraperBot(siteUrl = Constants.PAGALWORLDURL) as bot1:
        userInput = "teri deewani"
        bot1.getInput(userInput)
        ic(bot1.filterHtmlPagesByName(bot1.findSongHolderElements(), targetText = userInput))
    # ic(Utility.ifStringContains(fetchedText = "TERI-DEEWANI", targetText = "TERI DEEWANI"))
except WebDriverException as e:
    ic(f"Oh shit exception occurred as {e}")