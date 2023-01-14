"""
Autocorrector that will read a given file and correct all the wolof misspelled words
"""

from utils.TrieNode import *
from utils.wolof_rules import *
from utils.spellchecker_utils import *

# TrieNode
DICTIONARY = 'wolof_lexicon.txt'
TARGET = 'borvom'
MAX_COST = int(2)

# read dictionary file into a trie
trie = TrieNode()
for word in open(DICTIONARY, "rt").read().split():
    trie.insert(word)


results = search(trie, TARGET, MAX_COST)

print(results)
