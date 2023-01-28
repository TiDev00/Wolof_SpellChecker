import time
from utils.levenshtein import Corrector
from naive_spellchecking import get_probs, get_count, get_suggestions, word_extraction


def pairing(lines) -> list[tuple]:
    """
        Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')]
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


def lexical_recall():
    NotImplemented


def error_recall():
    NotImplemented


def precision():
    NotImplemented


def suggestion_adequacy_ns(test_set: str, verbose: bool = True):
    """
        For the naive levenshtein model
        Number of correct suggestions for invalid words for all the invalid words
        Also print the speed to do all the suggestions
        Parameters
        ----------
            test_set: List[str]
                File used to test systems
            verbose: bool
                Display or not correction for each word
        Returns
        ----------
            Prints reports
        """

    dataset = pairing(open(test_set, 'r'))

    vocab = []
    for w in open('utils/wolof_lexicon.txt', 'r').read().split():
        vocab.append(w)

    # noinspection PyTypeChecker
    probs = get_probs(get_count(word_extraction('utils/wolof_lexicon.txt')))

    good, unknown = 0, 0

    n = len(dataset)

    start = time.process_time()

    for right, wrong in dataset:
        # noinspection PyTypeChecker
        suggestion = (get_suggestions(wrong, probs, vocab))[0][0]

        good += (suggestion == right)
        if suggestion != right:
            unknown += (right not in vocab)
            if verbose:
                print('autocorrection({}) => {}; expected {}'
                      .format(wrong, suggestion, right))

    dt = time.process_time() - start

    print('{:.0%} of {} correct ({:.0%} unknown valid words) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))


def suggestion_adequacy_wl(test_set: str, verbose: bool = True):
    """
        For the weighted levenshtein model with Trie Structure
        Number of correct suggestions for invalid words for all the invalid words
        Also print the speed to do all the suggestions
        Parameters
        ----------
            test_set: List[str]
                File used to test systems
            verbose: bool
                Display or not correction for each word
        Returns
        ----------
            Prints reports
    """

    suggester = Corrector()

    dataset = pairing(open(test_set, 'r'))

    vocab = []
    for w in open('utils/wolof_lexicon.txt', 'r').read().split():
        vocab.append(w)

    good, unknown = 0, 0

    n = len(dataset)

    start = time.process_time()

    for right, wrong in dataset:
        suggestion = suggester.get_suggestions(wrong)[0][0]
        good += (suggestion == right)
        if suggestion != right:
            unknown += (right not in vocab)
            if verbose:
                print('autocorrection({}) => {}; expected {}'
                      .format(wrong, suggestion, right))

    dt = time.process_time() - start

    print('{:.0%} of {} correct ({:.0%} unknown valid words) at {:.0f} words per second '
          .format(good/n, n, unknown/n, n/dt))


if __name__ == '__main__':
    # list_mots = []
    # rep = []
    # data = open('misspelled_wolof_words.txt', 'r')
    # for item in data:
    #     print(item.split(':')[0])
    #     if item.split(':')[0] not in list_mots:
    #         list_mots.append(item.split(':')[0])
    #     else:
    #         rep.append(item.split(':')[0])
    # print(len(list_mots))
    # print(rep)


    # suggestion_adequacy_wl('misspelled_wolof_words.txt')

    suggestion_adequacy_ns('misspelled_wolof_words.txt')
