from Actions.actioninterface import ActionInterface
import os

#TODO:figure out how to get image's thumbnail to save to a dir

class CopyMiniature(ActionInterface):
    def setup(self, runtimeOptions):
        if not os.path.isdir(runtimeOptions['actionOut']):
            os.mkdir(runtimeOptions['actionOut'])

    def do_action(self, moduleResult, runtimeOptions):
        if not os.path.isdir(runtimeOptions['actionOut'] + '/' + moduleResult[1]):
            os.mkdir(runtimeOptions['actionOut'] + '/' + moduleResult[1])

        # copy2(moduleResult[0], runtimeOptions['actionOut'] + '/' + moduleResult[1])
