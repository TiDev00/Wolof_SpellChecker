"""
naive_spellchecking
-----
A naive implementation of spellchecker generating every combination of letters for a given word and
relying on frequency of words in given a text to sort suggestions.
Contents:
    get_count,
    get_probs,
    split_word,
    delete_letter,
    switch_letter,
    replace_letter,
    insert_letter,
    edit_one_letter,
    edit_two_letters,
    get_suggestions
"""

from collections import Counter
from utils.wolof_rules import compound_sound_transformation

WOLOF_LETTERS = 'aàãbcdeéëfgijklmnñŋoópqrstuwxy'


def get_count(word_list: list) -> dict:
    """
        Creates a dictionary with all words in corpus and their frequencies
        Parameters
        ----------
            word_list: list
                all words extracted from given a file
        Returns
        ----------
            word_count_dict: dict
                dictionary with corpus words as keys and their count as value
    """

    return Counter(word_list)


def get_probs(word_count_dict: dict) -> dict:
    """
        Creates a dictionary with all probabilities each word will occur
        Parameters
        ----------
            word_count_dict: dict
                the word count where key is the word and value is its frequency.
        Returns
        ----------
            probs: dict
                a dictionary where keys are the words and the values are the probability that a word will occur.
    """

    total_item = float(sum(word_count_dict.values()))

    probs = {}

    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / total_item

    return probs


def split_word(word: str) -> list:
    """
        Creates a list of tuple with all splitting combination for a given word
        Parameters
        ----------
            word: str
                word for which we generate all splits possible
        Returns
        ----------
            split_list: list
                all possible strings obtained by splitting a given word
        """

    word = word.lower()

    return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def delete_letter(word: str, verbose: bool = False) -> list:
    """
        Generates all words that result from deleting one character
        Parameters
        ----------
            word: str
                word for which we generate all possible words in the vocabulary which have 1 missing character
            verbose: bool
                set to true if we want to see all the process
        Returns
        ----------
            delete_list: list
                all possible strings obtained by deleting 1 character from word
    """

    split_list = split_word(word)
    delete_list = [L + R[1:] for L, R in split_list if R]

    if verbose:
        print(f"misspelled word = {word}\nsplit_list = {split_list}\ndelete_list = {delete_list}\n")

    return delete_list


def switch_letter(word: str, verbose: bool = False) -> list:
    """
        Switches 2 letters adjacent in a word
        Parameters
        ----------
            word: str
                input string
            verbose: bool
                set to true if we want to see all the process
        Returns
        ----------
            switch_list: list
                all possible strings with one adjacent character switched
    """

    split_list = split_word(word)
    switch_list = [a + b[1] + b[0] + b[2:] for a, b in split_list if len(b) >= 2]

    if verbose:
        print(f"switch_list = {switch_list}\n")

    return switch_list


def replace_letter(word: str, verbose: bool = False) -> list:
    """
        Creates a list of strings with 1 replaced letter from orignal word
        Parameters
        ----------
            word: str
                input string
            verbose: bool
                set to true if we want to see all the process
        Returns
        ----------
            replace_list: list
                all possible strings where we replaced one letter from original word
    """

    split_list = split_word(word)

    replace_list = [a + letter + (b[1:] if len(b) > 1 else '') for a, b in split_list if b for letter in WOLOF_LETTERS]
    replace_set = set(replace_list)
    replace_set.remove(word)

    # turn the set back into a list and sort it
    replace_list = sorted(list(replace_set))

    if verbose:
        print(f"replace_list = {replace_list}\n")

    return replace_list


def insert_letter(word: str, verbose: bool = False) -> list:
    """
        Creates a list of strings with 1 letter inserted at every offset
        Parameters
        ----------
            word: str
                input string
            verbose: bool
                set to true if we want to see all the process
        Returns
        ----------
            insert_list: list
                all possible strings with one new letter inserted at every offset
    """

    split_list = []

    for c in range(len(word) + 1):
        split_list.append((word[0:c], word[c:]))
    insert_list = [a + letter + b for a, b in split_list for letter in WOLOF_LETTERS]

    if verbose:
        print(f"insert_list = {insert_list}\n")

    return insert_list


def edit_one_letter(word: str, verbose: bool = False, allow_switch: bool = False) -> set:
    """
        Gets a set of all possible edits that are one edit away from a word
        Parameters
        ----------
            word: str
                input for which we generate all possible words one edit away
            verbose: bool
                set to true if we want to see all the process
            allow_switch: bool
                allows switch operation to be taken into account
        Returns
        ----------
            one_edit_list: set
                words obtained with one edit from a given word
    """

    one_edit_set = set()
    word = word.lower()

    one_edit_set.update(delete_letter(word, verbose=verbose))
    if allow_switch:
        one_edit_set.update(switch_letter(word, verbose=verbose))
    one_edit_set.update(replace_letter(word, verbose=verbose))
    one_edit_set.update(insert_letter(word, verbose=verbose))

    if verbose:
        print(f"edit_letters = {one_edit_set}\n")

    return one_edit_set


def edit_two_letters(word: str, verbose: bool = False, allow_switch: bool = False) -> set:
    """
        Gets a set of all possible edits that are n = 2  edit away from a word
        Parameters
        ----------
            word: str
                input for which we generate all possible words n edit away
            verbose: bool
                set to true if we want to see all the process
            allow_switch: bool
                allows switch operation to be taken into account
        Returns
        ----------
            n_edit_list: set
                words obtained with 2 edit from a given word
    """

    two_edit_set = edit_one_letter(word, verbose=False, allow_switch=allow_switch)

    for word in two_edit_set.copy():
        if word:
            two_edit_set.update(edit_one_letter(word, verbose=False, allow_switch=allow_switch))

    if verbose:
        print(f"edit_letters = {two_edit_set}\n")

    return two_edit_set


def get_suggestions(word: str, probs: dict, vocab: list[str],
                    verbose: bool = False, allow_switch: bool = False) -> list:
    """
        Computes and returns a list of n possible suggestions tuple and their probabilities
        Parameters
        ----------
            word: str
                input to check for suggestion
            probs: dict
                Maps each word to its probability in the corpus
            vocab: list[str]
                Vocabulary from which we will compare misspelled words
            verbose: bool
                set to true if we want to see all the process
            allow_switch: bool
                allows switch operation to be taken into account
        Returns
        ----------
            n_best: list
                Tuples with most probable n corrected words and their probabilities
    """

    word = compound_sound_transformation(word)

    # Creates suggestions
    suggestions = set(
        (word in vocab and word) or
        edit_one_letter(word, verbose=verbose, allow_switch=allow_switch).intersection(vocab) or
        edit_two_letters(word, verbose=verbose, allow_switch=allow_switch).intersection(vocab)
    )

    # Get the best words and return the top n_suggested words as n_best
    n_best = [(str(s), float(probs[s])) for s in list(suggestions) if s in probs]
    n_best.sort(key=lambda item: item[1], reverse=True)

    # return same word if set is empty
    if not n_best:
        n_best = [(word, 0)]

    if verbose:
        print("suggestions = ", n_best)

    return n_best
