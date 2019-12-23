import pytest
import os
import sys
import jsonschema
import json
from argparse import ArgumentParser
from pathlib import Path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
import ImageClassificator as ic


@pytest.fixture
def test_make_fixture():
    options = ['path', 'recursive', 'validation', 'validator', 'action', 'actionOut', 'moduleName']
    definition_schema = json.loads("""
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "moduleDefinitionsSchema",
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "methodToCall": {"type": "string"},
    "info":{
      "type": "object",
      "properties": {
        "path": {"type": "string"},
        "formats": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "help": {"type": "string"},
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "patternProperties": {
              "^(option|help|required|action|nargs|const|default|type|choices|metavar|dest)": {
                
              }
            }
          }
        }
      }
    }
  }
}
    """)

    dummy_def = """
{
  "name": "test",
  "methodToCall": "test",
  "info": {
    "path": "Modules.test.test",
    "options": [
      {
        "option": "-test",
        "required": "true",
        "default": 12123
      }
    ],
    "help": "This module uses variation of Laplacian to determine whether image is blurred."
  }
}
    """

    return options, definition_schema, dummy_def


def test_create_base_parser():
    parser = ic.create_base_parser()
    parsed = parser.parse_args(['-p', 'some_path'])
    assert isinstance(parser, ArgumentParser)
    assert parsed.path == 'some_path'


def test_load_module_definitions(test_make_fixture):
    definitions = ic.load_module_definitions('../Modules')
    for definition in definitions:
        assert jsonschema.validate(definition, test_make_fixture[1]) is None


def test_load_global_config(test_make_fixture):
    config = ic.load_global_config(str(Path(os.path.dirname(os.path.abspath(__file__))).parent) + str(Path('/defaultConfig.json')))
    assert isinstance(config, dict)
    for key in config.keys():
        assert key in test_make_fixture[0]


def test_add_module_defualt_values(test_make_fixture):
    options = {}
    assert bool(options) is False
    ic.add_default_module_values(json.loads(test_make_fixture[2]), options)
    assert options['test'] == 12123
    options = {'path': './Images', 'recursive': False, 'validation': None, 'validator': None, 'action': 'print', 'actionOut': './Output', 'moduleName': 'test', 'test': '10'}
    print(options['test'])
    ic.add_default_module_values(json.loads(test_make_fixture[2]), options)
    assert options['test'] == '10'

