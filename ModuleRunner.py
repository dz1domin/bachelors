from importlib import import_module
import glob
from pathlib import Path


class ModuleRunner:
    @staticmethod
    def run(runtimeOptions, moduleDefinition):
        print(runtimeOptions)
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
                    print(result)


def load_module_and_method(modulePath, methodToCall):
    module = import_module(modulePath)
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
