from Actions.actioninterface import ActionInterface
import json


class Report(ActionInterface):
    def setup(self, runtimeOptions):
        self.collection = []
        self.clasifications = {}
        self.outFile = runtimeOptions['actionOut'] + '/report.json'

    def do_action(self, moduleResult, runtimeOptions):
        self.collection.append(moduleResult)
        if moduleResult[1] not in self.clasifications:
            self.clasifications[moduleResult[1]] = 1
        else:
            self.clasifications[moduleResult[1]] += 1

    def finish(self):
        self.collection.append(self.clasifications)
        with open(self.outFile, 'w') as file:
            json.dump(self.collection, file)