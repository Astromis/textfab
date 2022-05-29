from abc import abstractmethod, ABCMeta

class ProcessUnit(metaclass=ABCMeta):
    
    @abstractmethod
    def process(self, text:str) -> str:
        pass

    @classmethod
    def __str__(self):
        pass

class ParamProcessUnit(ProcessUnit):
    
    def __init__(self, param) -> None:
        super().__init__()
        self.param = param