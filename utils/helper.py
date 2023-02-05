"""
helper
-----
Helper functions that are used by algorithms
Also contains 2 implementations to compute edit distance between 2 strings
Contents:
    fr_en_word,
    pre_process,
    replace_cost,
    sort_list,
    recursive_levenshtein,
    dynamic_levenshtein
"""

from typing import List
import enchant


fr_lex = enchant.Dict('fr')
en_lex = enchant.Dict('en')

COST_MATRIX = {('a', 'à'): 1, ('o', 'ó'): 1,
               ('a', 'ã'): 1, ('e', 'é'): 1,
               ('e', 'ë'): 1, ('é', 'ë'): 1,
               ('x', 'q'): 1}


def fr_en_word(word: str) -> bool:
    """
        Check if a word is either an English or French word and returns True or False
        Parameters
        ----------
            word: str
                word which will be checked
        Returns
        ----------
            checking_answer: bool
                True if a word is in French or English dictionary
    """
    if fr_lex.check(word) or en_lex.check(word):
        return True
    return False


def pre_process(word: str) -> str:
    """
        Convert to lower every word that will be indexed
        Parameters
        ----------
            word: str
                word that will converted
        Returns
        ----------
            processed_word: str
                Word in lowercase
    """

    return word.lower()


def replace_cost(source: str, target: str) -> float:
    """
        Cost to replace the letter in source with the letter in target
        Parameters
        ----------
            source: str
                First letter
            target: str
                Second letter
        Returns
        ----------
            cost: float
                The cost to replace the letters
    """

    if source == target:
        return 0

    if (source, target) in COST_MATRIX or (target, source) in COST_MATRIX:
        return COST_MATRIX.get((source, target)) or COST_MATRIX.get((target, source))

    return 2


def rank_filter(data: List[tuple], descending: bool = False) -> List[tuple]:
    """
        Sort the list of tuples according to the edit distance
        Parameters
        ----------
            data: List[tuple]
                The list of tuple which needs to be sorted
            descending: bool
                Indicate whether the sorting should be in ascending or descending order
        Returns
        ----------
            sorted_list: List[tuple]
                The sorted list of tuples according to the `sort_key` and `descending` variables
    """

    return sorted(data, key=lambda a: a[1], reverse=descending)


def recursive_levenshtein(source: str, target: str, m: int, n: int) -> int:
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
        return recursive_levenshtein(source, target, m - 1, n - 1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all operations and take minimum of three values.
    return 1 + min(recursive_levenshtein(source, target, m, n - 1), recursive_levenshtein(source, target, m - 1, n),
                   (recursive_levenshtein(source, target, m - 1, n - 1) + 1))


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
                                                            computations_array[(i - 1) % 2][j - 1]+1)))

    return computations_array[length_trg % 2][length_src]
