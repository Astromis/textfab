from textfab.units import *
from textfab.manager import Conveyer

class TestUnits:

    def test_punck_remove(self):
        unit = remove_punct()
        assert unit.process("test, case") == "test case"

    def test_enter_to_space(self):
        unit = swap_enter_to_space()
        assert unit.process("test\ncase") == "test case"

    def test_swap_enter_to_sapce(self):
        unit = collapse_spaces()
        assert unit.process("test    case") == "test case"
        
    def test_remove_latin(self):
        unit = remove_latin()
        assert unit.process("Переменные могут быть categorical или continious") == "Переменные могут быть  или "

    def test_remove_non_cyrillic(self):
        unit = remove_non_cyrillic()
        assert unit.process("Теst #2 для renive не cyrillic") == "Те  для  не "

    def test_remove_custom_regex(self):
        unit = remove_custom_regex(["[0-9]+"])
        assert unit.process("This is 1st text since 1343 . It contains 323 signs") == "This is st text since  . It contains  signs"

    def test_lemmatize_by_mystem(self):
        unit = lemmatize_by_mystem()
        assert unit.process("Красивая мама красиво мыла раму") == "красивый мама красиво мыть рама\n"

    def test_remove_emoji(self):
        unit = remove_emoji()
        assert unit.process("Привет😀") == 'Привет'

    def test_remove_accents(self):
        unit = remove_accents()
        assert unit.process("Модерниза́ция") == 'Модернизация'

def test_conv():
    config = ["swap_enter_to_space", "remove_punct", "collapse_spaces",]
    conv = Conveyer(config)
    assert conv.start(["This text, is\n\n for test"]) == ["This text is for test"]

def test_parralel_conv():
    config = ["swap_enter_to_space", "remove_punct", "collapse_spaces",]
    conv = Conveyer(config, )
    assert conv.start(["This text, is\n\n for test", "This another text, is\n\n for test", "This yet another text, is\n\n for test"], pool_size=5) == ["This text is for test", "This another text is for test", "This yet another text is for test"]


def test_param_units():
    config = ["remove_punct", ("remove_custom_regex", "a")]
    conv = Conveyer(config)
    assert conv.start(["This is a test string."]) == ["This is  test string"] 
