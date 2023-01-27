"""
dictionary
-----
A dictionary class to allow indexing words from lexicon file
Contents:
    constructor,
    add_words
"""

from typing import List, Tuple


class Dictionary(object):

    def __init__(self) -> None:
        self.words_at_node = None
        self.children = {}

    def add_words(self, words: List[Tuple[str, str]]) -> None:
        """
            Add words to index to the Trie dictionary
        Parameters
        ----------
            words: List[Tuple[str, str]]
                The list of words to index to the dictionary
        """

        for word in words:
            processed_word, actual_word = word
            trie_node = self
            for letter in processed_word:
                if letter not in trie_node.children:
                    trie_node.children.update({letter: Dictionary()})
                trie_node = trie_node.children[letter]

            if trie_node.words_at_node is None:
                trie_node.words_at_node = list()
            trie_node.words_at_node.append(actual_word)
