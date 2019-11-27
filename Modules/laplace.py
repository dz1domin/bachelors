import cv2
from pathlib import Path


def laplace(img_path, options):
    img = cv2.imread(r'{}'.format(img_path))
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_path, str(cv2.Laplacian(img_gray, cv2.CV_64F).var() < float(options['thresh']))

# laplace('D:\images\CERTH_ImageBlurDataset\EvaluationSet\DigitalBlurSet\DiskR10_1.jpg', dict())