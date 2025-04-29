from src.textfab.units import *
from textfab.fabric import Fabric


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
        assert (
            unit.process("Переменные могут быть categorical или continious")
            == "Переменные могут быть  или "
        )

    def test_remove_non_rus_alphabet(self):
        unit = remove_non_rus_alphabet()
        assert unit.process("Теst #2 для renive не cyrillic") == "Те  для  не "

    def test_remove_custom_regex(self):
        unit = remove_custom_regex({"regex": "[0-9]+"})
        assert (
            unit.process("This is 1st text since 1343 . It contains 323 signs")
            == "This is st text since  . It contains  signs"
        )

    def test_lemmatize_by_mystem(self):
        unit = lemmatize_by_mystem()
        assert (
            unit.process("Красивая мама красиво мыла раму")
            == "красивый мама красиво мыть рама\n"
        )

    def test_remove_emoji(self):
        unit = remove_emoji()
        assert unit.process("Привет😀") == "Привет"

    def test_remove_accents(self):
        unit = remove_accents()
        assert unit.process("Модерниза́ция") == "Модернизация"

    def test_emoji_tokenizer(self):
        unit = tokenize_with_emoji()
        assert unit.process("Привет!😀 Как дела?") == [
            "Привет",
            "!",
            "😀",
            "Как",
            "дела",
            "?",
        ]

    def test_tokenize_with_nltkr(self):
        unit = tokenize_with_nltk()
        assert unit.process("Привет! Как дела?") == ["Привет", "!", "Как", "дела", "?"]

    def test_segment_by_sentences(self):
        unit = segment_by_sentences({"language": "russian"})
        text = """<pa>Анализ численности КГМ проводили чашечным методом Коха, на среде СММ (среда для морских микроорганизмов) . 
        БГКП обнаруживали с использованием селективной среды Эндо. Определяли каталазоположительные, оксидазоотрицательные, грамотрицательные бактерии .  
        Наиболее вероятное количество бактерий отдельных физиологических групп – НО, ФД, ДТ оценивали на основе метода предельных разведений с 
        использованием элективной среды МКД, содержащей в качестве единственного источника углерода дизельное топливо, нефть, фенол в конечной концентрации 0.1% ."""
        assert unit.process(text) == [
            "<pa>Анализ численности КГМ проводили чашечным методом Коха, на среде СММ (среда для морских микроорганизмов) .",
            "БГКП обнаруживали с использованием селективной среды Эндо.",
            "Определяли каталазоположительные, оксидазоотрицательные, грамотрицательные бактерии .",
            "Наиболее вероятное количество бактерий отдельных физиологических групп – НО, ФД, ДТ оценивали на основе метода предельных разведений с \n        использованием элективной среды МКД, содержащей в качестве единственного источника углерода дизельное топливо, нефть, фенол в конечной концентрации 0.1% .",
        ]

    def test_remove_links(self):
        unit = remove_links()
        text = "привет. подпишись на https://github.com/Astromis/textfab/issues/10 и еще сюда https://www.google.com/search?q=dsf&sca_esv=595131700&source=hp&ei=S1KUZabvG4_BwPAP0dOHkAo&iflsig=AO6bgOgAAAAAZZRgWymwyPoYTEAdamM1XaAgdt6BMs60&ved=0ahUKEwjmwN-lp7-DAxWPIBAIHdHpAaIQ4dUDCAk&uact=5&oq=dsf&gs_lp=Egdnd3Mtd2l6IgNkc2YyCBAAGIAEGLEDMgUQLhiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESLwCUABYGHAAeACQAQCYAaMBoAG2AqoBAzIuMbgBA8gBAPgBAcICERAuGIAEGLEDGIMBGMcBGNEDwgILEAAYgAQYsQMYgwHCAggQLhiABBixA8ICBBAAGAPCAhcQLhiABBiKBRixAxiDARjHARivARiOBcICDhAuGIAEGLEDGMcBGNED&sclient=gws-wiz"
        assert unit.process(text) == "привет. подпишись на  и еще сюда "

    def test_remove_mobile_phone_numbers(self):
        unit = remove_mobile_phone_numbers()
        text = """89103123167|+7-910-221-22-22|+7(910)-221-22-22"""
        assert all([unit.process(x).strip() == "" for x in text.split("|")])

    def test_detokenize_with_space(self):
        unit = detokenize_with_space()
        text = ["part", "one", "part", "two"]
        assert "part one part two" == unit.process(text)

    def test_apply_butter_finger(self):
        unit = apply_butter_finger({"prob_token_pass": 0.5, "seed": 43})
        text = ["это", "тестовый", "набор", "для", "аугментаций"]
        assert ["это", "тестовай", "набон", "дтя", "аугментаций"] == unit.process(text)

    def test_apply_changing_token_char_case(self):
        unit = apply_changing_token_char_case({"try_numbers": 1, "seed": 42})
        text = ["это", "тестовый", "набор", "для", "аугментаций"]
        assert ["Это", "теСтОвыЙ", "набор", "для", "ауГМентаций"] == unit.process(text)

    def test_apply_apply_random_token_deletion(self):
        unit = apply_random_token_deletion({"try_numbers": 2, "seed": 43})
        text = ["это", "тестовый", "набор", "для", "аугментаций"]
        assert ["тестовый", "набор", "для"] == unit.process(text)

    def test_apply_random_token_swap(self):
        unit = apply_random_token_swap({"try_numbers": 1, "seed": 44})
        text = ["это", "тестовый", "набор", "для", "аугментаций"]
        assert ["это", "тестовый", "набор", "аугментаций", "для"] == unit.process(text)


def test_conv():
    config = [
        "swap_enter_to_space",
        "remove_punct",
        "collapse_spaces",
    ]
    conv = Fabric(config)
    assert conv(["This text, is\n\n for test"]) == ["This text is for test"]


def test_parralel_conv():
    config = [
        "swap_enter_to_space",
        "remove_punct",
        "collapse_spaces",
    ]
    conv = Fabric(config,)
    assert conv(
        [
            "This text, is\n\n for test",
            "This another text, is\n\n for test",
            "This yet another text, is\n\n for test",
        ],
        pool_size=5,
    ) == [
        "This text is for test",
        "This another text is for test",
        "This yet another text is for test",
    ]


def test_param_units():
    config = ["remove_punct", {"remove_custom_regex": {"regex": "a"}}]
    conv = Fabric(config)
    assert conv(["This is a test string."]) == ["This is  test string"]
