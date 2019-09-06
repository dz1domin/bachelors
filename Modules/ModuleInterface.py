# History of changes
# Version - Author - Change
# v1        Dominik   Initial version
import abc


class ModuleInterface(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process(options):
        pass
