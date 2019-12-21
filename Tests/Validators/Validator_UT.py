import pytest
import os
import sys
import inspect
import glob
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)
sys.path.append(base_path + '/Validators/')
import Validators.Validator as v
import abc
from importlib import import_module

def test_validator():

    list_with_class = inspect.getmembers(v, inspect.isclass)
    assert len(list_with_class) == 1

    class_name, class_obj = list_with_class[0]

    assert class_name == 'Validator'
    assert issubclass(class_obj, abc.ABC)

    list_with_method = inspect.getmembers(class_obj, inspect.isfunction)
    assert len(list_with_method) == 1

    method_name, method_obj = list_with_method[0]

    assert method_name == 'validate'
    assert getattr(method_obj, '__isabstractmethod__')

def test_validators():

    os.chdir(base_path + '/Validators/')
    modules = glob.glob("*.py")
    modules.remove('Validator.py')

    for module_name in modules:
        
        module = import_module(module_name.split('.')[0])
        
        main_class_found = False

        list_with_class = inspect.getmembers(module, inspect.isclass)
        for class_name, class_obj in list_with_class:
            if class_name == module_name.split('.')[0]:
                
                main_class_found = True
                main_function_found = False

                list_with_method = inspect.getmembers(class_obj, inspect.isfunction)
                for method_name, _ in list_with_method:
                    if method_name == 'validate':
                        main_function_found = True
                        break

                assert main_function_found
                break
        
        assert main_class_found

