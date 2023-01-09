"""
wolof lexicon processing
-----
Processing of several corpora and wolof dictionary to build a wolof lexicon used by the autocorrector
Contents:
    corpus processing,
    dictionary processing,
    masakhane_ner dataset processing
"""

import utils.wolof_rules as wr
from utils.spellchecker_utils import word_extraction


print("Processing wolof text")
corpus_words = set(word_extraction('wolof_texts.txt'))
for i in corpus_words.copy():
    if not i.isalpha() or wr.fr_en_checking(i) or not wr.rules_validator(i):
        corpus_words.remove(i)


print("Processing wolof dictionary")
dico_words = set(word_extraction('wolof_dictionary.txt'))
for j in dico_words.copy():
    if not j.isalpha() or wr.fr_en_checking(j) or not wr.rules_validator(j):
        dico_words.remove(j)

glossary = (corpus_words.union(dico_words))


print("Creating lexicon file")
with open('../wolof_lexicon.txt', 'w') as f:
    for word in glossary:
        if 'aaa' not in word and 'h' not in word and 'ï' not in word \
                and 'v' not in word and 'z' not in word and 'ç' not in word:
            f.write(word + '\n')

