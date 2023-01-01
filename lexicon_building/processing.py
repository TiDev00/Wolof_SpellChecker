import re
import enchant

fr_dict = enchant.Dict('fr')
en_dict = enchant.Dict('en')
wolof_letters = 'aàãbcdeéëfgijklmnñŋoópqrstuwxy'

print("Processing wolof text")
with open('lexicon_building/wolof_text.txt') as f:
    data = f.read()
corpus_words = set([s for s in re.findall('\w+', data.lower()) if s.isalpha()
                    and not fr_dict.check(s) and not en_dict.check(s)])

print("Processing wolof dictionary")
with open('lexicon_building/wolof_dictionary.txt') as f:
    data = f.read()
dico_words = set([s for s in re.findall('\w+', data.lower()) if s.isalpha()
                    and not fr_dict.check(s) and not en_dict.check(s)])

glossary = sorted(corpus_words.union(dico_words))

print("Creating glossary file")
with open('wolof_lexicon.txt', 'w') as f:
    for word in glossary:
        if 'aaa' not in word and 'h' not in word and 'ï' not in word \
                and 'v' not in word and 'z' not in word and 'ç' not in word:
            f.write(word + '\n')

