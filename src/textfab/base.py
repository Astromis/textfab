from typing import Dict, Any, Union, List
from abc import abstractmethod, ABCMeta


class ProcessUnit(metaclass=ABCMeta):
    """Allow processing without object modification."""

    @abstractmethod
    def process(self, text: str) -> str:
        pass

    @classmethod
    def __str__(self):
        pass


class ChangingProcessUnit(ProcessUnit):
    """Allow a processing with object changes.

    The parameters go as a dictionary. The params must be described 
    in doc of the unit.
    """

    @abstractmethod
    def process(self, text: Union[str, List[str], Any]) -> Any:
        ...


class ParamChangingProcessUnit(ChangingProcessUnit):
    """Allow parametrized processing with object changes.

    The parameters go as a dictionary. The params must be described 
    in doc of the unit.
    """

    def __init__(self, param: Dict[str, Any]) -> None:
        super().__init__()
        self.param = param


class ParamProcessUnit(ProcessUnit):
    """Allow parametrized processing without object modification."""

    def __init__(self, param: Dict[str, Any]) -> None:
        super().__init__()
        self.param = param
