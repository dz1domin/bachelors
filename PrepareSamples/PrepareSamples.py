# @Author Milosz Filus

# History of changes
# Version - Author - Change
# v1        Milosz   Initial version

import os
from pathlib import Path
from PIL import Image
from PIL import ImageFilter

IMAGES_PATH = '../Images'


DESTINATION_SAMPLES_DIRECTORY_PATH = 'Samples'
FULLY_BLURRED_PATH = 'Samples/Blurred' #which should be classified as blured
SEMI_BLURRED_PATH = 'Samples/SemiBlurred' #better check manually
NOT_MODIFIED_PATH = 'Samples/Original' #which should be classified as sharp
NUMBER_OF_OPTIONS = 3


class ImageManager:

    notModifiedCounter = 0
    semiBlurredCounter = 0
    wholeBlurredCounter = 0

    @staticmethod
    def saveWithoutBlurring(path):
        Image.open(path).save(NOT_MODIFIED_PATH + '/img_' + str(ImageManager.notModifiedCounter) + '.jpg', 'JPEG')
        ImageManager.notModifiedCounter += 1

    @staticmethod
    def blurWholeImage(path):
        original = Image.open(path)
        blurred = original.filter(ImageFilter.GaussianBlur)
        blurred.save(FULLY_BLURRED_PATH + '/img_' + str(ImageManager.wholeBlurredCounter) + '.jpg', 'JPEG')
        ImageManager.wholeBlurredCounter += 1

    #TBD - algorithm should compute how many boxes should blur + fit coords
    @staticmethod
    def blurPartOfImage(path, percentOfPixelsToBeBlurred):
        original = Image.open(path)
        for i in range(5):
            box = (i*100, i*100, 100 + i*100, 100 + i*100)
            toBeBlurred = original.crop(box)
            for j in range(10):
                toBeBlurred = toBeBlurred.filter(ImageFilter.BLUR)
            original.paste(toBeBlurred, box)
        original.save(SEMI_BLURRED_PATH + '/img_' + str(ImageManager.semiBlurredCounter) + '.jpg', 'JPEG')
        ImageManager.semiBlurredCounter += 1

def prepareDirectories():
    if not (os.path.exists(DESTINATION_SAMPLES_DIRECTORY_PATH) and os.path.isdir(DESTINATION_SAMPLES_DIRECTORY_PATH)):
        os.mkdir(DESTINATION_SAMPLES_DIRECTORY_PATH)

    if not (os.path.exists(FULLY_BLURRED_PATH) and os.path.isdir(FULLY_BLURRED_PATH)):
        os.mkdir(FULLY_BLURRED_PATH)

    if not (os.path.exists(SEMI_BLURRED_PATH) and os.path.isdir(SEMI_BLURRED_PATH)):
        os.mkdir(SEMI_BLURRED_PATH)

    if not (os.path.exists(NOT_MODIFIED_PATH) and os.path.isdir(NOT_MODIFIED_PATH)):
        os.mkdir(NOT_MODIFIED_PATH)


def prepareSamples():
    prepareDirectories()
    decisiveCounter = 0
    for imagePath in Path(IMAGES_PATH).glob('**/*.jpg'):

        if decisiveCounter == 0:
            ImageManager.saveWithoutBlurring(imagePath)
        elif decisiveCounter == 1:
            ImageManager.blurPartOfImage(imagePath, 0.5) #later maybe will be random
        elif decisiveCounter == 2:
            ImageManager.blurWholeImage(imagePath)
        decisiveCounter = (decisiveCounter + 1) % NUMBER_OF_OPTIONS

prepareSamples()