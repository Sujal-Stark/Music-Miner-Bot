# this file is created in purpose to store some functiions only that can be used for general purose actions
from icecream import ic
class Utility:
    # cheeck how much two Strings are equal with each other and sent percentage
    @staticmethod
    def ifStringContains(fetchedText : str, targetText : str) -> bool:
        """Takes 2 string and finds out fetchedText contains the targetText the utility just ignore case sensitivity"""
        if len(targetText) > len(fetchedText): return False # if fetched text is smaller it can't contain the target text
        fetchedText, targetText = fetchedText.upper(), targetText.upper() # converting everything upper case to avoid case sensitivity
        # replaces special character to analyse properly
        fetchedText = fetchedText.replace('-', ' ')
        fetchedText = fetchedText.replace('%', ' ')
        return targetText in fetchedText # returns true if target text is in fetched text else returns false

if __name__ == '__main__':
    ic(Utility.ifStringContains(fetchedText = "i am Tony Stark. Genius Billionaire Playboy Philanthropist",
    targetText = "tony Stark"))