from importlib import import_module
import inspect
from pathlib import Path


class ModuleRunner:
    @staticmethod
    def run(runtimeOptions, moduleDefinition):
        action_obj = load_action(runtimeOptions)
        action_obj.setup(runtimeOptions)
        _, method = load_module_and_method(moduleDefinition['info']['path'], moduleDefinition['methodToCall'])

        if runtimeOptions['validation'] is not None:
            if runtimeOptions['validator'] is not None:
                validator =  import_module(runtimeOptions['validator'])
                validator.validate(runtimeOptions['validation'], method, runtimeOptions)
        else:
            images = get_image_paths(runtimeOptions['path'], runtimeOptions['recursive'])
            for gen in images:
                for image in gen:
                    #str(image) is required for multiplatform, because it was detected as "WindowsPath" on windows, and then there was a type conflict :^)
                    result = method(str(image), runtimeOptions)
                    action_obj.do_action(result, runtimeOptions)

        action_obj.finish()


def load_module_and_method(modulePath, methodToCall):
    module = None
    try:
        module = import_module(modulePath)
    except ModuleNotFoundError:
        exit(-1)
    method = getattr(module, methodToCall)
    return module, method


def get_image_paths(path, isRecursive):
    formatPatterns = ['*.bmp', '*.pbm', '*.pgm', '*.ppm', '*.sr', '*.ras', '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.tiff', '*.tif', '*.png']
    result = None
    if isRecursive:
        for pattern in formatPatterns:
            if isinstance(result, list):
                result.append(Path(path).rglob(pattern))
            else:
                result = list(Path(path).rglob(pattern))
    else:
        for pattern in formatPatterns:
            if isinstance(result, list):
                result.append(Path(path).glob(pattern))
            else:
                result = list(Path(path).glob(pattern))
    return result


def load_action(runtimeOptions):
    module = None
    try:
        module = import_module('Actions.{}'.format(runtimeOptions['action']))
    except ModuleNotFoundError:
        exit(-1)
    action_class = None
    for el in inspect.getmembers(module, inspect.isclass):
        if el[0].casefold() == runtimeOptions['action']:
            action_class = getattr(module, el[0])
            return action_class()
    return None
