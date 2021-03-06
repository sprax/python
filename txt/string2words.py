#!/usr/bin/env python3
'''
Parse a string into words
Usage: python string2words.py words.txt rainrajatacozapsrakezarfabetrainzany
'''


import argparse
from collections import Counter
from collections import defaultdict
import pdb
from pdb import set_trace
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
    '''load dictionary from text file, one word per line, IFF DICTIONARY is empty'''
    word_count = 0
    if DICTIONARY:
        return
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


def palindromes_with_one_or_more_anagrams(dictionary, verbose=1):
    ''' find all palindromes in the given dictionary with anagrams that are also palindromes '''
    result = []
    original_order = []
    letter_counts = defaultdict(int)
    word_anagrams = defaultdict(list)
    for word in dictionary:
        sorted_letters = "".join(sorted(word))
        letter_counts[sorted_letters] += 1
        word_anagrams[sorted_letters].append(word)
        if is_palindrome(word):
            original_order.append(sorted_letters)
    for sorted_letters in original_order:
        if letter_counts[sorted_letters] > 1:
            if verbose > 0:
                print(word_anagrams[sorted_letters])
            result.append(word_anagrams[sorted_letters])
    return result


def palindromes_with_palindromic_anagrams(dictionary, verbose=1):
    ''' find all palindromes in the given dictionary with anagrams that are also palindromes '''
    result = []
    original_order = []
    letter_counts = defaultdict(int)
    palindrome_anagrams = defaultdict(list)
    for word in dictionary:
        if is_palindrome(word):
            sorted_letters = "".join(sorted(word))
            palindrome_anagrams[sorted_letters].append(word)
            letter_counts[sorted_letters] += 1
            if letter_counts[sorted_letters] == 2:
                original_order.append(sorted_letters)
    for sorted_letters in original_order:
        if verbose > 0:
            print(palindrome_anagrams[sorted_letters])
        result.append(palindrome_anagrams[sorted_letters])
    return result


def two_word_palindromes_naive(dictionary, verbose=1):
    ''' find all 2-word palindromes in the given dictionary.
        Examples: "live evil", "go dog", "across orca", ...
        Naive brute force N-squared algorithm.
    '''
    result = []
    for word_a in dictionary:
        first = word_a[0]
        for word_b in dictionary:
            if first == word_b[-1]:
                if is_palindrome(word_a + word_b):
                    two_word_palindrome = word_a + " " + word_b
                    if verbose > 0:
                        print(two_word_palindrome)
                    result.append(two_word_palindrome)
    return result

def two_word_palindromes_sophomore(dictionary, verbose=1):
    ''' find all 2-word palindromes in the given dictionary.
        Examples: "live evil", "go dog", "across orca", ...
        Naive brute force N-squared algorithm.
    '''
    result = []
    rev_words = [word[::-1] for word in dictionary.keys()]
    rev_words.sort()
    r_0 = '\0'
    rev_words_segs = {}
    for rev_word in rev_words:
        if  r_0 < rev_word[0]:
            r_0 = rev_word[0]
            rev_words_seg = []
            rev_words_segs[r_0] = rev_words_seg
        rev_words_seg.append(rev_word)
    seg = 0
    for word_a in dictionary:
        a_0 = word_a[0]
        a_z = len(word_a)
        for word_r in rev_words_segs[a_0]:
            ord = 0
            for (aaa, bbb) in zip(word_a, word_r):
                if aaa != bbb:
                    break
                ord += 1
            else:
                r_z = len(word_r)
                if  a_z == r_z  or \
                    a_z < r_z and is_palindrome(word_r[ord:]) or \
                    a_z > r_z and is_palindrome(word_a[ord:]):
                    word_b = word_r[::-1]
                    two_word_palindrome = word_a + " " + word_b
                    if verbose > 0:
                        print(two_word_palindrome)
                    result.append(two_word_palindrome)
    return result


def two_word_palindromes(dictionary, verbose=1):
    ''' find all 2-word palindromes in the given dictionary.
        e.g. "live evil", "go dog", "across orca", "shallot ayatollahs"
    '''
    backward_words = []
    for word in dictionary.keys():
        backward_words.append(word[::-1]);
    # bwit = iter(sorted(backward_words))
    backward_words.sort()
    size = len(backward_words)
    idx = 0
    result = []
    next_a, next_b = False, False
    word_r = backward_words[idx]
    for word_a in dictionary:
        # if word_a == 'ten' or word_a == 'not':
        #     set_trace()
        while word_a[0:2] > word_r[0:2]:
            idx += 1
            if idx >= size:
                return result
            word_r = backward_words[idx]
        ord = 0
        for (aaa, bbb) in zip(word_a, word_r):
            if aaa != bbb:
                break
            ord += 1
            # if aaa < bbb:
            #     next_a = True
            #     break
            #  aaa > bbb:
            #     next_b = True
            #     break
        else:
            word_a_ord = word_a[0:ord]
            tmp = idx
            while True:
                word_b = word_r[::-1]
                if is_palindrome(word_a + word_b):
                    two_word_palindrome = word_a + " " + word_b
                    if verbose > 0:
                        print(two_word_palindrome)
                    result.append(two_word_palindrome)
                tmp += 1
                if tmp >= size:
                    return result
                word_r = backward_words[tmp]
                if word_r[0:ord] != word_a_ord:
                    break
            # idx += 1
            word_r = backward_words[idx]
        # if next_a:
        #     next_a = False
        #     continue
        # if next_b:
        #     next_b = False
        #     word_r = next(bwit)
    return result


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

    print("\n\t  palindromes_with_one_or_more_anagrams(DICTIONARY):")
    palindromes_with_one_or_more_anagrams(DICTIONARY)
    print("\n\t  palindromes_with_palindromic_anagrams(DICTIONARY):")
    palindromes_with_palindromic_anagrams(DICTIONARY)

    if True:
        print("\n\t  two_word_palindromes_sophomore(DICTIONARY):")
        twps = two_word_palindromes_sophomore(DICTIONARY)
    elif True:
        print("\n\t  two_word_palindromes_naive(DICTIONARY):")
        twps = two_word_palindromes_naive(DICTIONARY)
    else:
        print("\n\t  two_word_palindromes(DICTIONARY):")
        twps = two_word_palindromes(DICTIONARY)
    print("two_word_palindromes list len: ", len(twps))
    uniq = set(twps)
    print("two_word_palindromes  set len: ", len(uniq))
    return

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
