from ..text_conveyer.units import *
from ..text_conveyer.manager import Conveyer

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


def test_conv():
    config = ["swap_enter_to_space", "remove_punct", "collapse_spaces",]
    conv = Conveyer(config)
    assert conv.start(["This text, is\n\n for test"]) == ["This text is for test"]

def test_parralel_conv():
    config = ["swap_enter_to_space", "remove_punct", "collapse_spaces",]
    conv = Conveyer(config, )
    assert conv.start(["This text, is\n\n for test", "This another text, is\n\n for test", "This yet another text, is\n\n for test"], pool_size=5) == ["This text is for test", "This another text is for test", "This yet another text is for test"]



