from Actions.actioninterface import ActionInterface
import json


class Report(ActionInterface):
    def __init__(self):
        self.collection = []
        self.classifications = {}
        self.outFile = ""

    def setup(self, runtimeOptions):
        self.outFile = runtimeOptions['actionOut'] + '/report.json'

    def do_action(self, moduleResult, runtimeOptions):
        self.collection.append(moduleResult)
        if moduleResult[1] not in self.classifications:
            self.classifications[moduleResult[1]] = 1
        else:
            self.classifications[moduleResult[1]] += 1

    def finish(self):
        self.collection.append(self.classifications)
        with open(self.outFile, 'w') as file:
            json.dump(self.collection, file)