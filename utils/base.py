"""
base
-----
The base class for all the spelling correction and word suggestion algorithms
Contents:
    Base class,
    insert_word
"""

from typing import List
from utils.dictionary import Dictionary
from utils.helper import pre_process

WOLOF_LETTERS = 'aàãbcdeéëfgijklmnñŋoópqrstuwxy'
WOLOF_VOWELS = 'aàãioóueéë'
lex_filepath = 'utils/wolof_lexicon.txt'


class Base(object):

    def __init__(self) -> None:

        self.alphabet = WOLOF_LETTERS
        self.vowels = WOLOF_VOWELS
        self.dictionary = Dictionary()

        vocab_file = open(lex_filepath, 'r').read().split()

        for word in vocab_file:
            self.insert_word([pre_process(word).strip()])

    def insert_word(self, words: List[str]) -> None:
        """
            Function that add words (index) to the dictionary used by the algorithm
            Parameters
            ----------
                words : List[str]
                    The list of words to be indexed
        """

        processed_actual_words = [(pre_process(word), word) for word in words]

        self.dictionary.insert_word(processed_actual_words)
