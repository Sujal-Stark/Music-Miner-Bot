# This File takes input for user information and saves it in launch.json file for further use

import os, pathlib
import json
from json import JSONDecodeError
# Custom import
import Constants

class ConfigFileHandler:
    def __init__(self):
        self._properties()
        return
    
    def _properties(self) -> None:
        '''Initializes all necessary properties'''
        return

    def _generateSchema(self) -> dict:
        '''Generates the Required Parameters for application to run'''
        return [
            {
                Constants.DOWNLOADING_DIRECTORY_LOCATION : "",
                Constants.USER_NAME : "",
                Constants.WALLPAPER_PATH : ""
            }
        ]

    def generateConfigFile(self) -> str:
        '''If Application doesn't Have it's config.json file. This method will create the json file'''
        if(not os.path.exists(os.path.join(os.getcwd(), Constants.FILE_NAME))):
            try:
                with open(os.path.join(os.getcwd(), Constants.FILE_NAME), "x") as file: 
                    json.dump(self._generateSchema(), file ) # dump the empty schema in the file
                return os.path.join(os.getcwd(), Constants.FILE_NAME) # file created
            except (OSError, MemoryError): return None
        else: return os.path.join(os.getcwd(), Constants.FILE_NAME) # if the file either exists
    
    def setDownloadingDirectory(self, downloadingDirectory : str) -> bool:
        '''Set the given name as Downloading directory in the config File'''
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if(os.path.exists(filePath)):
            try:
                with open(filePath, "r") as configFile:
                    config_information = json.load(configFile) # getting current configuraions
                    if(config_information): # if currently  the is not empty with schema or not curroupted
                        with open(filePath, "w") as configFile:
                            config_information[0][Constants.DOWNLOADING_DIRECTORY_LOCATION] = downloadingDirectory # setting changes
                            json.dump(config_information, configFile) # storing in the file
                        return True
                    else: return False
            except(MemoryError, OSError, JSONDecodeError): return False
        else: return False
    
    def getDownloadingDirectory(self) -> str:
        '''If config.json file exist's then this methods return the downloading Directory to the UI module'''
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if(os.path.exists(filePath)): # if file exists
            try:
                location = None # return value
                with open(filePath, "r") as configFile:
                    config_information = json.load(configFile)
                    if(config_information): location = config_information[0][Constants.DOWNLOADING_DIRECTORY_LOCATION]
                return location # if got perfect data
            except(MemoryError, OSError, JSONDecodeError): return None
        else: return None

    def getCurrentWallpaperLocation(self) -> str:
        '''If config.json file exist's then this methods return the currently used wallpaper file location to the UI module'''
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if(os.path.exists(filePath)):
            try:
                location = None # return value
                with open(filePath, "r") as configFile:
                    information = json.load(configFile)
                    if(information) : location = information[0][Constants.WALLPAPER_PATH]
                return location # if data retrieved
            except(MemoryError, OSError, JSONDecodeError): return None
        else: return None
    
    def setUserName(self, userName : str) -> bool:
        '''Set the user given name as User name for the Application'''
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if(os.path.exists(filePath)): # if file exists
            try:
                with open(filePath, "r") as configFile: # reading current data
                    config_information = json.load(configFile)
                    if(config_information): # if config data is not malicious
                        with open(filePath, "w") as fileObj:
                            config_information[0][Constants.USER_NAME] = userName # setting data
                            json.dump(config_information, fileObj) # saving data
                            return True
                    else: return False
            except(memoryview, OSError, JSONDecodeError): return False
        else: return False
    pass

if __name__ == '__main__':
    configHandler = ConfigFileHandler()
    if(configHandler.generateConfigFile()):
        print("File Created SuccessFully")
    else:
        print("Can't Create File. Maybe it's already created")
    if(configHandler.setDownloadingDirectory(os.getcwd())): print("Downloading Directory is set")
    if(configHandler.setUserName("Sujal Khan")): print("User name is set successfully")
