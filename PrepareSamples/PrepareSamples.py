# @Author Milosz Filus

# History of changes
# Version - Author - Change
# v1        Milosz   Initial version

import os
from pathlib import Path
from PIL import Image
from PIL import ImageFilter
import json

IMAGES_PATH = '../Images'


DESTINATION_SAMPLES_DIRECTORY_PATH = 'Samples'
BLURRED_PATH = 'Samples/Blurred'
NOT_MODIFIED_PATH = 'Samples/Original'
NUMBER_OF_OPTIONS = 2


class ImageManager:

    def __init__(self):
        self.counter = 0
        self.json_validation = []

    def save_original(self, path):
        Image.open(path).save(NOT_MODIFIED_PATH + '/img_' + str(self.counter) + '.jpg', 'JPEG')
        self.json_validation.append(('img_' + str(self.counter) + '.jpg', 0))
        self.counter += 1

    def save_blurred(self, path):
        original = Image.open(path)
        blurred = original.filter(ImageFilter.GaussianBlur)
        blurred.save(BLURRED_PATH + '/img_' + str(self.counter) + '.jpg', 'JPEG')
        self.json_validation.append(('img_' + str(self.counter) + '.jpg', 1))
        self.counter += 1

def prepareDirectories():
    if not (os.path.exists(DESTINATION_SAMPLES_DIRECTORY_PATH) and os.path.isdir(DESTINATION_SAMPLES_DIRECTORY_PATH)):
        os.mkdir(DESTINATION_SAMPLES_DIRECTORY_PATH)

    if not (os.path.exists(BLURRED_PATH) and os.path.isdir(BLURRED_PATH)):
        os.mkdir(BLURRED_PATH)

    if not (os.path.exists(NOT_MODIFIED_PATH) and os.path.isdir(NOT_MODIFIED_PATH)):
        os.mkdir(NOT_MODIFIED_PATH)


def prepareSamples():
    prepareDirectories()
    im = ImageManager()
    for imagePath in Path(IMAGES_PATH).glob('**/*.jpg'):
        im.save_original(imagePath)
        im.save_blurred(imagePath)
    with open('validation.json', 'w') as file:
        json.dump(im.json_validation, file)


if __name__ == "__main__":
    prepareSamples()