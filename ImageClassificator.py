#! /usr/bin/env python3
# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
import json
from ModuleRunner import Runner
import jsonschema
from pathlib import Path


schema_string = """
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
      },
      "required": ["path"]
    }
  },
  "required": ["name", "methodToCall"]
}
"""


def main():
    # options for overall program
    parser = create_base_parser()

    # loading module definitions
    moduleDefinitions = load_module_definitions()

    # validating loaded module definitions to fit schema
    for definition in moduleDefinitions:
        jsonschema.validate(definition, json.loads(schema_string))

    subparsers = parser.add_subparsers(dest='moduleName')
    for definition in moduleDefinitions:
        sub = subparsers.add_parser(definition['name'], help=definition['info']['help'])
        for arg in definition['info']['options']:
            optionName = arg['option']
            del arg['option']
            sub.add_argument(optionName, **arg)
            arg['option'] = optionName

    options = parser.parse_args()
    optionsDict = vars(options)
    defaultConfig = load_global_config()

    for key in defaultConfig.keys():
        if key not in optionsDict or not optionsDict[key]:
            optionsDict[key] = defaultConfig[key]

    classificationResult = None

    for definition in moduleDefinitions:
        if definition['name'] == optionsDict['moduleName']:
            add_default_module_values(definition, optionsDict)
            classificationResult = Runner.runModule(optionsDict, definition)
            
    if should_run_validation(optionsDict):
        Runner.runValidator(optionsDict, classificationResult)


def create_base_parser():
    parser = argparse.ArgumentParser(
        description='This is a program for classifying images and verifying different methods of doing so.')

    parser.add_argument('-p', '--path', help='This defines the path to the images.', type=str)
    parser.add_argument('-r', '--recursive',
                        help='This defines if image search is limited to directory passed in the path variable.',
                        action='store_true')
    parser.add_argument('-v', '--validation',
                        help='This variable can contain path to supported file to validate module output.',
                        type=str)
    parser.add_argument('-z', '--validator', help="This variable can contain path to validating module.",
                        type=str)
    parser.add_argument('-a', '--action',
                        help="This variable specifies what action to take when image has received its classification.",
                        type=str)
    parser.add_argument('-o', '--actionOut',
                        help="This variable specifies path at which output from chosen action will be saved.",
                        type=str)
    return parser


def load_global_config(pathToConfig = './defaultConfig.json'):
    result = None
    with open(pathToConfig, 'r') as file:
         result = json.load(file)
    return result


def load_module_definitions(pathToDefs = './Modules'):
    result = []
    moduleDefinitionPathGen = Path(pathToDefs).glob('*/moduleDefinition.json')
    for p in moduleDefinitionPathGen:
        with open(p, 'r') as file:
            definition = json.load(file)
        result.append(definition)
    return result

def should_run_validation(options):
    return options['validator'] is not None and options['validation'] is not None


def add_default_module_values(moduleDefinition, optionsDict):
    for option in moduleDefinition['info']['options']:
        if option['option'].split('-')[-1] not in optionsDict or optionsDict[option['option'].split('-')[-1]] is None:
            optionsDict[option['option'].split('-')[-1]] = option['default'] if 'default' in option.keys() else None


if __name__ == "__main__":
    main()