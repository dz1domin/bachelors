from Actions.actioninterface import ActionInterface


class Print(ActionInterface):
    def do_action(self, moduleResult, runtimeOptions):
        print(moduleResult)
