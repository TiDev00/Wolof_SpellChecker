"""
spell_test
-----
This is a test file to evaluate the implemented models in utils
Contents:
    pairing,
    lexical_recall,
    error_recall,
    lexical_precision,
    error_precision,
    lexical_f_score,
    error_f_score,
    predictive_accuracy,
    suggestion_adequacy,
    mean_reciprocal_rank
"""

import time
from utils.detection import Detector
from utils.weighted_levenshtein import Corrector
from collections import Counter
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


def lexical_recall(test_set, verbose: bool = False) -> tuple[int, int, float]:
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
            couple: tuple[int, int, float]
                # real valid words flagged valid by system
                # real valid words flagged invalid by system
                Lexical Recall of system
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
    nv = len(flagged_valid)

    lr = nv / n

    print('Weighted Levenshtein Lexical Recall : {:.2%} ({}) of {} valid words in the text successfully detected '
          'in {:.0f} milliseconds'.format(lr, nv, n, n / dt))

    return nv, (n - nv), lr


def error_recall(test_set, verbose: bool = False) -> tuple[int, int, float]:
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
            couple: tuple[int, int]
                # real invalid words flagged invalid by system
                # real invalid words flagged valid by system
                Error recall of system
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
    ni = len(flagged_invalid)

    er = ni / n

    print('Weighted Levenshtein Error Recall : {:.2%} ({}) of {} invalid words in the text successfully detected '
          'in {:.0f} milliseconds'.format(er, ni, n, n / dt))

    return ni, n - ni, er


def lexical_precision(tp: int, fp: int) -> float:
    """
        For the weighted levenshtein model with Trie Structure
        # real valid words flagged valid / (# real valid words flagged valid + # real invalid words flagged valid)
        Parameters
        ----------
            tp: int
                # real valid words flagged valid by system
            fp: int
                # real invalid words flagged valid by system
        Returns
        ----------
            Pc: float
                Lexical Precision of the system
    """

    size = tp + fp

    lp = tp / size

    print('Weighted Levenshtein Lexical Precision : {:.2%} ({}) of {} words flagged valid '
          'are real valid words'
          .format(lp, tp, size))

    return lp


def error_precision(tn: int, fn: int) -> float:
    """
        For the weighted levenshtein model with Trie Structure
        # real invalid words flagged invalid / (# real invalid words flagged invalid + # real valid words flagged invalid)
        Parameters
        ----------
            tn: int
                # real invalid words flagged invalid by system
            fn: int
                # real valid words flagged invalid by system
        Returns
        ----------
            Rc: float
                Error Precision of the system
    """

    size = tn + fn

    ep = tn / size

    print('Weighted Levenshtein Error Precision : {:.2%} ({}) of {} words flagged invalid '
          'are real invalid words'
          .format(ep, tn, size))

    return ep


def lexical_f_score(lr: float, lp: float):
    """
        For the weighted levenshtein model with Trie Structure
        Harmonic mean of models' lexical precision and recall
        Parameters
        ----------
        lr: float
            lexical recall of the model
        lp: float
            lexical precision of the model
        Returns
        -------
            Print report
    """

    print('Weighted Levenshtein lexical F-score : {:.2%}'.format(2*((lp * lr) / (lp + lr))))


def error_f_score(er: float, ep: float):
    """
        For the weighted levenshtein model with Trie Structure
        Harmonic mean of models' error precision and recall
        Parameters
        ----------
        er: float
            Error recall of the model
        ep: float
            Error precision of the model
        Returns
        -------
            Print report
    """

    print('Weighted Levenshtein Error F-score : {:.2%}'.format(2*((ep * er) / (ep + er))))


def predictive_accuracy(tp: int, tn: int, fp: int, fn: int):
    """
        For the weighted levenshtein model with Trie Structure
        Overall precision of the model
        Parameters
        ----------
            tp: int
                # real valid words flagged valid by system
            tn: int
                # real invalid words flagged invalid by system
            fp: int
                # real invalid words flagged valid by system
            fn: int
                # real valid words flagged invalid by system
        Returns
        ----------
            Prints a report
    """

    size = tp + tn + fp + fn

    total_correct = tp + tn

    pa = total_correct / size

    print('Weighted Levenshtein Predictive Accuracy : {:.2%} ({}) of {} words correctly flagged valid or invalid'
          .format(pa, total_correct, size))


def suggestion_adequacy(test_set, verbose: bool = False):
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


def mean_reciprocal_rank(test_set):
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
    print('Weighted Levenshtein Mean Reciprocal Rank : {:.2f}'.format(total_reciprocal_rank / len(correct_suggestions)))


def edit_distance_stats(test_set):

    data = pairing(test_set)

    word_cost = {}

    for right, wrong in data:
        word_cost[wrong] = dynamic_levenshtein(wrong, right)

    print(Counter(word_cost.values()))


def error_stats(test_set):

    data = pairing(test_set)

    error = {}

    corrector = Corrector()

    for right, wrong in data:
        if corrector.get_suggestions(wrong)[0][0] != right:
            error[wrong] = dynamic_levenshtein(wrong, right)

    print(Counter(error.values()))


if __name__ == '__main__':
    Tp, Fn, Lr = lexical_recall(open('misspelled_wolof_words.txt'))
    Tn, Fp, Er = error_recall(open('misspelled_wolof_words.txt'))
    Lp = lexical_precision(Tp, Fp)
    Ep = error_precision(Tn, Fn)
    lexical_f_score(Lp, Lr)
    error_f_score(Ep, Er)
    predictive_accuracy(Tp, Tn, Fp, Fn)
    suggestion_adequacy(open('misspelled_wolof_words.txt'))
    mean_reciprocal_rank(open('misspelled_wolof_words.txt'))
    # edit_distance_stats(open('misspelled_wolof_words.txt'))
    # error_stats(open('misspelled_wolof_words.txt'))

