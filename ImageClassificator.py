#! /usr/bin/env python3
# @author Dominik Dziuba
# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import argparse
from importlib import import_module
import json
from ModuleRunner import ModuleRunner


def dynamic_load(moduleInfo):
    return import_module(moduleInfo['info']['path'])


def main():
    parser = argparse.ArgumentParser(description='This is a program for classifying images and verifying different methods of doing so.')

    moduleDefinitions = None
    with open('moduleDefinitions.json') as moduleDefinitionsFile:
        moduleDefinitions = json.load(moduleDefinitionsFile)

    subparsers = parser.add_subparsers()
    for moduleDefinition in moduleDefinitions:
        sub = subparsers.add_parser(moduleDefinition['name'], help=moduleDefinition['info']['help'])
        for arg in moduleDefinition['info']['options']:
            sub.add_argument(arg['option'], help=arg['help'])
        sub.set_defaults(which=moduleDefinition['name'])

    options = parser.parse_args()
    optionsDict = vars(options)
    if not optionsDict:
        pass
        # brak opcji, jak będzie trzeba bedzie tutaj gui uruchamiane
    else:
        for module in moduleDefinitions:
            if module['name'] == optionsDict['which']:
                ModuleRunner.run(optionsDict, module)
                break


if __name__ == "__main__":
    main()
