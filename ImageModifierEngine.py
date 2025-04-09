# This file will be responsible for generating image objects and providing them to GUI class or other class need of using image for the design purpose or representation purpose for the application

from PIL import Image, UnidentifiedImageError
import Constants

class ImageModifier:
    @staticmethod
    def resizeImage(imagePath : str, width : int = Constants.SOFTWARE_WIDTH, height : int = Constants.SOFTWARE_HEIGHT) -> bool:
        '''Resizes the image on the given path according to the Width and Height. Weather the image is larger or smaller than the given size this method will resize it to the given size'''
        try:
            with Image.open(imagePath) as img:
                if(img.size[0] != width and img.size[1] != height):# only works if the image size and given size doesn't match
                    img = img.resize((width, height)).save(imagePath)
        except (UnidentifiedImageError, OSError, MemoryError, TypeError, FileNotFoundError, ValueError):
            return False
        return True
    
if __name__ == '__main__':
    ImageModifier.resizeImage("./static/icon.png", 128, 128)