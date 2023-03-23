"""
autocorrector
-----
A module to autocorrect words in a given wolof text file and writes the corrected text to a new file
"""

import os
import sys
from utils.detection import Detector
from utils.weighted_levenshtein import Corrector
from utils.helper import fr_en_word
import re


detection = Detector()
correction = Corrector()

filepath = sys.argv[1]

# get the directory and filename from the input filepath
directory = os.path.dirname(filepath)
filename = os.path.splitext(os.path.basename(filepath))[0]

# read the text from the input file
with open(filepath, "r") as f:
    text = f.read()

# split the text into lines
lines = text.split("\n")

# correct the text line by line
corrected_lines = []
for line in lines:
    # use regular expression to split the line into words and punctuation
    words = re.findall(r"[\w']+|[^\w\s]", line)
    corrected_words = []
    for word in words:
        # ignore punctuation
        if not re.match(r"[\w']+|[^\w\s]", word):
            continue
        # process words
        if not fr_en_word(word) and not detection.checker(word):
            suggestions = correction.get_suggestions(word)
            if suggestions:
                corrected_word = suggestions[0][0]
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    # join the corrected words and punctuation to form the corrected line
    corrected_line = " ".join(corrected_words)
    corrected_lines.append(corrected_line)

# join the corrected lines with newline characters
corrected_text = "\n".join(corrected_lines)

# write the corrected text to a new file
output_filepath = os.path.join(directory, f"{filename}_corrected.txt")
with open(output_filepath, "w") as f:
    f.write(corrected_text)
