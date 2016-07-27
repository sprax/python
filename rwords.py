#!/usr/bin/env python3
# Sprax Lines       2016.07.25      Written with Python 3.5
'''Class and driver script to solve simple substitution cipher from
a corpus and encoded text in separate text files.
'''

import heapq
import re
import sys
from collections import defaultdict
from collections import Counter

class SubCipher:
    '''Solver to infer a simple substituion cipher based on a large
    corpus and small sample of encoded text.   Assumes English for
    boot-strapping off these four words: I, a, the, and.'''
    def __init__(self, cipher_file, corpus_file, verbose):
        self.cipher_file = cipher_file
        self.corpus_file = corpus_file
        self.cipher_lines = read_file_lines(cipher_file)
        self.cipher_short, self.cipher_words = word_counts_short_and_long(cipher_file, 1)
        self.corpus_short, self.corpus_words = word_counts_short_and_long(corpus_file, 1)
        self.cipher_chars = count_chars_from_words(self.cipher_words)
        self.corpus_chars = count_chars_from_words(self.corpus_words)
        self.forward_map = defaultdict(int)
        self.inverse_map = defaultdict(int)
        self.inverse_score = 0
        self.verbose = verbose
        if self.verbose > 1:
            print("The dozen most common corpus words and their counts:")
            for word, count in self.corpus_words.most_common(12):
                print("\t", word, "\t", count)

    def assign(self, corp, ciph):
        '''Assigns corpus char -> cipher char in the forward cipher map,
        and the opposite in the inverse map.  Asserts that these character
        are not already mapped.  TODO: Replace assert with actual error?'''
        assert self.forward_map[corp] == 0, (
            "Cannot forward assign {} -> {} because already {} -> {}"
            .format(corp, ciph, corp, self.forward_map[corp]))
        assert self.inverse_map[ciph] == 0, (
            "Cannot inverse assign {} -> {} because already {} -> {}"
            .format(corp, ciph, self.inverse_map[ciph], ciph))
        self.forward_map[corp] = ciph
        self.inverse_map[ciph] = corp
        if self.verbose > 1:
            print("Accept", corp, "->", ciph)

    def find_a_and_i(self):
        '''Try to find the word "I" as the most common capitalized
        single-letter word, and "a" as the most common lowercase
        single-letter word.  Assuming English, obviously.'''
        if self.verbose > 0:
            print("Search for the words 'a' and 'I'")

        # Peek at these most common corpus words as a sanity-check
        corp_ai = self.corpus_short.most_common(2)
        corpchars = (corp_ai[0][0], corp_ai[1][0])
        if corpchars != ('a', 'I') and corpchars != ('I', 'a'):
            print("Unexpected most common 1-letter words in corpus: ", corp_ai)

        ciph_ai = self.cipher_short.most_common(2)
        if ciph_ai[0][0].islower():
            self.assign('a', ciph_ai[0][0])
            self.assign('i', ciph_ai[1][0].lower())
        else:
            self.assign('a', ciph_ai[1][0])
            self.assign('i', ciph_ai[0][0].lower())

    def find_the_and_and(self):
        '''Try to find the two most common English words: "the" and "and".'''
        if self.verbose > 0:
            print("Search for the words 'the' and 'and'")

        # Peek at these most common corpus words as a sanity-check
        corps = self.corpus_words.most_common(2)
        words = (corps[0][0], corps[1][0])
        if words != ('the', 'and') and words != ('and', 'the'):
            print("Unexpected most common 3-letter words in corpus: ", corps)

        most_freq_ciphs = self.cipher_chars.most_common(2)
        probable_e = most_freq_ciphs[0][0]
        alternate_e = most_freq_ciphs[0][0]
        found_and = False
        found_the = False
        for item in self.cipher_words.most_common(10):
            ciph = item[0]
            if len(ciph) == 3:
                if not found_the and (ciph[2] == probable_e or ciph[2] == alternate_e):
                    found_the = True
                    self.assign('t', ciph[0])
                    self.assign('h', ciph[1])
                    self.assign('e', ciph[2])
                if not found_and and ciph[0] == self.forward_map['a']:
                    found_and = True
                    self.assign('n', ciph[1])
                    self.assign('d', ciph[2])

    def find_words_from_ciphers(self):
        '''Find common corpus words comprised mostly of known inverse
        cipher chars, and try filling in the missing letters.  Trials
        are evaluated by scoring how many decoded cipher words then
        match corpus words.  The highest score wins.  (That is, the
        decision is immediate, not defered to accumulate multiple
        scoring passes or backpropogating votes.'''
        num_words = len(self.corpus_words)
        corpus = self.corpus_words.most_common(num_words) # Just try them all
        inverse_pq = [] # priority = [num_unknown (updated on pop), -count, length]
        for ciph, count in self.cipher_words.items():
            entry = [self.number_of_unknowns(ciph), -count, len(ciph), ciph]
            heapq.heappush(inverse_pq, entry)

        sentinel = ''   # terminate the loop when the sentinel is seen a second time
        while inverse_pq:
            num_unk, neg_count, length, ciph = heapq.heappop(inverse_pq)
            if num_unk == 0:
                continue
            num_unk, idx_unk = self.num_idx_unknown(ciph)   # update (unknowns can become known)
            if num_unk == 1:
                self.inverse_match_1_unknown(ciph, length, idx_unk, corpus)

            elif num_unk > 1:
                if ciph == sentinel:
                    print('Breaking from queue at: ', ciph, num_unk, -neg_count)
                    break
                elif not sentinel:
                    # Set the sentinel and give each item still in the queue
                    # a chance to update its unknowns.  Some may change to 1
                    # and get matched.  Quit when the sentinel comes back to
                    # the front.
                    sentinel = ciph
                    print('Repush entry [', ciph, num_unk, -neg_count, '] to end of the queue')
                    heapq.heappush(inverse_pq, [1000, 0, length, ciph])
            elif self.verbose > 2:
                print('\tAlready deciphered: ', num_unk, -neg_count, ciph
                      , self.decipher_word(ciph))

    def inverse_match_1_unknown(self, ciph, length, idx_unknown, corpus):
        '''Try to match one cipher word with a single unknown against all
        corpus words of same length.  Accept the match that maximaly
        improves the total score (if there is any such a match).'''
        ## print('Trying to match: ', ciph, 1, count)
        self.inverse_score = self.score_inverse_map()
        ciph_char = ciph[idx_unknown]
        max_score = 0
        max_char = 0
        max_word = ''
        deciphered = self.decipher_word(ciph)
        for word, _ in corpus:
            if len(word) == length:
                # Match inverted ciphers to word chars
                for idx in range(length):
                    if idx == idx_unknown:
                        continue            # skip over the single unknown
                    if word[idx] != deciphered[idx]:
                        break               # break on the first known mismatch
                else:                       # all known chars matched, hole excluded
                    # Compute the total score that would result from accepting this mapping
                    word_char = word[idx_unknown]
                    self.inverse_map[ciph_char] = word_char # create temporary inverse mapping
                    try_score = self.score_inverse_map()    # compute score with this mapping
                    self.inverse_map[ciph_char] = 0         # delete temporary inverse mapping
                    if max_score < try_score:
                        max_score = try_score
                        max_char = word_char
                        max_word = word

        if max_score > self.inverse_score:
            old_forward = self.forward_map[max_char]
            count = self.cipher_words[ciph]
            # Must delete the previous forward mapping, if it exists
            if old_forward != 0:
                if self.verbose > 0:
                    old_word = self.decipher_word(ciph)
                    print("Delete {} -> {} because {} x '{}' => '{}' gave old score: {}".format(
                        max_char, self.forward_map[max_char], count, ciph, old_word, self.inverse_score))
                self.forward_map[max_char] = 0
                self.inverse_map[old_forward] = 0
            if self.verbose > 0:
                print("Assign {} -> {} because {} x '{}' => '{}' gives new score {} > {}".format(
                    max_char, ciph_char, count, ciph, max_word, max_score, self.inverse_score))
            self.inverse_score = max_score
            self.assign(max_char, ciph_char)

    def update_mapping_on_better_score(self, ciph, idx_unknown, max_word, max_score):
        ciph_char = ciph[idx_unknown]
        max_char = max_word[idx_unknown]
        old_forward = self.forward_map[max_char]
        count = self.cipher_words[ciph]
        # Must delete the previous forward mapping, if it exists
        if old_forward != 0:
            if self.verbose > 0:
                old_word = self.decipher_word(ciph)
                print("Delete {} -> {} because {} x '{}' => '{}' gave old score: {}".format(
                    max_char, self.forward_map[max_char], count, ciph, old_word, self.inverse_score))
            self.forward_map[max_char] = 0
            self.inverse_map[old_forward] = 0
        if self.verbose > 0:
            print("Assign {} -> {} because {} x '{}' => '{}' gives new score {} > {}".format(
                max_char, ciph_char, count, ciph, max_word, max_score, self.inverse_score))
        self.inverse_score = max_score
        self.assign(max_char, ciph_char)

    def score_inverse_map(self):
        '''score based on totality of deciphered cipher words matching corpus words'''
        score_total = 0
        for ciph, ciph_count in self.cipher_words.items():
            word = self.decipher_word(ciph)
            word_count = self.corpus_words[word]    # 0 if not in corpus
            score = word_count * ciph_count * len(ciph)
            ##print(" {:9}\t {} => {}".format(score, ciph, word))
            score_total += score
        return score_total

    def number_of_unknowns(self, ciph):
        '''returns the number of unknown cipher characters in the string ciph'''
        return sum(map(lambda x: self.inverse_map[x] == 0, ciph))

    def num_idx_unknown(self, ciph):
        '''returns the number of unknown cipher characters in the string ciph
        and the index of the right-most unknown'''
        num_unknown = 0
        idx_unknown = -1
        idx = 0
        for fwd in ciph:
            inv = self.inverse_map[fwd]
            if inv == 0:
                num_unknown += 1
                idx_unknown = idx
            idx += 1
        return num_unknown, idx_unknown

    def decipher_word(self, encoded_word):
        '''Replace contents of encoded_word with inverse mapped chars'''
        out = []
        for fwd in encoded_word:
            inv = self.inverse_map[fwd]
            if inv == 0:
                out.append('_')
            else:
                out.append(inv)
        return ''.join(out)

    def decipher_text(self, line):
        '''Decode any string using the current inverse cipher map.  Only lower
        and upper case ASCII letters will be changed, preserving case.'''
        decoded = []
        for char in line:
            if char >= 'a' and char <= 'z':
                inv = self.inverse_map[char]
                decoded.append(inv if inv else '_')
            elif char >= 'A' and char <= 'Z':
                inv = self.inverse_map[char.lower()]
                decoded.append(inv.upper() if inv else '_')
            else:
                decoded.append(char)
        return ''.join(decoded)

    def print_deciphered_words(self, outfile=sys.stdout):
        '''Print all the words from the cipher file as decoded using
        the current inverse_map to stdout (default) or a file'''
        for ciph in self.cipher_words.keys():
            print(ciph, '=>', self.decipher_word(ciph), file=outfile)

    def print_forward_map(self, outfile=sys.stdout):
        '''Print the forward cipher mapping to stdout (default) or a file'''
        for word_char in char_range_inclusive('a', 'z'):
            ciph_char = self.forward_map[word_char]
            print(word_char, "->", ciph_char if ciph_char else ' ', file=outfile)

    def print_deciphered_lines(self, outfile=sys.stdout):
        '''Print the decoded contents of the original cipher file to the console
        (default) or a file'''
        for line in self.cipher_lines:
            text = self.decipher_text(line)
            if outfile == sys.stdout:
                uprint(text)                # compensate for non-UTF-terminals
            else:
                print(text, file=outfile)

    def write_forward_cipher_key(self, path):
        '''Write the forward cipher mapping into a new file.'''
        with open(path, 'w') as out:
            self.print_forward_map(out)
            out.close()

    def write_deciphered_text(self, path):
        '''Write the decoded contents of the original cipher file into a new file'''
        with open(path, 'w') as out:
            self.print_deciphered_lines(out)
            out.close()

def uprint(*objects, sep=' ', end='\n', outfile=sys.stdout):
    '''Prints non-ASCII Unicode (UTF-8) characters in a safe (but possibly
    ugly) way even in a Windows command terminal.  Unicode-enabled terminals
    such as on Mac or KDE have no problem, nor do most IDE's, but calling
    Python's built-in print to print such characters (e.g., an em-dash)
    from a Windows cmd or Powershell terminal causes errors such as:
    UnicodeEncodeError: 'charmap' codec can't encode characters in position 32-33:
    character maps to <undefined> '''
    enc = outfile.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=outfile)
    else:
        enc_dec = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(enc_dec, objects), sep=sep, end=end, file=outfile)

def char_range_inclusive(first, last, step=1):
    '''ranges from specified first to last character, inclusive, in
    any character set, depending only on ord()'''
    for char in range(ord(first), ord(last)+1, step):
        yield chr(char)


def read_file_lines(path):
    '''reads a text file into a list of lines'''
    lines = []
    with open(path, 'r') as text:
        for line in text:
            lines.append(line.rstrip())
    return lines

def count_words(path):
    '''Returns a Counter that has counted all ASCII-only words found in a text file.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    counter = Counter()
    with open(path, 'r') as text:
        for line in text:
            words = re.findall(rgx_match, line.rstrip())
            words = [x.lower() if len(x) > 1 else x for x in words]
            counter.update(words)
    return counter

def word_counts_short_and_long(path, max_short_len):
    '''Returns two Counters containing all the ASCII-only words found in a text file.
       The first counter counts only words up to length max_short_len, as-is.
       The second counter contains all the longer words, but lowercased.'''
    rgx_match = re.compile(r"[A-Za-z]+")
    short_counter = Counter()
    other_counter = Counter()
    with open(path, 'r') as text:
        for line in text:
            short = []
            other = []
            words = re.findall(rgx_match, line.rstrip())
            for word in words:
                if len(word) <= max_short_len:
                    short.append(word)
                else:
                    other.append(word.lower())
            short_counter.update(short)
            other_counter.update(other)
    return short_counter, other_counter

def count_chars_from_words(word_counter):
    '''Count chars from all words times their counts'''
    char_counter = Counter()
    for item in word_counter.items():
        for _ in range(item[1]):
            char_counter.update(item[0])
    return char_counter

def solve_simple_substition_cipher(cipher_file, corpus_file, verbose):
    '''Given a file of ordinary English sentences encoded using a simple
    substitution cipher, and a corpus of English text expected to contain
    most of the words in the encoded text, decipher the encoded file.
    Uses the SubCipher class.
    '''
    subs = SubCipher(cipher_file, corpus_file, verbose)
    subs.find_a_and_i()
    subs.find_the_and_and()
    subs.find_words_from_ciphers()
    if verbose > 1:
        subs.print_deciphered_words()
    score = subs.score_inverse_map()
    print("Score from all matched words using the key below: ", score)
    subs.print_forward_map()
    subs.print_deciphered_lines()
    subs.write_forward_cipher_key(cipher_file + ".key")
    subs.write_deciphered_text(cipher_file + ".decoded")

def main():
    '''Get file names for cipher and corpus texts and call
    solve_simple_substition_cipher.'''

    # simple, inflexible arg parsing:
    argc = len(sys.argv)
    if argc > 2:
        print(sys.argv[0])
        print(__doc__)

    # Get the paths to the files (relative or absolute)
    cipher_file = sys.argv[1] if argc > 1 else r'cipher.txt'
    corpus_file = sys.argv[2] if argc > 2 else r'corpus.txt'

    verbose = 1
    solve_simple_substition_cipher(cipher_file, corpus_file, verbose)


if __name__ == '__main__':
    main()
