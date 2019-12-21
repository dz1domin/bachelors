import pytest
import os
import sys
import inspect
import glob
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import ModuleRunner as mr
from Actions.actioninterface import ActionInterface

def test_load_module_and_method():
    module, method = mr.load_module_and_method('Module', 'method')
    inspected = inspect.getmembers(module, inspect.isfunction)
    assert method('', {}) == ('', 'test')
    assert inspected[0][0] == 'method'


def test_get_image_paths():
    paths = mr.get_image_paths('./TestImage', False, ['*.jpg'])
    for el in paths:
        assert os.path.isfile(el)


def test_load_action():
    action_obj = mr.load_action('copy')
    assert isinstance(action_obj, ActionInterface)


def test_load_validator(capsys):
    
    validator_base_class = 'Validator.py'
    validator_base_dir = '/Validators'
    assert os.path.isdir(base_path + validator_base_dir)

    os.chdir(base_path + validator_base_dir)
    files = glob.glob("*.py")

    assert validator_base_class in files
    files.remove(validator_base_class)

    for validator_class in files:
        assert mr.load_validator(validator_class.split('.')[0]) is not None

    test_invalid_validator = 'ValidatorWhichDoesntExist'
    assert mr.load_validator(test_invalid_validator) is None
    assert capsys.readouterr().out == 'Cannot load validator: ' + test_invalid_validator + '\n'

