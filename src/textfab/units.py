import re
import unicodedata

from string import punctuation 
from pymystem3 import Mystem

from .base import ProcessUnit
from .base import ParamProcessUnit

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

class remove_custom_regex(ParamProcessUnit):
    
    def process(self, text: str) -> str:
        if len(self.param) > 1:
            raise ValueError(f"Too many parameterfs for {self.__str__()} unit")
        return re.sub(*self.param, "", text)

    def __str__(self):
        return f"remove_custom_regex:{self.param}"

class lemmatize_by_mystem(ProcessUnit):
    def __init__(self) -> None:
        self.stemmer = Mystem()

    def process(self, text: str) -> str:
        return "".join(self.stemmer.lemmatize(text))

    def __str__(self):
        return "lemmatize_by_mystem"

class remove_emoji(ProcessUnit):
    def __init__(self):
        self.emoji_pattern = re.compile(u"(["                 # .* removed
                                    u"\U00010000-\U0001FFFF"
                                    u"\U0000200D"
                                    #u"\U0001F600-\U0001F64F"  # emoticons
                                    #u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                    #u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                    #u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                    "])", flags= re.UNICODE)
    
    def process(self, text: str) -> str:
        
        return re.sub(self.emoji_pattern, '', text)

    def __str__(self):
        return "remove_emoji"

class remove_accents(ProcessUnit):
    def process(self, text: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                    if unicodedata.category(c) != 'Mn')
    def __str__(self):
        return "remove_accents"
