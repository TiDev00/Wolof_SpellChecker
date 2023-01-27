"""
Autocorrector that will read a given file and correct all the wolof misspelled words
"""

from utils.levenshtein import Corrector

suggester = Corrector()

suggestions = suggester.get_suggestions("")
print(suggestions)
