"""
This module contains a set of functions for mapping process and product names
based on string similarity measures.
"""

import os

import jellyfish
import numpy
import scipy.optimize


_stop_words = None


def stopwords() -> set:
    """ Returns a list of stopwords. """
    global _stop_words
    if _stop_words is not None:
        return _stop_words
    folder = os.path.dirname(__file__)
    _stop_words = set()
    with open(folder + os.sep + 'data' + os.sep + 'stopwords.txt',
              'r', encoding='utf-8') as f:
        for line in f:
            _stop_words.add(line.strip())
    return _stop_words


def is_stopword(word: str) -> bool:
    """ Returns `True` when the given word is a stopword. """
    if word is None:
        return False
    return word.strip().lower() in stopwords()


def keywords(phrase: str, strip_lci_terms=False) -> list:
    """ Returns the keywords from the given phrase (without duplicates). A
        keyword is a word that is not a stopword. """
    if not isinstance(phrase, str):
        return []
    feed = phrase.lower()
    if strip_lci_terms:
        lci_terms = ["production mix", "at plant"]
        for lci_term in lci_terms:
            feed = feed.replace(lci_term, "")

    p = set()
    buffer = ""
    for char in feed:
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
    """ Searches for the best matching string for the given term `s` in the
        given list based on the similarity of the keywords in the respecitive
        strings """
    if len(phrases) == 0:
        return ""

    terms = keywords(s)
    if len(terms) == 0:
        return ""

    candidate = None
    score = 0.0
    for phrase in phrases:
        comps = keywords(phrase)
        if len(comps) == 0:
            continue
        c_score = words_similarity(terms, comps)
        if candidate is None or c_score > score:
            candidate = phrase
            score = c_score

    return candidate


def words_similarity(words_a: list, words_b: list) -> float:
    """ Calculate the similarity of the given word lists a and b. """
    if len(words_a) == 0 or len(words_b) == 0:
        return 0.0
    # create a matrix with the string similarities and calculate
    # the best score using the "Hungarian method"
    # (see https://en.wikipedia.org/wiki/Hungarian_algorithm).
    # we use negative values for the similarities in the matrix
    # because the implementation in SciPy searches for the minimum
    # https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
    rows = len(words_a)
    cols = len(words_b)
    mat = numpy.zeros((rows, cols))
    for row in range(0, rows):
        for col in range(0, cols):
            mat[row, col] = -similarity(words_a[row], words_b[col])
    row_ind, col_ind = scipy.optimize.linear_sum_assignment(mat)

    # dividing the score by the number of keywords considers unmatched
    # keywords; however, this is not perfect when the number of keywords
    # is small
    n = max(rows, cols)
    return abs(mat[row_ind, col_ind].sum()) / n


def similarity(a: str, b: str) -> float:
    """ Calculates a value between 0 and 1 that describes the similarity of
        the given strings `a` and `b` where 0 means completely different and `1`
        means equal. """
    if not isinstance(a, str) or not isinstance(b, str):
        return 0.0
    dist = jellyfish.levenshtein_distance(a, b)
    max_len = max(len(a), len(b))
    if dist >= max_len:
        return 0.0
    sim = 1 - (dist / max_len)
    return sim
