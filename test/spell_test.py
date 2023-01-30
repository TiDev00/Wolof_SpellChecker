"""
spell_test
-----
This is a test file to evaluate the implemented models in utils
Contents:
    pairing,
    lexical_recall,
    error_recall,
    precision,
    suggestion_adequacy
"""

import time
from utils.detection import Detector
from utils.weighted_levenshtein import Corrector
from utils.naive_levenshtein import get_probs, get_count, get_suggestions
from utils.helper import dynamic_levenshtein

vocab = []
for w in open('utils/wolof_lexicon.txt', 'r').read().split():
    vocab.append(w)


def pairing(lines) -> list[tuple]:
    """
        Parse 'right: wrong1 wrong2' test_set into [('right', 'wrong1'), ('right', 'wrong2')]
        Parameters
        ----------
            lines: TextIO
                Stream with each line from test file
        Returns
        ----------
            pairs: list[tuple]
                list of tuple with a wrong word and the associated correct word
    """
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]


def lexical_recall_wl(test_set, verbose: bool = False) -> int:
    """
        For the weighted levenshtein model with Trie Structure
        # words flagged valid / # valid words
        Parameters
        ----------
            test_set: TextIO
                File used to test systems
            verbose: bool
                Display or not correction for each word
        Returns
        ----------
            # word flagged valid by system that are real valid words
    """

    data = pairing(test_set)

    real_valid = set()

    for w1, _ in data:
        real_valid.add(w1)

    flagged_valid = set()

    detector = Detector()

    start = time.time()

    for word in real_valid:
        if detector.checker(word):
            flagged_valid.add(word)
        else:
            if verbose:
                print('detector({}) => Not a valid word; expected Is a valid word'.format(word))

    dt = time.time() - start

    n = len(real_valid)
    print('Weighted Levenshtein Lexical recall : {:.2%} ({}) of {} valid words successfully detected '
          'in {:.0f} milliseconds'.format(len(flagged_valid) / n, len(flagged_valid), n, n / dt))

    return len(flagged_valid.intersection(real_valid))


def error_recall_wl(test_set, verbose: bool = False) -> int:
    """
        For the weighted levenshtein model with Trie Structure
        # words flagged invalid / # invalid words
        Parameters
        ----------
            test_set: TextIO
                File used to test systems
            verbose: bool
                Display or not correction for each word
        Returns
        ----------
            # word flagged invalid by system that are real invalid words
    """

    data = pairing(test_set)

    real_invalid = set()

    for _, w2 in data:
        real_invalid.add(w2)

    flagged_invalid = set()

    detector = Detector()

    start = time.time()

    for word in real_invalid:
        if not detector.checker(word):
            flagged_invalid.add(word)
        else:
            if verbose:
                print('detector({}) => Is a valid word; expected Not a valid word'.format(word))

    dt = time.time() - start

    n = len(real_invalid)
    print('Weighted Levenshtein error recall : {:.2%} ({}) of {} invalid words successfully detected '
          'in {:.0f} milliseconds'.format(len(flagged_invalid) / n, len(flagged_invalid), n, n / dt))

    return len(flagged_invalid.intersection(real_invalid))


def precision_wl(test_set, lex_rec: int, err_rec: int):
    """
        For the weighted levenshtein model with Trie Structure
        # words flagged invalid / # invalid words
        Parameters
        ----------
            test_set: TextIO
                File used to test systems
            lex_rec: int
                # word flagged valid by system that are real valid words
            err_rec: int
                # word flagged invalid by system that are real invalid words
        Returns
        ----------
            Print a report
    """

    data = pairing(test_set)

    real_valid = set()
    real_invalid = set()

    for w1, w2 in data:
        real_valid.add(w1)
        real_invalid.add(w2)

    n = len(real_valid) + len(real_invalid)
    le = lex_rec + err_rec

    print('Weighted Levenshtein Precision : {:.2%} ({}) of {} words correctly flagged valid or invalid'
          .format(le / n, le, n))


def suggestion_adequacy_wl(test_set, verbose: bool = False):
    """
        For the weighted levenshtein model with Trie Structure
        # correct suggestions for invalid words / # invalid words
        Also print the speed to do all the suggestions
        Parameters
        ----------
            test_set: TextIO
                File used to test systems
            verbose: bool
                Display or not correction for each word
        Returns
        ----------
            Prints reports
    """

    suggester = Corrector()

    dataset = pairing(test_set)

    good, unknown = 0, 0
    unknown_words = set()

    n = len(dataset)

    start = time.time()

    for right, wrong in dataset:
        suggestion = suggester.get_suggestions(wrong)[0][0]
        good += (suggestion == right)
        if suggestion != right:
            if right not in vocab:
                unknown_words.add(right)
                unknown += 1
            if verbose:
                print('autocorrection({}) => {}; expected {}'.format(wrong, suggestion, right))

    dt = time.time() - start

    print('Weighted Levenshtein Suggestion Adequacy: {:.2%} ({}) of {} invalid words successfully corrected '
          '({:.2%} unknown valid words) in {:.0f} second'.format(good / n, good, n, unknown / n, n / dt))
    if unknown_words:
        print('List of valid words not in the lexicon: ', unknown_words)


def mean_reciprocal_rank_wl(test_set):
    """
        For the weighted levenshtein model with Trie Structure
        Mean reciprocal rank (MRR) for a list of correct answers and suggestions.
        Parameters
        ----------
            test_set: TextIO
        Returns
        ----------
            Prints reports
    """

    data = pairing(test_set)

    suggester = Corrector()

    correct_suggestions = []

    for right, wrong in data:
        # add every tuple (correct word, system suggestions) to correct_suggestions list w/o costs
        correct_suggestions.append((right, list(map(lambda x: x[0], suggester.get_suggestions(wrong)))))

    # Initialize the total reciprocal rank
    total_reciprocal_rank = 0

    # Iterate over the queries
    for query in correct_suggestions:
        # Get the correct word and the list of suggested words
        correct_word = query[0]
        suggested_words = query[1]

        # Initialize the rank to the number of suggested words + 1
        rank = len(suggested_words) + 1

        # Iterate over the suggested words
        for i, word in enumerate(suggested_words, 1):
            # If the correct word is found, update the rank and break the loop
            if word == correct_word:
                rank = i
                break

        # Add the reciprocal rank to the total reciprocal rank
        total_reciprocal_rank += 1 / rank

    # Print the mean reciprocal rank
    print('Weighted Levenshtein MRR : {:.2f}'.format(total_reciprocal_rank / len(correct_suggestions)))


# def suggestion_adequacy_ns(test_set: str, verbose: bool = False):
#     """
#         For the naive levenshtein model
#         Number of correct suggestions for invalid words for all the invalid words
#         Also print the speed to do all the suggestions
#         Parameters
#         ----------
#             test_set: List[str]
#                 File used to test systems
#             verbose: bool
#                 Display or not correction for each word
#         Returns
#         ----------
#             Prints reports
#         """
#
#     dataset = pairing(test_set)
#
#     probs = get_probs(get_count(vocab))
#
#     good, unknown = 0, 0
#     unknown_words = set()
#
#     n = len(dataset)
#
#     start = time.time()
#
#     for right, wrong in dataset:
#         suggestion = (get_suggestions(wrong, probs, vocab))[0][0]
#         good += (suggestion == right)
#         if suggestion != right:
#             if right not in vocab:
#                 unknown_words.add(right)
#                 unknown += 1
#             if verbose:
#                 print('autocorrection({}) => {}; expected {}'.format(wrong, suggestion, right))
#
#     dt = time.time() - start
#
#     print('Naive Levenshtein Suggestion Adequacy: {:.2%} ({}) of {} invalid words successfully corrected '
#           '({:.2%} unknown valid words) in {:.0f} second'.format(good / n, good, n, unknown / n, n / dt))
#     if unknown_words:
#         print('List of valid words not in the lexicon: ', unknown_words)


if __name__ == '__main__':
    lr = lexical_recall_wl(open('misspelled_wolof_words.txt'))
    er = error_recall_wl(open('misspelled_wolof_words.txt'))
    precision_wl(open('misspelled_wolof_words.txt'), lr, er)
    suggestion_adequacy_wl(open('misspelled_wolof_words.txt'))
    mean_reciprocal_rank_wl(open('misspelled_wolof_words.txt'))
