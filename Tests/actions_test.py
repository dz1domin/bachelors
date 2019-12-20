import os
import sys
import pytest
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from Tests.Module import method
from Actions.print import Print
from Actions.copy import Copy
from Actions.report import Report
from Actions.actioninterface import ActionInterface
from PIL import Image


@pytest.fixture
def runtime_fixture():
    runtime_options = {'actionOut': './TestsOut'}
    return runtime_options


def test_print():
    print_obj = Print()
    assert isinstance(print_obj, ActionInterface)


def test_copy(runtime_fixture):
    img = Image.open('./TestImage/testImage.jpg')
    copy_obj = Copy()
    assert isinstance(copy_obj, ActionInterface)
    copy_obj.setup(runtime_fixture)
    assert os.path.isdir('./TestsOut')
    copy_obj.do_action(method('./TestImage/testImage.jpg', runtime_fixture), runtime_fixture)
    assert os.path.isdir('./TestsOut/test')
    assert os.path.isfile('./TestsOut/test/testImage.jpg')
    img2 = Image.open('./TestsOut/test/testImage.jpg')
    assert img.size == img2.size


def test_report(runtime_fixture):
    report_obj = Report()
    assert isinstance(report_obj, ActionInterface)
    report_obj.setup(runtime_fixture)
    report_obj.do_action(method('./TestImage/testImage.jpg', runtime_fixture), runtime_fixture)
    report_obj.finish(runtime_fixture)
    assert os.path.isfile('./TestsOut/report.json')
