from utils.TrieNode import *


# SpellChecker_utils
# my_word = 'borvorm'
# probs = get_probs(get_count(word_extraction('wol_corpus.txt')))
# vocab = set(word_extraction('dico_wol.txt'))
# tmp_corrections = get_suggestions(my_word, probs, vocab, nbr_edit=2, verbose=True)

# TrieNode
DICTIONARY = 'wolof_lexicon.txt'
TARGET = 'borvom'
MAX_COST = int(2)

# read dictionary file into a trie
trie = TrieNode()
for word in open(DICTIONARY, "rt").read().split():
    WordCount += 1
    trie.insert(word)

print("Read %d words into %d nodes" % (WordCount, NodeCount))

start = time.time()
results = search(trie, TARGET, MAX_COST)
end = time.time()

for result in results:
    print(result)

print("Search took %g s" % (end - start))
