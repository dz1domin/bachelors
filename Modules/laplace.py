import cv2
import numpy as np

def laplace(img_path):
	img = cv2.imread(img_path)
	img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
	return cv2.Laplacian(img_gray, cv2.CV_64F).var()