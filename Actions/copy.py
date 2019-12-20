from Actions.actioninterface import ActionInterface
from shutil import copy2
import os


class Copy(ActionInterface):
    def setup(self, runtimeOptions):
        if not os.path.isdir(runtimeOptions['actionOut']):
            os.mkdir(runtimeOptions['actionOut'])

    def do_action(self, moduleResult, runtimeOptions):
        if not os.path.isdir(runtimeOptions['actionOut'] + '/' + moduleResult[1]):
            os.mkdir(runtimeOptions['actionOut'] + '/' + moduleResult[1])

        copy2(moduleResult[0], runtimeOptions['actionOut'] + '/' + moduleResult[1])
