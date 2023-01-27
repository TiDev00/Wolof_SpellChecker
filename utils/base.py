"""
base
-----
The base class for all the spelling correction and word suggestion algorithms
Contents:
    Base class,
    add_words
"""

from typing import List
from utils.dictionary import Dictionary
from utils.helper import pre_process

WOLOF_LETTERS = 'aàãbcdeéëfgijklmnñŋoópqrstuwxy'
WOLOF_VOWELS = 'aàãioóueéë'


class Base(object):

    def __init__(self) -> None:

        self.alphabet = WOLOF_LETTERS
        self.vowels = WOLOF_VOWELS
        self.dictionary = Dictionary()

        vocab_file = open('utils/lexicon.txt', "r").read().split()

        for word in vocab_file:
            self.add_words([pre_process(word).strip()])

    def add_words(self, words: List[str]) -> None:
        """
            Function that add words (index) to the dictionary used by the algorithm
            Parameters
            ----------
                words : List[str]
                    The list of words to be indexed
        """

        processed_actual_words = [(pre_process(word), word) for word in words]

        self.dictionary.add_words(processed_actual_words)
