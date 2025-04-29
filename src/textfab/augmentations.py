"""From https://github.com/RussianNLP/rutransform/tree/main"""

from typing import List, Optional
import random
from copy import deepcopy
from nltk.corpus import stopwords

STOPWORDS = stopwords.words("russian")


def butter_finger(
    text: List[str],
    prob: float = 0.1,
    prob_token_pass: float = 0.1,
    try_numbers: int = 1,
    stop_words: List[str] = [],
    seed: Optional[int] = None,
) -> List[str]:
    """
    Adds typos to text the sentence using keyboard distance

    Parameters
    ----------
    text: List[str]
        text to transform
    prob: float
        probability of the transformation (default is 0.1)
    prob_token_pass: float
        probability of the transformation of the particular token (default is 0.1)
    seed: int
        seed to freeze everything (default is 42)
    try_numbers: int
        how much the transformation is applied (default is 1)
    stop_words: List[int], optional
        stop words to ignore during transformation (default is None)

    Returns
    -------
    List[str]
        list of transformed sentences
    """
    if seed is not None:
        random.seed(seed)
    key_approx = {
        "й": "йцфыувяч",
        "ц": "цйуыфвкасч",
        "у": "уцкыавйфячсмпе",
        "к": "куевпацычсмпе",
        "е": "екнарпувсмитог",
        "н": "негпоркамитош",
        "г": "гншрлоепитьдщ",
        "ш": "шгщодлнртьдз",
        "щ": "щшзлдгоь",
        "з": "здщхэшл",
        "х": "хзъэж\щдю.",
        "ъ": "ъх\зэж.",
        "ф": "фйыяцчцвсу",
        "ы": "ыцчфвкам",
        "в": "вусыафйпим",
        "а": "авпкмцычнрт",
        "п": "пеиарувснот",
        "р": "рнтпоакмлшь",
        "о": "орлтгпеидщь",
        "л": "лодштнрт",
        "д": "дщльзгот",
        "ж": "жз.дэх\ю",
        "э": "эхж\зъ.",
        "я": "яфчымву",
        "ч": "чясывимакуцй",
        "с": "счмваяыцукпи",
        "м": "мсаипчвукент",
        "и": "имтпрсаенгт",
        "т": "тиьромпегшл",
        "ь": "ьтлодщшл",
        "б": "блдьюож",
        "ю": "юджб.ьл",
        " ": " ",
    }
    if stop_words is None:
        stop_words = []

    transformed_texts = deepcopy(text)
    for _ in range(try_numbers):
        for i, word in enumerate(text):
            if random.uniform(0, 1) <= prob_token_pass:
                transformed_texts[i] = word
            elif word in stop_words:
                transformed_texts[i] = word
            else:
                new_word = ""
                for letter in word:
                    lcletter = letter.lower()
                    if lcletter not in key_approx.keys():
                        new_letter = lcletter
                    else:
                        if random.uniform(0, 1) <= prob:
                            new_letter = random.choice(key_approx[lcletter])
                        else:
                            new_letter = lcletter
                    # go back to original case
                    if not lcletter == letter:
                        new_letter = new_letter.upper()
                    new_word += new_letter
                transformed_texts[i] = new_word
    return transformed_texts


def random_deletion(
    text: List[str],
    prob: float = 0.1,
    try_numbers: int = 1,
    stop_words: Optional[List[str]] = [],
    seed: int = None,
) -> List[str]:
    """
    Randomly deletes words from the sentence with probability p

    Parameters
    ----------
    text: List[str]
        list of tokens in the sentence
    prob: float
        probability of the deletion
    try_numbers: int
        how much the transformation is applied (default is 1)
    seed: int
        seed to freeze everything
    stop_words: List[int], optional
        stop_words to ignore during deletion (default is None)

    Returns
    -------
    List[str]
        transformed sentence in tokens
    """
    if seed is not None:
        random.seed(seed)
    # if there's only one word, don't delete it
    if len(text) <= 1:
        return text

    # randomly delete words with probability p
    words_copy = deepcopy(text)
    for _ in range(try_numbers):
        new_words = []
        for idx, word in enumerate(words_copy):
            if idx in stop_words:
                new_words.append(word)
                continue
            r = random.uniform(0, 1)
            if r > prob:
                new_words.append(word)
        words_copy = deepcopy(new_words)

    # if you end up deleting all words, just return a random word
    if len(new_words) == 0:
        rand_int = random.randint(0, len(text) - 1)
        return [text[rand_int]]

    if new_words == text:
        stopwords = [
            i
            for (i, word) in enumerate(text)
            if (word in STOPWORDS and i not in stop_words)
        ]
        if len(stopwords) > 0:
            random_idx = random.choice(stopwords)
            new_words.pop(random_idx)

    return new_words


def random_swap(
    words: List[str],
    try_numbers: int = 1,
    stop_words: Optional[List[str]] = [],
    seed: int = None,
) -> List[str]:
    """
    Randomly swap two words in the sentence

    Parameters
    ----------
    words: List[str]
        list of tokens in the sentence
    try_numbers: int
        how much the transformation is applied (default is 1)
    seed: int
        seed to freeze everything
    stop_words: List[int], optional
        stop_words to ignore during swaps (default is None)

    Returns
    -------
    List[str]
        transformed sentence in tokens
    """
    if seed is not None:
        random.seed(seed)
    new_words = words.copy()
    allowed_words = [word for word in words if word not in stop_words]
    if len(allowed_words) == 1:
        return new_words

    for _ in range(try_numbers):
        word_1, word_2 = random.choice(allowed_words), random.choice(allowed_words)
        word_idx_1, word_idx_2 = words.index(word_1), words.index(word_2)

        new_words[word_idx_1], new_words[word_idx_2] = (
            new_words[word_idx_2],
            new_words[word_idx_1],
        )

    return new_words


def change_char_case(
    text: List[str],
    prob: float = 0.1,
    prob_token_pass: float = 0.1,
    try_numbers: int = 1,
    seed: int = 42,
    stop_words: List[str] = [],
) -> List[str]:
    """
    Changes character cases randomly

    Parameters
    ----------
    text: str
        text to transform
    prob: float
        probability of the transformation (default is 0.1)
    prob_token_pass: float
        probability of the transformation of the particular token (default is 0.1)
    try_numbers: int
        how much the transformation is applied (default is 1)
    seed: int
        seed to freeze everything (default is 42)
    stop_words: List[str], optional
        stop words to ignore during transformation (default is None)

    Returns
    -------
    List[str]
        list of transformed sentences
    """
    if seed is not None:
        random.seed(seed)
    transformed_texts = deepcopy(text)
    for _ in range(try_numbers):
        for i, word in enumerate(transformed_texts):
            if random.uniform(0, 1) <= prob_token_pass:
                transformed_texts[i] = word
            if word in stop_words:
                new_word = word
            else:
                new_word = ""
                for c in word:
                    if random.uniform(0, 1) < prob:
                        if c.isupper():
                            new_word += c.lower()
                        elif c.islower():
                            new_word += c.upper()
                    else:
                        new_word += c
            transformed_texts[i] = new_word
    return transformed_texts
