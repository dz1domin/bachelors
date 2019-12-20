import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import ModuleRunner as mr
from Actions.actioninterface import ActionInterface


def test_print():
    print_obj = mr.load_action('print')
    print_obj.do_action('test', {})
    assert isinstance(print_obj, ActionInterface)