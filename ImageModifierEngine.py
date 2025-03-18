# This file will be responsible for generating image objects and providing them to GUI class or other class need of using image for the design purpose or representation purpose for the application

from PIL import Image
import Constants

class ImageModifier:
    @staticmethod
    def resizeImage(imagePath : str, width : int, height = int) -> None:
        with Image.open(imagePath) as img:
            imgWidth, imgHeight = img.size
            if(imgWidth != width and imgHeight != height):
                print("worked")
                img = img.resize((width, height))
                img.save(imagePath)
        return
    
if __name__ == '__main__':
    ImageModifier.resizeImage("./static/icon.png", 128, 128)