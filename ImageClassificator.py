#! /usr/bin/env python3
# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
from importlib import import_module
import json
from ModuleRunner import ModuleRunner


def main():
    parser = argparse.ArgumentParser(description='This is a program for classifying images and verifying different methods of doing so.')

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
