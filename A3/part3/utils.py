import re

from math import log

words_only_regex = re.compile(r"[a-zA-Z]{2,}")

def get_processed_words_from_file(filename):
    f_contents = None
    with open(filename, 'r', encoding="Latin-1") as f:
        f_contents = f.read()
    #change to lowercase
    f_contents = f_contents.lower()
    #get array of words with length more than 1
    return words_only_regex.findall(f_contents)
