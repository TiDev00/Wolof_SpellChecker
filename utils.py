"""
utils
-----
Implementations for functions used by the main file.
Contents:
    word_extraction,
    get_count,
    get_probs,
    split_word,
    delete_letter,
    switch_letter,
    replace_letter,
    insert_letter,
    edit_one_letter,
    edit_n_letters,
    get_suggestions
"""

import re
from collections import Counter

wolof_letters = 'aàãbcdeéëfgijklmnñŋoópqrstuwxy'


def word_extraction(filename: str) -> list:
    """
        Processes file and return a list of all words in lowercase.
        Parameters
        ----------
            filename: str
                File from which words will be extracted
        Returns
        ----------
            words_list: list
                all words extracted from given file and sorted
    """

    with open(filename) as f:
        data = f.read()

    words = re.findall('\w+', data.lower())

    return sorted(words)


def wolof_transformation(word: str) -> str:
    """
        Modifies writing of a word according to wolof writing rules.
        Deletes compound sounds like ou, oi, ch, an, en, eu, au, eau, ien, ienne, ai, gn, elle, ette, tion, oin
        ui, ill, ille, eil, eille, ouille, ail, aille, ueil, ier, ei, oeu, kh, gn, di, tch, gni, ouss
        Parameters
        ----------
            word: str
                word which will be changed
        Returns
        ----------
            words: list
                new word written in wolof by taking into account wolof rules
    """
    fr_wol_maps = [('ouss', 'us'), ('ouille', 'uy'), ('ou', 'u'), ('gn', 'ñ'), ('di', 'j'), ('kh', 'x'), ('tch', 'c'),
                   ('oeu', 'ë'), ('eu', 'ë'), ('aille', 'ay'), ('eille', 'ey'), ('eau', 'óo'), ('au', 'ó'),
                   ('ienne', 'iyen'), ('v', 'w'), ('z', 's'), ('h', '')]
    word = word
    for phonetics in fr_wol_maps:
        word = re.sub(phonetics[0], phonetics[1], word.lower())
    print(word)
    return word


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

    replace_list = [a + letter + (b[1:] if len(b) > 1 else '') for a, b in split_list if b for letter in wolof_letters]
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
    insert_list = [a + letter + b for a, b in split_list for letter in wolof_letters]

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

    one_edit_set.update(delete_letter(word, verbose=verbose))
    if allow_switch:
        one_edit_set.update(switch_letter(word, verbose=verbose))
    one_edit_set.update(replace_letter(word, verbose=verbose))
    one_edit_set.update(insert_letter(word, verbose=verbose))

    if verbose:
        print(f"edit_letters = {one_edit_set}\n")

    return set(one_edit_set)


def edit_n_letters(word: str, nbr_edit: int = 2, verbose: bool = False, allow_switch: bool = False) -> set:
    """
        Gets a set of all possible edits that are n edit away from a word
        Parameters
        ----------
            word: str
                input for which we generate all possible words n edit away
            nbr_edit: int
                number of edit n
            verbose: bool
                set to true if we want to see all the process
            allow_switch: bool
                allows switch operation to be taken into account
        Returns
        ----------
            n_edit_list: set
                words obtained with n edit from a given word
    """

    n_edit_set = edit_one_letter(word, verbose=False, allow_switch=allow_switch)

    for j in range(nbr_edit - 1):
        for word in n_edit_set.copy():
            if word:
                n_edit_set.update(edit_one_letter(word, verbose=False, allow_switch=allow_switch))

    if verbose:
        print(f"edit_letters = {n_edit_set}\n")

    return set(n_edit_set)


def get_suggestions(word: str, probs: dict, vocab: set, nbr_edit: int = 2,
                    verbose: bool = False, allow_switch: bool = False) -> list:
    """
        Computes and returns a list of n possible suggestion tuple and their probabilities
        Parameters
        ----------
            word: str
                input to check for suggestion
            probs: dict
                Maps each word to its probability in the corpus
            vocab: set
                Vocabulary from which we will compare misspelled words
            nbr_edit: int
                number of edit n
            verbose: bool
                set to true if we want to see all the process
            allow_switch: bool
                allows switch operation to be taken into account
        Returns
        ----------
            n_best: list
                Tuples with most probable n corrected words and their probabilities
    """

    # Creates suggestions
    suggestions = set(
        (word in vocab and word) or
        edit_one_letter(word, verbose=verbose, allow_switch=allow_switch).intersection(vocab) or
        edit_n_letters(word, nbr_edit=nbr_edit, verbose=verbose, allow_switch=allow_switch).intersection(vocab)
    )

    # Get the best words and return the top n_suggested words as n_best
    n_best = [(str(s), float(probs[s])) for s in list(suggestions) if s in probs]
    n_best.sort(key=lambda item: item[1], reverse=True)

    if verbose:
        print("suggestions = ", n_best)

    return n_best

