import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from Modules.laplace.laplace import laplace


def test_laplace():
    out = laplace(os.path.dirname(os.path.abspath(__file__)) + '/TestImage/testImage.jpg', {'thresh': 10.0})
    assert out[1] == 'False'