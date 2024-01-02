import re
from typing import List
import unicodedata

from string import punctuation 

from .base import ProcessUnit
from .base import ParamProcessUnit
from .base import ChangingProcessUnit
from .base import ParamChangingProcessUnit

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
        from pymystem3 import Mystem
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

class tokenize_with_emoji(ChangingProcessUnit):
    """Tokenize text string with socnet specific objects like emoji or emoticons
    """
    def __init__(self) -> None:
        super().__init__()
        from .emoji_tokenizer import tokenize
        self.tokenize = tokenize

    def process(self, text: str) -> List[str]:
        return self.tokenize(text)

    def __str__(self,):
        return "tokenizer_with_emoji"

class tokenize_with_nltk(ChangingProcessUnit):
    """Tokenize text with nltk.word_tokenize
    """
    def __init__(self) -> None:
        super().__init__()
        from nltk import word_tokenize
        self.tokenize = word_tokenize
    
    def process(self, text: str) -> List[str]:
        return self.tokenize(text)

    def __str__(self,):
        return "tokenize_with_nltk"

class segment_by_sentences(ParamChangingProcessUnit):
    """Segment text by the sentences with nltk.sent_tokenize
    """
    def __init__(self, param) -> None:
        """
        Args:
            param (str): language parameter for sent_tokenize
        """
        super().__init__(param)
        self.param = param
        from nltk import sent_tokenize
        self.tokenize = sent_tokenize

    def process(self, text: str) -> List[str]:
        return self.tokenize(text, *self.param)
    
class remove_links(ProcessUnit):
    """Remove any links from text."""
    def __init__(self) -> None:
        super().__init__()
        self.link_regex = re.compile("(https?://)?([\da-z.-]+).([a-z.]{2,6})([/\w.-?&\-\#]*)")

    def process(self, text: str) -> str:
        return self.link_regex.sub("", text)
        
class remove_mobile_phone_numbers(ProcessUnit):
    """Remove mobile phone numbers from text."""

    def __init__(self) -> None:
        super().__init__()
        self.phone_number_regex = re.compile("^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$")

    def process(self, text: str) -> str:
        return self.phone_number_regex.sub("", text)