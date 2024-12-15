from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from icecream import ic
import requests
from io import BytesIO
import time

class PagalWorldDataScraperBot(webdriver.Chrome):
    def __init__(self,siteUrl : list, options = None, service = None, keep_alive = True)->None:
        super().__init__(options, service, keep_alive)
        self.get(siteUrl)
        self.implicitly_wait(10)
        self.maximize_window()
        time.sleep(2)
        return
    
    def getInput(self, searchParameter : str):
        searchBar = self.find_element(By.CSS_SELECTOR, 'input[id="gsc-i-id1"]')
        searchBar.send_keys(searchParameter)
        searchBar.send_keys(Keys.ENTER)
        time.sleep(2)
        return
    
    def findSongHolderElements(self):
        songHolder = self.find_elements(By.CSS_SELECTOR, 'div[class="gs-title"]')
        songContainingURL = []
        for holder in songHolder:
            songContainingURL.append(
                holder.find_element(By.CSS_SELECTOR, 'a[class="gs-title"]').get_attribute("href")
            )
        return songContainingURL
    
    def __exit__(self, exc_type, exc, traceback):
        self.quit()
        return