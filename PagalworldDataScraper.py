from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

import re
import Constants
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
        time.sleep(Constants.WAITFORLOADING)
        return
    
    def getInput(self, searchParameter : str):
        searchBar = self.find_element(By.CSS_SELECTOR, 'input[id="gsc-i-id1"]')
        searchBar.send_keys(searchParameter)
        searchBar.send_keys(Keys.ENTER)
        time.sleep(Constants.WAITFORLOADING)
        return
    
    def findSongHolderElements(self):
        songHolder = self.find_elements(By.CSS_SELECTOR, 'div[class="gs-title"]')
        songContainingURL = []
        for holder in songHolder:
            songContainingURL.append(
                holder.find_element(By.CSS_SELECTOR, 'a[class="gs-title"]').get_attribute("href")
            )
        return songContainingURL
    
    # download a specific song
    def downloadSingleSong(self, pageURL : str):
        try:
            self.minimize_window()
            downloader = webdriver.Chrome()
            downloader.get(pageURL)
            downloader.maximize_window()
            time.sleep(Constants.WAITFORLOADING)
            downloadButton = downloader.find_element(By.CSS_SELECTOR, 'a[class="dbutton"]')
            url = downloadButton.get_attribute("href")
            if(url):
                downloadObject = requests.get(url, stream = True)
                if downloadObject.status_code == Constants.STATUSCODE_SUCCEED:
                    ic("Downloading Through HTTP Request")
                    with open("mySong.mp3", mode = 'a') as songFile:
                        for chunk in downloadObject.iter_content(chunk_size = 1024):
                            songFile.write(BytesIO(chunk))
                else:
                    ic("Downloading Through Bot")
                    downloadButton.click()
                    time.sleep(Constants.TIMEOUT)
                    downloader.close()
            else:
                ic("URL must be broken or removed")
        except WebDriverException:
            ic("Can't download the song")
        return
    
    # stores the all information that is available in the page about the song
    @staticmethod
    def getMusicInfoFromPage(htmlURL : str)-> dict:
        dataSet = {}
        htmlPage = BeautifulSoup(requests.get(htmlURL).text, 'html.parser')
        try:
            targetDivision = htmlPage.find("div", {"class" : "row file-details"})
            name_Singer = targetDivision.find("h2").text.split("-")
            dataSet["song"] = name_Singer[0].strip()
            dataSet["singer"] = name_Singer[1].strip()
            restData : list[str] = [i.text for i in targetDivision.findAll("div", re.compile("desc"))]
            dataSet["Album"] = restData[0].strip()
            dataSet["Format"] = restData[2].strip()
        except AttributeError:
            pass
        return dataSet
    
    def __exit__(self, exc_type, exc, traceback):
        self.quit()
        return