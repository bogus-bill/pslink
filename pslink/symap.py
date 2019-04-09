import math
import os

import jellyfish
import numpy
import scipy.optimize


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


def keywords(phrase: str) -> list:
    if not isinstance(phrase, str):
        return []
    p = set()
    buffer = ""
    for char in phrase:
        if char.isalnum() or char == "-":
            buffer = buffer + char
            continue
        if buffer == "":
            continue
        if not is_stopword(buffer):
            p.add(buffer.lower())
        buffer = ""
    if buffer != "" and not is_stopword(buffer):
        p.add(buffer.lower())
    return list(p)


def best_match(s: str, phrases: list) -> str:
    if len(phrases) == 0:
        return None

    terms = keywords(s)
    if len(terms) == 0:
        return None

    candidate = None
    score = 0.0
    for phrase in phrases:
        comps = keywords(phrase)
        if len(comps) == 0:
            continue
        rows = len(comps)
        cols = len(terms)
        mat = numpy.zeros((rows, cols))
        for row in range(0, rows):
            for col in range(0, cols):
                mat[row, col] = -similarity(comps[row], terms[col])
        row_ind, col_ind = scipy.optimize.linear_sum_assignment(mat)
        c_score = abs(mat[row_ind, col_ind].sum())

        if rows != cols:
            f = 1 - 0.25 * (min(rows, cols) / max(rows, cols))
            c_score = c_score * f

        if candidate is None or c_score > score:
            candidate = phrase
            score = c_score

    return candidate


def similarity(a: str, b: str) -> float:
    return jellyfish.jaro_winkler(a, b)
