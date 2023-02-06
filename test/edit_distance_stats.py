from utils.helper import dynamic_levenshtein
from test.spell_test import pairing
from collections import Counter

data = pairing(open('../misspelled_wolof_words.txt'))

word_cost = {}

for right, wrong in data:
    word_cost[wrong] = dynamic_levenshtein(wrong, right)

print(Counter(word_cost.values()))
