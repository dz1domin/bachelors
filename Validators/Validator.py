import abc

class Validator(abc.ABC):
    @abc.abstractstaticmethod
    def validate(validationFile, moduleResults, moduleOptions):
        pass
