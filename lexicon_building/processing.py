"""
wolof lexicon processing
-----
Processing of several corpora and wolof dictionary to build a wolof lexicon used by the autocorrector
Contents:
    corpus processing,
    dictionary processing,
    masakhane_ner dataset processing,
    wolof_lexicon file creation
"""

import utils.wolof_rules as wr
from utils.spellchecker_utils import word_extraction
import re

exceptions = {'v', 'z', 'h'}

print("Processing wolof texts")
raw_words = word_extraction('wolof_texts.txt')
corpus_words = set([word for word in raw_words for word in re.split('(?<=.)(?=[A-Z])', word)])
for i in corpus_words.copy():
    if not i.isalpha() or i.isupper() or wr.fr_en_checking(i) or not wr.rules_validator(i):
        corpus_words.remove(i)

print("Processing wolof dictionary")
raw_dict = word_extraction('wolof_dictionary.txt')
dict_words = set([word for word in raw_dict for word in re.split('(?<=.)(?=[A-Z])', word)])
for j in dict_words.copy():
    if not j.isalpha() or j.isupper() or wr.fr_en_checking(j) or not wr.rules_validator(j):
        dict_words.remove(j)

lexicon = (corpus_words.union(dict_words))

for exception in exceptions:
    for word in lexicon.copy():
        if exception in word:
            lexicon.remove(word)

print("Creating wolof lexicon file")
with open('../lexicon1.txt', 'w') as f:
    for word in lexicon:
        f.write(word.lower() + '\n')

