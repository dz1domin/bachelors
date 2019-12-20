import pytest
import os
import sys
import inspect
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import ModuleRunner as mr


def test_load_module_and_method():
    module, method = mr.load_module_and_method('TestModule', 'test_method')
    inspected = inspect.getmembers(module, inspect.isfunction)
    assert method('', {}) == ('', 'test')
    assert inspected[0][0] == 'test_method'


def test_get_image_paths():
    # nie wiem jak by to przetestowac xd
    pass


def test_load_action():
    pass


def test_load_validator():
    pass
