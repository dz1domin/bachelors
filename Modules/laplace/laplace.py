import cv2


def laplace(img_path, options):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_path, str(cv2.Laplacian(img_gray, cv2.CV_64F).var() < float(options['thresh']))