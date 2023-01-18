"""
Interactive spellchecker which will correct given word by user or give suggestions
"""

from utils.spellchecker_utils import *
from utils.wolof_rules import *



my_word = 'borvorm'
probs = get_probs(get_count(word_extraction('wol_corpus.txt')))
vocab = word_extraction('dico_wol.txt')
tmp_corrections = get_suggestions(my_word, probs, vocab, verbose=True)

