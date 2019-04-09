import os

import jellyfish


_stop_words = None


def stopwords() -> list:
    global _stop_words
    if _stop_words is not None:
        return _words
    folder = os.path.dirname(__file__)
    _words = set()
    with open(folder + os.sep + 'data' + os.sep + 'stopwords.txt',
              'r', encoding='utf-8') as f:
        for line in f:
            _words.add(line.strip())
    return _words


def is_stopword(word: str) -> bool:
    if word is None:
        return False
    return word.strip().lower() in stopwords()


def similarity(a: str, b: str) -> float:
    return jellyfish.levenshtein_distance(a, b)
