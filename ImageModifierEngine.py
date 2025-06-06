# This file will be responsible for generating image objects and providing them to GUI class or other class
# need of using image for the design purpose or representation purpose for the application
from PIL import Image, UnidentifiedImageError
import os

import Constants

class ImageModifier:
    # properties
    currentWallpaperLocation = None

    def getCurrentlyUsedImageLocation(self, location) -> None:
        """
            Takes user's currently using wallpaper location and set this as class property
            :param location: String [Valid Image location]
            :return: None
        """
        self.currentWallpaperLocation = location
        return None

    def resizeImage(
            self, imagePath: str, width: int = Constants.SOFTWARE_WIDTH, height: int = Constants.SOFTWARE_HEIGHT,
            dPath: str = None
    ) -> bool:
        """
            Resizes the image on the given path according to the Width and Height. Weather the image is larger
            or smaller than the given size this method will resize it to the given size
        """
        # only perform delete action if there is a wallpaper location in the ./temp directory
        if self.currentWallpaperLocation: ImageModifier.clearTempDirectory(self.currentWallpaperLocation)
        try:
            with Image.open(imagePath) as img:
                if img.size[0] != width or img.size[1] != height:# only works if image size and given size doesn't match
                    img = img.resize((width, height))
                if dPath: img.save(dPath)
                else: img.save(imagePath)
        except (UnidentifiedImageError,OSError, TypeError, FileNotFoundError, MemoryError, ValueError):
            return False
        return True
    
    @staticmethod
    def computeAVGColor(imagePath : str) -> tuple[int, int, int] | tuple:
        """
            Input > imagePath : str  --- valid path of an Image
            Output > List[int, int, int] R(avg), G(avg), B(avg)
        """
        output : tuple = ()
        if imagePath is None: return output
        if not os.path.exists(imagePath):
           imagePath : str = os.getcwd() + imagePath
        if os.path.exists(imagePath):
            try:
                with Image.open(imagePath) as image:
                    pixels = image.getdata()
                    pixelCount = image.width * image.height
                    RGB = list(map(lambda c : (sum(c)// pixelCount), zip(*pixels)))
                    output = tuple(RGB[0 : 3])
            except (OSError, MemoryError, TypeError, FileNotFoundError, ValueError):
                print("Error")
        else: pass
        return output

    @staticmethod
    def clearTempDirectory(current_file_path : str) -> None:
        """
            After Completing wallpaper Changing operation use this method to keep Temp folder Clean.
        """
        try:
            for tempFile in os.listdir("./temp"):
                path = os.path.join(os.getcwd() + "/temp/", tempFile).replace("\\", "/")
                if path != current_file_path: os.remove(path)
        except (OSError, MemoryError, TypeError, FileNotFoundError, ValueError):
            print("Error")
        return
    pass
if __name__ == '__main__':
    imageModifier = ImageModifier()
    pass