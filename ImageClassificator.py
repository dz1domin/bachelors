#! /usr/bin/env python3
# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
import json
from ModuleRunner import ModuleRunner
import jsonschema


schema_string = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "moduleDefinitionsSchema",
  "type": "object",
  "patternProperties": {
  	"[A-Za-z]+": {
      "type": "object",
      "properties": {
      	"methodToCall": {"type": "string"},
        "info": {
          "type": "object",
          "properties": {
            "path": {"type": "string"},
            "options": {
              "type": "array",
              "items": {
                "type": "object",
                "patternProperties": {
                  "^(option|help|required|action|nargs|const|default|type|choices|metavar|dest)": {
                    "type": "string"
                  }
                },
                "required": ["option"]
              }
            },
            "help": {"type": "string"}
          },
          "required": ["path", "options", "help"]
        }
      },
      "required": ["methodToCall", "info"]
    }
  }
}
"""


def main():
    # options for overall program
    parser = argparse.ArgumentParser(description='This is a program for classifying images and verifying different methods of doing so.')

    parser.add_argument('-p', '--path', help='This defines the path to the images.', default='.', type=str)
    parser.add_argument('-r', '--recursive',
                        help='This defines if image search is limited to directory passed in the path variable.',
                        default=False, action='store_true')
    parser.add_argument('-v', '--validation', help='This variable can contain path to supported file to validate module output.',
                        default=None, type=str)

    # loading module definitions
    moduleDefinitions = None
    with open('moduleDefinitions.json') as moduleDefinitionsFile:
        moduleDefinitions = json.load(moduleDefinitionsFile)

    # validating loaded module definitions to fit schema
    jsonschema.validate(moduleDefinitions, json.loads(schema_string))

    subparsers = parser.add_subparsers(dest = "moduleName", required=True)
    for (moduleName, moduleInfo) in moduleDefinitions.items():
        sub = subparsers.add_parser(moduleName, help=moduleInfo['info']['help'])
        for arg in moduleInfo['info']['options']:
            optionName = arg['option']
            del arg['option']
            sub.add_argument(optionName, **arg)

    options = parser.parse_args()
    optionsDict = vars(options)

    if not optionsDict:
        pass
        # no options, gui might be launched from here in the future
    else:
        ModuleRunner.run(optionsDict, moduleDefinitions[optionsDict['moduleName']])


if __name__ == "__main__":
    main()