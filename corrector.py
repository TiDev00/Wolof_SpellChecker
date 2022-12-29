

my_word = 'borvorm'
probs = get_probs(get_count(word_extraction('wol_corpus.txt')))
vocab = set(word_extraction('dico_wol.txt'))
tmp_corrections = get_suggestions(my_word, probs, vocab, nbr_edit=2, verbose=True)

