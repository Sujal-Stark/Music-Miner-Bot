# this file is responsible for implementing all the processes that are created in other files of this directory
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from PagalworldDataScraper import PagalWorldDataScraperBot
from icecream import ic
import Constants

try:
    with PagalWorldDataScraperBot(siteUrl = Constants.PAGALWORLDURL) as bot1:
        bot1.getInput("challa")
        ic(bot1.findSongHolderElements())
        pass

except WebDriverException as e:
    ic(f"Oh shit exception occurred as {e}")