import cv2
import numpy as np


def fourier(img_path, options):
    img = cv2.imread(r'{}'.format(img_path))
    if img is None:
        return '', ''
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    row, cols = img_gray.shape
    crow, ccol = row // 2, cols // 2
    xoff, yoff = int(row * 0.05), int(cols * 0.05)
    fft = np.fft.fft2(img_gray)
    fft_shifted = np.fft.fftshift(fft)
    fft_shifted[crow - xoff:crow + xoff, ccol - yoff:ccol + yoff] = 0
    fft_inverse_shift = np.fft.ifftshift(fft_shifted)
    fft_inverse = np.fft.ifft2(fft_inverse_shift)
    fft_inverse = 20 * np.log(np.abs(fft_inverse))
    return img_path, str(np.mean(fft_inverse) < float(options['thresh']))