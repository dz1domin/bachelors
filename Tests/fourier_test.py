import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from Modules.fourier.fourier import fourier


def test_fourier():
    out = fourier('./TestImage/testImage.jpg', {'thresh': 10.0})
    assert out[1] == 'False'