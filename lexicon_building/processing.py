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

exceptions = {'v', 'z', 'h'}

print("Processing wolof texts")
corpus_words = set(word_extraction('wolof_texts.txt'))
for i in corpus_words.copy():
    if not i.isalpha() or i.isupper() or wr.fr_en_checking(i) or not wr.rules_validator(i):
        corpus_words.remove(i)


print("Processing wolof dictionary")
dico_words = set(word_extraction('wolof_dictionary.txt'))
for j in dico_words.copy():
    if not j.isalpha() or j.isupper() or wr.fr_en_checking(j) or not wr.rules_validator(j):
        dico_words.remove(j)

glossary = (corpus_words.union(dico_words))

for exception in exceptions:
    for word in glossary.copy():
        if exception in word:
            glossary.remove(word)


print("Creating lexicon file")
with open('../wolof_lexicon.txt', 'w') as f:
    for word in glossary:
        f.write(word + '\n')

