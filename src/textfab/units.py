import re
import unicodedata

from string import punctuation 
from pymystem3 import Mystem

from .base import ProcessUnit
from .base import ParamProcessUnit

class remove_punct(ProcessUnit):
    """
    Remove all punctuation that listed in a same named module.
    """
    def process(self, text: str) -> str:
        return ''.join([x for x in text if x not in punctuation])
    
    def __str__(self):
        return "remove_punct"

class swap_enter_to_space(ProcessUnit):
    """
    Replace any \\n symbol on space
    """
    def process(self, text: str) -> str:
        return text.replace("\n", ' ')

    def __str__(self):
        return "swap_enter_to_space"
    
class collapse_spaces(ProcessUnit):
    """
    Replace multiple spaces to one.
    """
    def process(self, text: str) -> str:
        return re.sub(r"[ ]{2,}", " ", text)
    
    def __str__(self):
        return "collapse_spaces"

class lower_string(ProcessUnit):
    '''
    Make any string to low level
    '''
    def process(self, text: str) -> str:
        return text.lower()
    
    def __str__(self):
        return "lower_string"

class strip_string(ProcessUnit):
    '''
    Remove spaces at the beginning and at the end of the string
    '''
    def process(self, text: str) -> str:
        return text.strip()
    
    def __str__(self):
        return "strip_string"
    
class remove_latin(ProcessUnit):
    """
    Remove any latin characters in string
    """
    def process(self, text:str) -> str:
        return re.sub("[A-Za-z]+", '', text)
    
    def __str__(self):
        return "remove_latin"
    
class remove_non_cyrillic(ProcessUnit):
    """
    Remove any non-cyrillic characters in string
    """
    def process(self, text:str) -> str:
        return re.sub("[^А-Яа-я \-\,\.\;\:]+", '', text)
    
    def __str__(self):
        return "remove_non_cyrillic"

class remove_custom_regex(ParamProcessUnit):
    """
    Allows to define a custom regex for substitution
    """
    def process(self, text: str) -> str:
        if len(self.param) > 1:
            raise ValueError(f"Too many parameterfs for {self.__str__()} unit")
        return re.sub(*self.param, "", text)

    def __str__(self):
        return f"remove_custom_regex:{self.param}"

class lemmatize_by_mystem(ProcessUnit):
    """
    Lemmatize all words in the string with pymystem3
    """
    def __init__(self) -> None:
        self.stemmer = Mystem()

    def process(self, text: str) -> str:
        return "".join(self.stemmer.lemmatize(text))

    def __str__(self):
        return "lemmatize_by_mystem"

class remove_emoji(ProcessUnit):
    """
    Remove all emojis from UTF-8
    """
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
    """
    Remove accent symbolо́
    """
    def process(self, text: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFD', text)
                    if unicodedata.category(c) != 'Mn')
    def __str__(self):
        return "remove_accents"
