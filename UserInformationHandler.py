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
        """Initializes all necessary properties"""
        self.configFilePath = Constants.FILE_NAME # Full Location Of Config File
        self.colorJsonPath = Constants.COLOR_FILE_REL_PATH # Full location of colorJson File
        return

    def _generateSchema(self) -> list[dict]:
        """Generates the Required Parameters for application to run"""
        return [
            {
                Constants.DOWNLOADING_DIRECTORY_LOCATION : "",
                Constants.USER_NAME : "",
                Constants.WALLPAPER_PATH : ""
            }
        ]

    def generateConfigFile(self) -> bool | None:
        """If Application doesn't Have its config.json file. This method will create the json file"""
        path = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if not os.path.exists(path):
            try:
                with open(path, "x") as file: 
                    json.dump(self._generateSchema(), file ) # dump the empty schema in the file
                return True # file created
            except (OSError, MemoryError): return False
        return None

    def setUserName(self, userName : str) -> bool:
        """Set the user given name as Username for the Application"""
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if os.path.exists(filePath): # if file exists
            try:
                config_information = None
                with open(filePath, "r") as configFile: # reading current data
                    config_information = json.load(configFile)
                if config_information: # if config data is not malicious
                    with open(filePath, "w") as fileObj:
                        config_information[0][Constants.USER_NAME] = userName # setting data
                        json.dump(config_information, fileObj) # saving data
                    return True
                else: return False
            except(MemoryError, OSError, JSONDecodeError): return False
        else: return False

    def setWallpaperLocation(self, location : str) -> bool:
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if os.path.exists(filePath) and  os.path.exists(location): # if File Exists
            try:
                configInfo = None
                with open(filePath, "r") as configFile:
                    configInfo = json.load(configFile)
                if configInfo:
                    with open(filePath, "w") as configFile:
                        configInfo[0][Constants.WALLPAPER_PATH] = location
                        json.dump(configInfo, configFile)
                    return True
                else: return False
            except(MemoryError, OSError, JSONDecodeError): return False
        else: return False
    
    
    def setDownloadingDirectory(self, downloadingDirectory : str) -> bool:
        """Set the given name as Downloading directory in the config File"""
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if os.path.exists(filePath):
            try:
                with open(filePath, "r") as readConfigFile:
                    config_information = json.load(readConfigFile) # getting current configuraions
                    if config_information: # if currently  the is not empty with schema or not curroupted
                        with open(filePath, "w") as writeConfigFile:
                            # setting changes
                            config_information[0][Constants.DOWNLOADING_DIRECTORY_LOCATION] = downloadingDirectory
                            json.dump(config_information, writeConfigFile) # storing in the file
                        return True
                    else: return False
            except(MemoryError, OSError, JSONDecodeError): return False
        else: return False
    
    def getDownloadingDirectory(self) -> str | None:
        """
            If config.json file exists then this methods return the downloading Directory
            to the UI module
        """
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if os.path.exists(filePath): # if file exists
            try:
                location = None # return value
                with open(filePath, "r") as configFile:
                    config_information = json.load(configFile)
                    if config_information: location = config_information[0][Constants.DOWNLOADING_DIRECTORY_LOCATION]
                return location # if got perfect data
            except(MemoryError, OSError, JSONDecodeError): return None
        else: return None

    def getCurrentWallpaperLocation(self) -> str:
        """If config.json file exist's then this methods return the currently used
         wallpaper file location to the UI module"""
        filePath = os.path.join(os.getcwd(), Constants.FILE_NAME)
        if os.path.exists(filePath):
            try:
                location = None # return value
                with open(filePath, "r") as configFile:
                    information = json.load(configFile)
                    if information: location = information[0][Constants.WALLPAPER_PATH]
                return location # if data retrieved
            except(MemoryError, OSError, JSONDecodeError): return None
        else: return None
    
    ####### COLOR FILE HANDLING #######
    def _generateColorLogSchema(self) -> dict:
        """Generates the basic color Schemes for the application UI"""
        return {
            Constants.BUTTON_COLOR_CONFIG : [7, 128, 87],
            Constants.LABEL_COLOR_CONFIG : None,
            Constants.FRAME_COLOR_CONFIG : None
        }
    
    def generateColorFile(self) -> bool:
        """If Application doesn't have color.json file this method will create the file"""
        path = os.path.join(os.getcwd(), Constants.COLOR_FILE_REL_PATH) # full path creation
        if not os.path.exists(path):
            try:
                with open(path, "x") as file:
                    json.dump(self._generateColorLogSchema(), file) # dump the default Schema in the file
                return True
            except (OSError, MemoryError): return False
        else: return False

    def setColorValueIntoFile(self, key : str, value : list) -> bool:
        """
            Parameters:
                key -> a string value that refers to a key in related config file.
                value -> a tuple of 3 integers ranging from 0 to 255.
                Operation -> This method takes the key and value & store inside Color
                json File permanently, until next change.Returns True if succeeded.
        """
        path : str = os.path.join(os.getcwd(), self.colorJsonPath) # full path
        if os.path.exists(path):
            try:
                colorData = None # set initially to none for error handling
                with open(path, "r") as colorFile:
                    colorData = json.load(colorFile) # fetching data
                if colorData:
                    colorData[key] = value # adding changes
                    with open(path, "w") as writeColorFile:
                        json.dump(colorData, writeColorFile) # setting changes
                    return True
            except(OSError, MemoryError, JSONDecodeError): return False
        else: return False

    def getColorValueFromFile(self, key : str) -> tuple | None:
        """
            Parameters: key -> a string value that refers to a key in related config file.
            Operation: Takes the Key and fetch the co responding User chosen value from the colors.json file
        """
        path : str = os.path.join(os.getcwd(), self.colorJsonPath) # full path
        if os.path.exists(path):
            try:
                jsonData : dict = None # set initially to none for error handling
                with open(path, "r") as colorReadFile:
                    jsonData = json.load(colorReadFile) # loading Data
                if jsonData: return jsonData[key] # delivering req value
            except(MemoryError, OSError, JSONDecodeError): return None
        else: return None
    pass
    

if __name__ == '__main__':
    configHandler = ConfigFileHandler()
    if configHandler.generateConfigFile():
        print("File Created SuccessFully")
    else:
        print("Can't Create File. Maybe it's already created")
    if configHandler.setDownloadingDirectory(os.getcwd()): print("Downloading Directory is set")
    if configHandler.setUserName("Sujal Khan"): print("User name is set successfully")
