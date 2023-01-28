"""
levenshtein
-----
The corrector class for suggesting words based on  weighted levenshtein edit distance and
2 other functions that can be used to compute edit distance between 2 words.
Contents:
    Corrector class,
    naive_levenshtein,
    dynamic_levenshtein,
"""

from utils.helper import *
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

        return sort_list(suggestions)


def naive_levenshtein(source: str, target: str, m: int, n: int) -> int:
    """
        Naive recursive function to find minimum edit distance between 2 string.
        Time complexity O(3^m)
        Auxiliary space O(1)
        Parameters
        ----------
            source: str
                Source word to calculate minimum edit distance
            target: str
                Target word to calculate minimum edit distance
            m: int
                Length of source word
            n: int
                Length of target word
        Returns
        ----------
            minimum_edit_distance: int
                Distance required to convert a source string to target string
    """

    # If first string is empty, insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, ignore last characters and get count for remaining strings.
    if source[m - 1] == target[n - 1]:
        return naive_levenshtein(source, target, m - 1, n - 1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all operations and take minimum of three values.
    return 1 + min(naive_levenshtein(source, target, m, n - 1), naive_levenshtein(source, target, m - 1, n),
                   naive_levenshtein(source, target, m - 1, n - 1))


def dynamic_levenshtein(source: str, target: str) -> int:
    """
        Space efficient Dynamic Programming function to find minimum edit distance between 2 string
        Time complexity O(mxn)
        Auxiliary space O(m)
        Parameters
        ----------
            source: str
                Source word to calculate minimum edit distance
            target: str
                Target word to calculate minimum edit distance
        Returns
        ----------
            minimum_edit_distance: int
                Distance required to convert a source string to target string
    """

    length_src = len(source)
    length_trg = len(target)

    # Create an array to memorize result of previous computations
    computations_array = [[0 for i in range(length_src + 1)] for j in range(2)]

    # Base condition when second String is empty then we remove all characters
    for i in range(0, length_src + 1):
        computations_array[0][i] = i

    # This loop run for every character in second String
    for i in range(1, length_trg + 1):
        # This loop compares the char from second String with first String characters
        for j in range(0, length_src + 1):
            # If first String is empty then we have to perform add character operation to get second String
            if j == 0:
                computations_array[i % 2][j] = i
            # If character from both String is same then we do not perform any operation
            # here i % 2 is for bound the row number
            elif source[j - 1] == target[i - 1]:
                computations_array[i % 2][j] = computations_array[(i - 1) % 2][j - 1]
            # If character from both String is not same then we take the minimum from three specified operation
            else:
                computations_array[i % 2][j] = (1 + min(computations_array[(i - 1) % 2][j],
                                                        min(computations_array[i % 2][j - 1],
                                                            computations_array[(i - 1) % 2][j - 1])))

    return computations_array[length_trg % 2][length_src]
