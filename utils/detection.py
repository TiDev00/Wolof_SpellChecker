"""
detection
-----
The detector class for checking valid wolof words
Contents:
    Detector class
"""

from utils.base import Base
from utils.wolof_rules import fr_en_word, rules_validator


class Detector(Base):

    def __init__(self) -> None:
        super(Detector, self).__init__()

    def is_word(self, word: str) -> bool:
        """
            Helper method to check if a given word is in the wolof lexicon
            Parameters
            ----------
                word: str
                    Word that will be checked
            Returns
            -------
                is_wolof_word: bool
                    True if the given word is in the wolof lexicon
        """
        word_length = len(word)
        trie_node = self.dictionary
        for i, letter in enumerate(word.lower()):
            if letter in trie_node.children:
                trie_node = trie_node.children[letter]
                if i == word_length - 1:
                    if trie_node.words_at_node is not None:
                        return True
                    else:
                        return False
            else:
                return False

    def checker(self, word: str) -> bool:
        """
            Helper method that check if a given word is not french, respects wolof writing rules
            and is in the wolof lexicon
            Parameters
            ----------
                word: str
                    Word that will be checked
            Returns
            -------
                is_valid_word: bool
                    True if the given word is a valid word
        """
        if rules_validator(word) and self.is_word(word):
            return True
        return False
