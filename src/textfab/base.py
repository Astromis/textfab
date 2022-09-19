from abc import abstractmethod, ABCMeta

class ProcessUnit(metaclass=ABCMeta):
    
    @abstractmethod
    def process(self, text:str) -> str:
        pass

    @classmethod
    def __str__(self):
        pass

class ChangingProcessUnit(ProcessUnit):
    
    @abstractmethod
    def process(self, text: str) -> None:
        ...

class ParamChangingProcessUnit(ChangingProcessUnit):
    
    def __init__(self, param: list) -> None:
        super().__init__()
        self.param = param

class ParamProcessUnit(ProcessUnit):
    
    def __init__(self, param: list) -> None:
        super().__init__()
        self.param = param