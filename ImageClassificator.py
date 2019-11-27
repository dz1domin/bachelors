#! /usr/bin/env python3
# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
import json
from ModuleRunner import ModuleRunner


def main():
    parser = argparse.ArgumentParser(description='This is a program for classifying images and verifying different methods of doing so.')

    parser.add_argument('-p', '--path', help='This defines the path to the images.', default='.', type=str)
    parser.add_argument('-r', '--recursive',
                        help='This defines if image search is limited to directory passed in the path variable.',
                        default=False, action='store_true')
    parser.add_argument('-v', '--validation', help='This variable can contain path to supported file to validate module output.',
                        default=None, type=str)

    moduleDefinitions = None
    with open('moduleDefinitions.json') as moduleDefinitionsFile:
        moduleDefinitions = json.load(moduleDefinitionsFile)

    subparsers = parser.add_subparsers()
    for (moduleName, moduleInfo) in moduleDefinitions.items():
        sub = subparsers.add_parser(moduleName, help=moduleInfo['info']['help'])
        for arg in moduleInfo['info']['options']:
            sub.add_argument(arg['option'], help=arg['help'])
        sub.set_defaults(which=moduleName)

    options = parser.parse_args()
    optionsDict = vars(options)
    if not optionsDict:
        pass
        # brak opcji, jak będzie trzeba bedzie tutaj gui uruchamiane
    else:
        if optionsDict['which'] in moduleDefinitions:
            ModuleRunner.run(optionsDict, moduleDefinitions[optionsDict['which']])


if __name__ == "__main__":
    main()
