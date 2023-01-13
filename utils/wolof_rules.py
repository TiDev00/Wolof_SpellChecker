"""
wolof_rules
-----
Functions used to verify wolof word in accordance to the writing rules established.
Contents:
    fr_en_checking,
    compound_sound_transformation,
    rules_validator
"""

import re
import enchant

fr_lex = enchant.Dict('fr')
en_lex = enchant.Dict('en')

weak_wolof_consonants = {'p', 't', 'c', 'k', 'q', 'b', 'd', 'j', 'g', 'm', 'n', 'ñ', 'ŋ', 'f', 'r',
                         's', 'x', 'w', 'l', 'y'}
gemine_wolof_letters = {'pp', 'tt', 'cc', 'kk', 'bb', 'dd', 'jj', 'gg', 'ŋŋ', 'ww', 'll',
                        'mm', 'nn', 'yy', 'ññ', 'qq'}
prenasalized_wolof_letters = {'mp', 'nt', 'nc', 'nk', 'nq', 'mb', 'nd', 'nj', 'ng'}
strong_wolof_consonants = gemine_wolof_letters | prenasalized_wolof_letters
short_wolof_vowels = {'a', 'à', 'ã', 'i', 'o', 'ó', 'u', 'e', 'é', 'ë'}
long_wolof_vowels = {'ii', 'uu', 'éé', 'óó', 'ee', 'aa'}


def fr_en_checking(word: str) -> bool:
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
    if fr_lex.check(word.lower()) or en_lex.check(word.lower()):
        return True
    return False


def compound_sound_transformation(word: str) -> str:
    """
        Modifies writing of a word according to wolof writing rules.
        Deletes compound sounds like ou, oi, ch, an, en, eu, au, eau, ien, ienne, ai, gn, elle, ette, tion, oin
        ui, eil, eille, ouille, ail, aille, ueil, ier, ei, oeu, kh, gn, di, tch, ouss
        Parameters
        ----------
            word: str
                word which will be changed
        Returns
        ----------
            word: str
                new word written in wolof by taking into account wolof rules
    """
    fr_wol_maps = {'tion': 'siyoŋ', 'ouss': 'us', 'ouille': 'uy', 'ou': 'u', 'gn': 'ñ', 'kh': 'x', 'tch': 'c',
                   'oeu': 'ë', 'eu': 'ë', 'aille': 'ay', 'eille': 'ey', 'eau': 'óo', 'au': 'ó', 'ienne': 'iyen',
                   'oi': 'uwa', 'ui': 'uwi', 'gue': 'ge', 'gui': 'gi', 'gua': 'ga', 'v': 'w', 'z': 's', 'h': ''}
    word = word.lower()
    for k, v in fr_wol_maps.items():
        word = re.sub(k, v, word)
    return word


def rules_validator(word: str) -> bool:
    """
    Check if a given string respects several wolof writing rules
    Parameters
    ----------
        word: str
            word which we want to check
    Returns
    ----------
        correct_word: bool
            boolean which is True if the given word respects wolof writing rules
    """
    # word cannot end with long consonants and long vowels at same time
    for gl in gemine_wolof_letters:
        for lv in long_wolof_vowels:
            if word.lower().endswith(gl+lv):
                return False

    # strong consonant never follow long vowel
    for sc in strong_wolof_consonants:
        for lv in long_wolof_vowels:
            if lv+sc in word.lower():
                return False

    # strong consonant never start word except prenasalized letter
    for gl in gemine_wolof_letters:
        if word.lower().startswith(gl):
            return False

    return True


