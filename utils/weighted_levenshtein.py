"""
levenshtein
-----
The corrector class for suggesting words based on  weighted levenshtein edit distance
Contents:
    Corrector class
"""

from utils.helper import List, pre_process, replace_cost, rank_filter
from utils.dictionary import Dictionary
from utils.base import Base
from utils.wolof_rules import compound_sound_transformation


class Corrector(Base):

    def __init__(self) -> None:
        super(Corrector, self).__init__()

    def get_suggestions(self, word: str, max_distance: int = 5) -> List[tuple]:
        """
            Get suggestions based on the edit-distance using the under dynamic programming approach
            Parameters
            ----------
                word: str
                    The given source word for suggesting indexed words
                max_distance: int
                    The maximum distance between the words indexed and the source word
            Returns
            ----------
                suggestions: List[tuple]
                    The word suggestions with their corresponding distances
        """

        processed_word = compound_sound_transformation(pre_process(word))

        def search(dictionary_node: Dictionary, previous_row: list):
            """
                Search for the candidates in the given dictionary node's children
            Parameters
            ----------
                dictionary_node: Dictionary
                    The node in the Trie dictionary
                previous_row: list
                    The previous row in the dynamic-programming approach
            """

            for current_source_letter in dictionary_node.children:
                current_row = [previous_row[0] + 1]

                for i in range(1, len(processed_word) + 1):
                    value = min(previous_row[i] + 1, current_row[i - 1] + 1, previous_row[i - 1] +
                                replace_cost(current_source_letter, processed_word[i - 1]))
                    current_row.append(value)

                if (current_row[-1] <= max_distance and
                        dictionary_node.children[current_source_letter].words_at_node is not None):

                    for words in dictionary_node.children[current_source_letter].words_at_node:
                        # noinspection PyTypeChecker
                        suggestions.append((words, current_row[-1]))

                if min(current_row) <= max_distance:
                    search(dictionary_node.children[current_source_letter], current_row)

        suggestions = []

        first_row = range(0, len(processed_word) + 1)

        # noinspection PyTypeChecker
        search(self.dictionary, first_row)

        return rank_filter(suggestions)
