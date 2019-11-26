from importlib import import_module


class ModuleRunner:
    @staticmethod
    def run(runtimeOptions, moduleInfo):
        print(runtimeOptions, moduleInfo)
