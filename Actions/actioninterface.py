import abc


class ActionInterface(abc.ABC):
    def do_action(self, moduleResult, runtimeOptions):
        pass

    def setup(self, runtimeOptions):
        pass

    def finish(self, runtimeOptions):
        pass