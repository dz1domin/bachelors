from importlib import import_module
import glob
from pathlib import Path


class ModuleRunner:
    @staticmethod
    def run(runtimeOptions, moduleDefinition):
        module, method = load_module_and_method(moduleDefinition['info']['path'], moduleDefinition['methodToCall'])
        images = get_image_paths(runtimeOptions['path'], runtimeOptions['recursive'])
        for gen in images:
            for image in gen:
                result = method(image, runtimeOptions)
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
