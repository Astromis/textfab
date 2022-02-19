from abc import abstractmethod, ABCMeta
from string import punctuation 
import re

class ProcessUnit(metaclass=ABCMeta):
    
    @abstractmethod
    def process(self, text:str) -> str:
        pass

    @classmethod
    def __str__(self):
        pass

class remove_punct(ProcessUnit):
    def process(self, text: str) -> str:
        return ''.join([x for x in text if x not in punctuation])
    
    def __str__(self):
        return "remove_punct"

class swap_enter_to_space(ProcessUnit):
    def process(self, text: str) -> str:
        return text.replace("\n", ' ')

    def __str__(self):
        return "swap_enter_to_space"
    
class collapse_spaces(ProcessUnit):
    def process(self, text: str) -> str:
        return re.sub(r"[ ]{2,}", " ", text)
    
    def __str__(self):
        return "collapse_spaces"

class lower_string(ProcessUnit):
    def process(self, text: str) -> str:
        return text.lower()
    
    def __str__(self):
        return "lower_string"

class strip_string(ProcessUnit):
    def process(self, text: str) -> str:
        return text.strip()
    
    def __str__(self):
        return "strip_string"
    
class remove_latin(ProcessUnit):
    def process(self, text:str) -> str:
        return re.sub("[A-Za-z]+", '', text)
    
    def __str__(self):
        return "remove_latin"
    
class remove_non_cyrillic(ProcessUnit):
    def process(self, text:str) -> str:
        return re.sub("[^А-Яа-я \-\,\.\;\:]+", '', text)
    
    def __str__(self):
        return "remove_non_cyrillic"
