from importlib import import_module
import inspect
from pathlib import Path
from Validators.Validator import Validator


class Runner:
    @staticmethod
    def runModule(runtimeOptions, moduleDefinition):
        action_obj = load_action(runtimeOptions['action'])
        action_obj.setup(runtimeOptions)
        _, method = load_module_and_method(moduleDefinition['info']['path'], moduleDefinition['methodToCall'])

        images = get_image_paths(runtimeOptions['path'], runtimeOptions['recursive'], moduleDefinition['info']['formats'])
        all_results = []
        for gen in images:
            for image in gen:
                result = method(str(image), runtimeOptions)
                all_results.append(result)
                action_obj.do_action(result, runtimeOptions)
                
        action_obj.finish(runtimeOptions)
        return all_results

    @staticmethod
    def runValidator(runtimeOptions, moduleResults):
        validator_class = load_validator(runtimeOptions['validator'])
        if validator_class is not None:
            validator_class.validate(runtimeOptions['validation'], moduleResults, runtimeOptions)
    

def load_module_and_method(modulePath, methodToCall):
    module = None
    try:
        module = import_module(modulePath)
    except ModuleNotFoundError:
        exit(-1)
    method = getattr(module, methodToCall)
    return module, method


def get_image_paths(path, isRecursive, formatPatterns = []):
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


def load_action(action):
    module = None
    try:
        module = import_module('Actions.{}'.format(action))
    except ModuleNotFoundError:
        exit(-1)

    for el in inspect.getmembers(module, inspect.isclass):
        if el[0].casefold() == action:
            action_class = getattr(module, el[0])
            return action_class()
    return None


def load_validator(validator):
    try:
        module = import_module('Validators.{}'.format(validator))
        for class_name, class_obj in inspect.getmembers(module, inspect.isclass):
            if class_name == validator:
                if issubclass(class_obj, Validator):
                    return class_obj
        
    except ModuleNotFoundError:
        print("Cannot load validator: " + validator)

    return None
