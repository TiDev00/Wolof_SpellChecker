"""
Test data building
-----
Processing of wolof lexicon file to build a corpus of misspelled words
Contents:
    wolof lexicon processing,
    random word extraction,
    corpus building
"""

import random
from utils.spellchecker_utils import word_extraction

wolof_lexicon = word_extraction('../wolof_lexicon.txt')

with open('../test_data.txt', 'w') as f:
    for word in random.sample(wolof_lexicon, 275):
        f.write(word.lower() + '\n')
    f.close()

