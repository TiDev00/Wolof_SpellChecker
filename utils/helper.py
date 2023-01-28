"""
helper
-----
Helper functions that are used by algorithms
Contents:
    pre_process,
    replace_cost,
    sort_list
"""

from typing import List


COST_MATRIX = {('a', 'à'): 1, ('o', 'ó'): 1,
               ('a', 'ã'): 1, ('e', 'é'): 1,
               ('e', 'ë'): 1, ('é', 'ë'): 1,
               ('x', 'q'): 1}


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


def sort_list(data: List[tuple], descending: bool = False) -> List[tuple]:
    """
        Sort the list of dictionaries according to the `sort_key` field
        Parameters
        ----------
            data: List[tuple]
                The list of tuple which needs to be sorted
            descending: bool
                Indicate whether the sorting should be in ascending or descending order
        Returns
        ----------
            sorted_list: List[tuple]
                The sorted list of tuples, according to the `sort_key` and `descending` variables
    """

    return sorted(data, key=lambda a: a[1], reverse=descending)
