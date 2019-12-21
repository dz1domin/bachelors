import pytest
import os
import sys
import inspect
import glob
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_path)

import Validators.Validator as v
import Validators.BlurValidator as bv
import abc

def test_load_and_parse_data(capsys):

    extension, imges = bv.BlurValidator._load_and_parse_data(os.path.dirname(os.path.abspath(__file__)) + '/BlurValidator_files/test.xlsx')
    assert extension == 'xlsx'
    assert imges is not None
    assert len(imges) == 3
    
    extension, imges = bv.BlurValidator._load_and_parse_data(os.path.dirname(os.path.abspath(__file__)) + '/BlurValidator_files/test.json')
    assert extension == 'json'
    assert imges is not None
    assert len(imges) == 3
    
    extension, imges = bv.BlurValidator._load_and_parse_data(os.path.dirname(os.path.abspath(__file__)) + '/BlurValidator_files/test.xml')
    assert extension == 'xml'
    assert imges is not None
    assert len(imges) == 3

    extension, imges = bv.BlurValidator._load_and_parse_data(os.path.dirname(os.path.abspath(__file__)) + '/BlurValidator_files/test.txt')
    assert extension is None
    assert imges is None
    assert capsys.readouterr().out == 'Not supported file format: txt\n'

def test_generate_raport(capsys):
    
    data = [['img1', 1, 1], ['img2', 1, 2]]

    for extension in ['xlsx', 'json', 'xml']:
        bv.BlurValidator._generate_raport(data, extension)

        assert os.path.isfile('validation_result.' + extension)
        os.remove('validation_result.' + extension)
        assert not os.path.isfile('validation_result.' + extension)

    bv.BlurValidator._generate_raport(data, 'txt')
    assert capsys.readouterr().out == 'Not supported file format: txt\n'

    
def test_extract_only_name():

    assert bv.BlurValidator._extract_only_name("/dir1/dir2/file.jpg") == 'file.jpg'
    assert bv.BlurValidator._extract_only_name("\\dir1/dir2\\file.jpg") == 'file.jpg'

def test_validate():


    validation_file = os.path.dirname(os.path.abspath(__file__)) + '/BlurValidator_files/test.json'
    module_results = [[ "Original_2.jpg", 0 ], [ "Original_3.jpg", 0 ], [ "Original_4.jpg", 0 ]]
    bv.BlurValidator.validate(validation_file, module_results, {})

    result_file = 'validation_result.json'
    assert os.path.isfile(result_file)
    os.remove(result_file)
