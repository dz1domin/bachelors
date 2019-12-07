import abc

class ActionInterface(abc.ABC):
    @staticmethod
    def do_action(moduleResult, runtimeOptions):
        pass
