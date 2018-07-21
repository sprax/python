#!/usr/bin/python3
'''
Parse a string into words
Usage: python string2words.py words.txt rainrajatacozapsrakezarfabetrainzany
'''

import sys

VERBOSE = 1
MIN_WORD_LEN = 2
MAX_WORD_LEN = 24
DICTIONARY = {}

def string2words_from_end_one(string, words_already_parsed):
    '''
    Recursively divide a string into string of words, backing up greedily from the end.
    Returns a string with spaces inserted between the words, or None if the parse fails.
    '''

    if  VERBOSE > 1:
        print("string2wordFromEnds: string(", string, ") words("
              , words_already_parsed, ")\n")

    # If the this string is a word, just return it with any words already parsed.
    if is_word(string):
        if words_already_parsed:
            return string + " " + words_already_parsed
        return string

    # Else divide the string into two parts, and if the 2nd part is a word, keep going.
    # Use min and max word lengths to skip checking substrings that cannot be words.
    max_index = len(string)
    min_index = max_index - MAX_WORD_LEN
    if  min_index < 0:
        min_index = 0
    max_index -= MIN_WORD_LEN
    while max_index > min_index:
        substr = string[max_index:]
        if is_word(substr):
            if words_already_parsed:
                substr += " " + words_already_parsed
            more_words = string2words_from_end_one(string[0:max_index], substr)
            if more_words:
                return more_words
        max_index -= 1
    return None          # string did not parse


def string2words_from_beg_all(string, words_already_parsed, all_parses):
    '''
    Recursively divide a string into array of strings of words,
    going greedily from the beginning.
    Returns a string with spaces inserted between the words, or None if the parse fails.
    '''

    if  VERBOSE > 1:
        print("string2words_from_beg_all: string(", string, ") words("
              , words_already_parsed, ")\n")

    # If the this string is a word, just return it with any words already parsed.
    if is_word(string):
        if words_already_parsed:
            parsed = string + " " + words_already_parsed
        else:
            parsed = string
        all_parses.append(parsed)

    # Else divide the string into two parts, and if the 2nd part is a word, keep going.
    # Use min and max word lengths to skip checking substrings that cannot be words.
    max_index = len(string)
    min_index = max_index - MAX_WORD_LEN
    if  min_index < 0:
        min_index = 0
    max_index -= MIN_WORD_LEN
    while max_index > min_index:
        substr = string[max_index:]
        if is_word(substr):
            if words_already_parsed:
                substr += " " + words_already_parsed
            string2words_from_beg_all(string[0:max_index], substr, all_parses)
        max_index -= 1
    # No return value; any results were appended to all_parses.


def load_dictionary(file_name):
    '''load dictionary from text file, one word per line'''
    word_count = 0
    for line in open(file_name):  # opened in text-mode; all EOLs are converted to '\n'
        line = line.rstrip('\n')
        size = len(line)
        word_count += 1
        DICTIONARY[line] = size
    print("Read ", word_count, " words from dictionary file: ", file_name, "\n")

def is_word(string):
    '''true iff dictionary word'''
    return DICTIONARY.get(string)


def is_palindrome(data):
    '''true iff palindrome'''
    half_len = int(len(data) / 2)
    for j in range(half_len):
        if  data[j] != data[-j-1]:
            return False
    return True


def test_is_palindrome(string):
    '''test if argument is a palindrome'''
    print("string", string, "is a palindrome? ", is_palindrome(string))
    i_tuple = (1, 2, 3, 2, 1)
    print("i_tuple", i_tuple, "is a palindrome? ", is_palindrome(i_tuple))
    i_list = [4, 5, 6, 7, 7, 6, 5, 4]
    print("i_list", i_list, "is a palindrome? ", is_palindrome(i_list))


def test_string2words():
    '''test the string2words functions'''
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "words.txt"

    if len(sys.argv) > 2:
        strings = [sys.argv[2:]]
    else:
        strings = ["minimumergold", "garbageatone", 'atone']

    test_is_palindrome(strings[0])

    load_dictionary(file_name)

    if len(sys.argv) > 3:
        word = sys.argv[3]
        print("is_word(", word, ") returned ", is_word(word), "\n")

    for string in strings:
        ret = string2words_from_end_one(string, "")
        num_parses = 0
        if ret != None:
            num_parses = 1
        print("string2words_from_end_one got", num_parses, "(" + ret + ")")
        all_parses = []
        string2words_from_beg_all(string, "", all_parses)
        num_parses = len(all_parses)
        print("string2words_from_beg_all got", str(num_parses), all_parses)

if __name__ == '__main__':
    test_string2words()
