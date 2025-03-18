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


# WEB SITE PARAMTERS
PAGALFREESITEURL = r"https://pagalfree.com/"
SEARCH_DELIMITER = "%20" # replaces the space key
SEARCH_END_POINT = "search/" # end point for search operation in site
ID_CATAGORY_CONTENT = "category_content"

# PROSSESSING ALGORTITHM RELATED CONSTANTS
NOT_FOUND_MESSAGE = "NOT FOUND"
LINK_TO_REDIRECT_TUNE_CONTAINER = "link_to_redirect_tune_container" # dictionary key
LINK_TO_TUNE_POSTER_CONTAINER = "link_to_tune_poster_container" # dictionary key
SONG_NAME = "song name" # dictionary key
SINGER_NAME = "singer name" # dictionary key

# SOFTWARE DIMENTION RELATED
SOFTWARE_TITLE = "Music-Miner-Bot" # shows as the name
SOFTWARE_WIDTH = 860 # main window length
SOFTWARE_HEIGHT = 660 # main window height
# Search Section Width and height
SEARCH_SECTION_WIDTH = 820
SEARCH_SECTION_HEIGHT = 80
# control section Width and Height
CONTROL_SECTION_WIDTH = 200
CONTROL_SECTION_HEIGHT = 535
# View panel Height and Width
VIEW_PANEL_WIDTH = 610
VIEW_PANEL_HEIGHT = CONTROL_SECTION_HEIGHT

# Widget Related Sconstants

# SEARCH RELATED BUTTONS
SEARCH_BUTTON = "Search"
SEARCH_BY_SINGER_BUTTON =  "Search by singer's Name"
SEARCH_HERE = "Search here....."

# CONTROL RELATED BUTTON TEXTS
CHANGE_BACKGROUND = "Change Background"
SET_DOWNLOAD_DIRECTORY = "Set downlaoding Directory"
SHOW_HIGH_QUALITY = "Show High Quality"
SHOW_LOW_QUALITY = "Show Low Quality"
SHOW_DOWNLOAD_HISTORY = "Show downloading history"
DELETE_DOWNLOAD_HISTORY = "Delete downloading history"

# table Headers and sizes meant to be used as constants
SERIAL = "Serial"
SERIAL_SIZE = 130
THUMBNAIL = "Thumbnail"
THUMBNAIL_SIZE = 130
SONG_NAME = "Song name"
SONG_NAME_SIZE = 150
SINGER_NAME = "Singer name"
SINGER_NAME_SIZE = 150
DOWNLOAD_URL = "Download Url"
DOWNLOAD_URL_SIZE = 115 

# Static file Paths
ICON_PATH = R"static\icon.png" # Window Icon
TABLE_DEFAULT_LABEL = R"static\tagline.png"
STARTING_SCREEN_PATH = R"static\startingScreen.png" # for splash screen image
STARTING_SCREEN_SHOW_TIME = 3 # for this much time the splash Screen will be visbile

#QML path
MAIN_QML_PATH = "masterUI.qml" # Styles for Main application