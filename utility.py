# this file is created in purpose to store some functiions only that can be used for general purose actions
from icecream import ic
class Utility:
    # cheeck how much two Strings are equal with each other and sent percentage
    @staticmethod
    def ifStringContains(fetchedText : str, targetText : str) -> bool:
        '''Takes 2 string and finds out fetchedText contains the targetText the utility just ignore case sensitivity'''
        if(len(targetText) > len(fetchedText)): return False # if fetched text is smaller it can't contain the target text
        fetchedText, targetText = fetchedText.upper(), targetText.upper() # converting everything upper case to avoid case sensitivity
        ptr1 : int = 0 # tells the current positon for fetchedText
        ptr2 : int = 0 # tells the current position for targetText
        fetchedText = fetchedText.replace('-', ' ') # replaces special character to analyse properly
        while (ptr2 != len(targetText) and ptr1 != len(fetchedText)):
            if(fetchedText[ptr1] == targetText[ptr2]):
                ptr2 += 1
                if(ptr2 == len(targetText)): break
            else:
                if(ptr2 != 0):
                    ptr2 = 0
            ptr1 += 1
        return ptr2 == len(targetText)