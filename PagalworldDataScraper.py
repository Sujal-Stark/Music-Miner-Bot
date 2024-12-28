from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
from utility import Utility

import re
import Constants
from icecream import ic
import requests
from io import BytesIO
import time

class PagalWorldDataScraperBot(webdriver.Chrome):
    def __init__(self,siteUrl : list, options = None, service = None, keep_alive = True)->None:
        '''Constructor for Pagal world website crawling bot if bot doesn't work may possible that links are changed, use new links'''
        super().__init__(options, service, keep_alive)
        self.get(siteUrl)
        self.implicitly_wait(10)
        self.maximize_window()
        time.sleep(Constants.WAITFORLOADING)
        return
    
    # initiate properties of song
    def setSongDetailsFromUser(self, songName : str, singer : str = None, album : str = None) -> None:
        self.song_name = songName
        self.singer_name = singer
        self.album_name = album
        return
    
    def getInput(self, searchParameter : str):
        '''Takes user given input as song name'''
        searchBar = self.find_element(By.CSS_SELECTOR, 'input[id="gsc-i-id1"]')
        searchBar.send_keys(searchParameter)
        searchBar.send_keys(Keys.ENTER)
        time.sleep(Constants.WAITFORLOADING)
        return
    
    # returns how many pages can be iterated if user search by signer name only
    def searchBySingerInput(self) -> int:
        '''Search in website if only self.singer input is given, and finds out total number of pages that could be reached'''
        searchBar = self.find_element(By.CSS_SELECTOR, 'input[id="gsc-i-id1"]')
        searchBar.send_keys(self.singer_name)
        searchBar.send_keys(Keys.ENTER)
        time.sleep(Constants.WAITFORLOADING)
        try:
            searchPagesSoup = BeautifulSoup(
                self.find_element(By.CSS_SELECTOR, 'div[class="gsc-cursor"]').get_attribute("outerHTML"),
                "html.parser"
            )
            return len(searchPagesSoup.find_all("div"))
        except WebDriverException:
            ic("Unable to find selector")
        return 0

    def getAllSongHolderHTMLforSingerSearch(self, iter : int):
        if iter == 0 : return []
        urlList : list[str] = [] # all the songs holding HTML
        # assuming that bot is landed on first page
        i = -1
        try:
            for i in range(1, iter + 1):
                # navigatorDivision = self.find_element(By.CSS_SELECTOR, 'div[class="gsc-cursor"]')
                if(int(self.find_element(By.CSS_SELECTOR, 'div[class="gsc-cursor-page gsc-cursor-current-page"]').text) == i):
                    htmlLinks = [
                        el.get_attribute("href") for el in self.find_elements(By.CSS_SELECTOR,'a[class="gs-title"]')if (el.get_attribute("href")!= None and el.get_attribute("href").endswith(".html"))
                    ]
                    urlList = urlList + htmlLinks
                    self.find_element(By.CSS_SELECTOR, f'div[aria-label="Page {i+1}"]').click()
                    time.sleep(Constants.WAITFORLOADING)
        except WebDriverException as e:
            ic(f"oooops wrong web element: {e}") if i == -1 else ic(f"Got Runtime error: {e}")
            return urlList
    
    def findSongHolderElements(self) -> list:
        '''Finds all the HTML links that ridirects to diffent page'''
        songHolder = self.find_elements(By.CSS_SELECTOR, 'div[class="gs-title"]')
        songContainingURL = []
        for holder in songHolder:
            songContainingURL.append(
                holder.find_element(By.CSS_SELECTOR, 'a[class="gs-title"]').get_attribute("href")
            )
        return songContainingURL
    
    # download a specific song
    def downloadSingleSong(self, pageURL : str):
        '''download song from the given url in paramter. It uses two appproach.\n1. Sends HHTP request using the link found by bot and download it.\n2. If request fails then bot downloads it.'''
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
        '''Takes Html links of Pagal world site and fetch song related important data.'''
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
    
    # filters out actual song link from given HTML link O(1)
    def filterHtmlPagesByName(self, urls : list[str], targetText : str) -> list:
        '''Takes a list of URLs and analysing the target text inside it, if found returns it in a list'''
        outputUrls : list[str] = [] # a list that will store all the values of validated urls
        for html in urls:
            if (isinstance(html, str) and html.endswith(".html") and Utility.ifStringContains(html.split('/')[3], targetText = targetText)):
                outputUrls.append(html)
        return outputUrls
    
    # if other song paramters are given then it tries to analyse that parameter in link if found then that link is ranked up
    def filerHTMLPageswithOtherparameter(self, urls : list[str], secondaryParameter : str) -> list[str]:
        '''Reaarange given urls list according to the avialavility of secondary parameter is found in urls.\nReturn urls'''
        pos : int = 0 # it's the postion of the last ranked up link
        for i in range(len(urls)):
            if(urls[i] != None and Utility.ifStringContains(urls[i].split('/')[3], targetText = secondaryParameter)):
                temp = urls[pos]
                urls[pos] = urls[i]
                urls[i] = temp
                pos += 1
        return urls
    
    # reorganise the links based upon user given song name singer name and album name
    def filterSongs(self, urls:list[str]) -> list[str]:
        urls = self.filterHtmlPagesByName(urls = urls, targetText = self.song_name) # finds the name of song in links
        if(len(urls) == 0): return ["Invalid search query"] # don't check further if links are empty
        if self.singer_name: # finds the singer name in link and reorder
            urls = self.filerHTMLPageswithOtherparameter(urls = urls, secondaryParameter = self.singer_name)
        if(self.album_name): # finds album name and reorder
            urls = self.filerHTMLPageswithOtherparameter(urls = urls, secondaryParameter = self.album_name)
        if(len(urls) == 0): return ["Invalid search query"]
        return urls
    
    def __exit__(self, exc_type, exc, traceback):
        self.quit()
        return