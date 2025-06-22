# stores all the constants and values to work with the bot

# DEFAULT BS4 & REQUESTS RELATED CONSTANTS
STATUSCODE_SUCCEED = 200 # http status code for successful completion for operation
PARSER_KEY = "utf-8" # convention
HTML_PARSER = "html.parser" # convention
RGBA_LITERAL = "RGBA" # convention
RAW_LITERAL = "raw" # convention
DIV = "div" # HTML tag
A_TAG = "a" # HTML tag
HREF = "href" # HTML tag
IMG_TAG = "img" # HTML tag
SRC = "src" # HTML tag
B_TAG = "b" # HTML tag
MAIN_PAGE_SONG_TEXT = "main_page_category_music_txt" # CSS selector
BTN_DOWNLOAD = "btn-download" # css Selector
KBPS_320 = "320Kbps"
KBPS_128 = "128Kbps"
MP3_EXTENSION = ".mp3"
WELCOME = "Welcome!!!"
UNABLE_TO_LOAD =  "Unable to load"

# WEB SITE PARAMETERS
PAGAL_FREE_SITE_URL = r"https://pagalfree.com/"
SEARCH_DELIMITER = "%20" # replaces the space key
SEARCH_END_POINT = "search/" # end point for search operation in site
ID_CATAGORY_CONTENT = "category_content"
INDICATOR_WIDTH = 20 # can be used to give default width to any indicator

# POSSESSING ALGORITHM RELATED CONSTANTS
NOT_FOUND_MESSAGE = "NOT FOUND"
LINK_TO_REDIRECT_TUNE_CONTAINER = "link_to_redirect_tune_container" # dictionary key
LINK_TO_TUNE_POSTER_CONTAINER = "link_to_tune_poster_container" # dictionary key


######################################### Key action related ##############################################
ENTER_KEY_SHORTCUT = "Enter Key Shortcut"

# SOFTWARE DIMENSION RELATED
SOFTWARE_TITLE = "Music-Miner-Bot" # shows as the name
SOFTWARE_WIDTH = 900 # main window length
SOFTWARE_HEIGHT = 720 # main window height
MASTER_FRAME_OBJECT_NAME = "master_layout_frame"
DEFAULT_WALLPAPER_LOCATION = "./static/arora1.jpg"
# Search Section Width and height
SEARCH_SECTION_WIDTH = 860
SEARCH_SECTION_HEIGHT = 80
SEARCH_SECTION_BUTTON_HEIGHT = 25
# control section Width and Height
CONTROL_SECTION_WIDTH = 200
CONTROL_SECTION_HEIGHT = 535
CONTROL_SECTION_BUTTON_WIDTH = CONTROL_SECTION_WIDTH - 20
CONTROL_SECTION_BUTTON_HEIGHT = 40
# View panel Height and Width
VIEW_PANEL_WIDTH = 650
VIEW_PANEL_HEIGHT = CONTROL_SECTION_HEIGHT
# Information section with and height
INFORMATION_SECTION_WIDTH = 860
INFORMATION_SECTION_HEIGHT = 40

# Widget Related Constants

# ALERTDIALOG CONSTANTS
SELECT_DIRECTORY = "Select Directory"

# SEARCH RELATED BUTTONS
SEARCH_BUTTON = "Search"
SEARCH_BY_SINGER_BUTTON =  "Search by singer's Name"
SEARCH_HERE = "Search here....."

# CONTROL RELATED BUTTON TEXTS
CHANGE_BACKGROUND = "Change Background"
SET_DOWNLOAD_DIRECTORY = "Set downloading Directory"
SHOW_HIGH_QUALITY = "Show High Quality"
SHOW_LOW_QUALITY = "Show Low Quality"
SHOW_DOWNLOAD_HISTORY = "Show downloading history"
DELETE_DOWNLOAD_HISTORY = "Delete downloading history"
RESET_VIEW_PANEL = "Delete"

# table Headers and sizes meant to be used as constants
SERIAL = "Serial"
SERIAL_SIZE = 130
THUMBNAIL = "Thumbnail"
THUMBNAIL_SIZE = 150
SONG_NAME = "Song name"
SONG_NAME_SIZE = 170
SINGER_NAME = "Singer name"
SINGER_NAME_SIZE = 170
DOWNLOAD_URL = "Download Here"
DOWNLOAD_URL_SIZE = 115
DOWNLOAD_BUTTON_TEXT = "Download"
ROW_HEIGHT = 150
SEARCH_RESULT = "Search Result"

# Static file Paths
ICON_PATH = R"static\icon.ico" # Window Icon
TABLE_DEFAULT_LABEL = R"static\tagline.png"
STARTING_SCREEN_PATH = R"static\startingScreen.png" # for splash screen image
STARTING_SCREEN_SHOW_TIME = 3 # for this much time the splash Screen will be visbile

#QML path
MAIN_QML_PATH = "masterUI.qml" # Styles for Main application

# TOOL_TIP_CONSTANTS
SEARCH_BUTTON_TOOL_TIP = "Click to search"
SEARCH_BY_SINGER_TOOL_TIP = "Enter any Singer name & search"
BACKGROUND_BUTTON_TOOL_TIP = "Change the background of Application"
DOWNLOAD_HISTORY_BUTTON_TOOL_TIP = "Reveals all history"
DOWNLOAD_DIRECTORY_BUTTON_TOOL_TIP = "Set any directory as downloading directory"
LOW_QUALITY_ENABLE_BUTTON_TOOL_TIP = "Switch to 180kbps"
HIGH_QUALITY_ENABLE_BUTTON_TOOL_TIP = "Switch to 320 kbps"
DELETE_DOWNLOAD_HISTORY_BUTTON_TOOL_TIP = "Delete Browsing History"
RESET_PANEL_BUTTON_TOOL_TIP = "Removes all search items from view panel"

LABEL_POSTER_TOOL_TIP = "Search First to get your result"


# DEFAULT STYLES
DOWNLOAD_BUTTON_STYLE = """QPushButton {
    background-color: rgb(7, 128, 87); }QPushButton:hover {background-color: rgb(0, 160, 110);
}"""


# CONFIG FILE CONSTANTS
FILE_NAME = "config.json"
DOWNLOADING_DIRECTORY_LOCATION = "Downloading Directory"
USER_NAME = "User Name"
WALLPAPER_PATH = "Wall Paper Path"

# COLOR FILE CONSTANTS
COLOR_FILE_REL_PATH = "colors.json"
BUTTON_COLOR_CONFIG = "Button_Color"
LABEL_COLOR_CONFIG = "Label_Color"
FRAME_COLOR_CONFIG = "Frame_Color"


# MESSAGE FOR USER
DOWNLOAD_FAILED = "Sorry Download has been failed"
INVALID_DIRECTORY = "Given Directory is invalid"
DOWNLOAD_SUCCEED = "Downloaded"
FAILED_TO_COMMIT_CHANGE = "Failed to Commit Change"
SEARCH_MSG = "Searching"
SEARCH_COMPLETED = "Completed"
CLEAN_REQ_MESSAGE = "Clean View panel"
UNEXPECTED_ERROR_MESSAGE = "Sorry!! Unexpected Error occurred"
INTERNET_CONNECTION_OFF_ERROR = "Turn on System's Internet Connection to browse"
DOWNLOAD_CONTINUES = "Downloading..."




####################################### CONSTANTS FOR WALLPAPER PREVIEW #############################################
WALLPAPER_PREVIEW_STYLE_PATH = "WallPaperPreviewStyle.qml" # Style for Image Preview Window
WALLPAPER_PREVIEW_TITLE = "Select Wallpaper" # main ttile for the window
WALLPAPER_PREVIEW_WIDTH = 600 # fixed width of the window
WALLPAPER_PREVIEW_HEIGHT = 600 # fixed height for the window

# FRAMES
WALLPAPER_PREVIEW_MAIN_FRAME_WIDTH = WALLPAPER_PREVIEW_WIDTH - 10
WALLPAPER_PREVIEW_MAIN_FRAME_HEIGHT = WALLPAPER_PREVIEW_HEIGHT - 10

# PUSH BUTTONS
SELECT_FROM_DEVICE = "Select from Device"
USE = "Use as Wallpaper"
WALLPAPER_PREVIEW_BUTTON_WIDTH = 150
WALLPAPER_PREVIEW_BUTTON_HEIGHT = 40

# LABELS
SCREEN_PREVIEW = "Preview of the Application"
CUSTOM_WALLPAPER = "Custom Wallpapers"

# SONG CARD
SONG_CARD_OBJECT_NAME = "Song Card"
SONG_CARD_WIDTH = VIEW_PANEL_WIDTH - 60
SONG_CARD_HEIGHT = 150
SONG_CARD_IMAGE_WIDTH = 130
SONG_CARD_IMAGE_HEIGHT = 130
SONG_CARD_NAME_LABEL_WIDTH = 400
SONG_CARD_QSS_LOCATION = "./SongCard.qss"

# static wallpaper location
WALLPAPER_ARORA = "./static/arora1.jpg"
WALLPAPER_BLACK_HOLE = "./static/blackHole.jpeg"
WALLPAPER_DESERT = "./static/desert.jpeg"
WALLPAPER_DRAGON = "./static/dragon.jpeg"
WALLPAPER_PLANET = "./static/planet.jpeg"

#  CLICKABLE LABEL CONSTANTS
LOCATION_PROP = "Location"

#################   DUMMY FILE    ####################
TEMP_PATH = "/temp/"
DUMMY_RESOURCE_FOLDER = "./DummyResourceFolder"
DUMMY_FILE_STYLE_PATH = "DummyFile_style.qml"
DUMMY_WINDOW_WIDTH = 540
DUMMY_WINDOW_HEIGHT = 300


################################## DataBase Manager ################################
DB_MANAGER_WINDOW_TITLE = "History"
DB_MANAGER_WINDOW_WIDTH =  600
DB_MANAGER_WINDOW_HEIGHT = 400

DB_MAIN_FRAME_WIDTH = DB_MANAGER_WINDOW_WIDTH - 20
DB_MAIN_FRAME_HEIGHT = DB_MANAGER_WINDOW_HEIGHT - 20
DB_MAIN_FRAME_OBJECT_NAME = "Main Frame"

DB_BODY_LAYOUT_FRAME_OBJECT_NAME = "Body Layout Frame"

DB_SCROLL_AREA_OBJECT_NAME = "History Scroll Area"
DB_BODY_LAYOUT_SCROLL_AREA_WIDTH = 560
DB_BODY_LAYOUT_SCROLL_AREA_HEIGHT = 310
DB_TABLE_SL = "Sl"
DB_TABLE_SONG_NAME = "Song Name"
DB_TABLE_DATE = "Date"
DB_UI_QSS_PATH = "./DataBaseManager.qss"