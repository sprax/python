#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# # # coding: iso-8859-15
'''
FIXME: fix wrong syllable segmentation for "asexual", "abort", "Obama", etc.

Plan:
    Words|phrases -> words >= [phonetic syllables reprs]
    Emojis >= [phontic syllable reprs]
    Text => <syllabic repr> => <emoji>
'''

import argparse
import re
import string
# from collections import defaultdict
from collections import namedtuple
from nltk.corpus import cmudict
from text_regex import words_split_out
from text_regex import word_tokens
import hyphenate

def syl_count_cmu(pron):
    '''number of syllables in a CMU-style pronunciation'''
    return sum(str.isdigit(syl[-1]) for syl in pron)

def syl_count_cmu_max(cmu_prons, word):
    '''
    Return the CMU syllable count for word (max if there are alternates),
    or KeyError.  The word should already be lowercased.
    '''
    prons = cmu_prons[word]
    return max(syl_count_cmu(pron) for pron in prons)

def syl_count_cmu_min(cmu_prons, word):
    '''
    Return the CMU syllable count for word (min if there are alternates),
    or KeyError.  The word should already be lowercased.
    '''
    prons = cmu_prons[word]
    return min(syl_count_cmu(pron) for pron in prons)

def syl_count_cmu_first(cmu_prons, word):
    '''
    Return the CMU syllable count for word (first if there are alternates),
    or KeyError.  The word should already be lowercased.
    '''
    first = cmu_prons[word][0]
    return syl_count_cmu(first)


EXAMPLES = {
    "There isn't one empyrean ouroborous; everyone knows there've always been several." : (11, 24),
    #  1   2  3  4   5  6 78   9 0 1  2   3 4* 5     6     7  8   9  0    1    2 3 4
    '"There aren\'t really any homogeneous cultures," you\'ll say, "they\'ve always shown rifts."' : (12, 21),
    #   1   2        3   5 6 7  8 9 0 1 2   3  4        5      6      7      8  9     0    1
    '"Ain\'t all y\'all young\'uns under 17," she\'d said, "like 11- or 15-years old?!"' : (13, 21),
    #  1     2      3    4     5   6  7  +3     1     2      3   +3  7  +2  0    1}
    "Didn't you know a X-15's XLR-99 engine burns 15,000 pounds (6,717 kg) of propellant in 87 seconds?" : (17, 35),
    # 1  2   3    4  5 6 +2    +3 +2 4  5    6     +2  +2  1     +3  +8 +3  6    7 8  9   0  +3  4 5
}


VOWEL_EXP = "ae|ai|au|ay|a|ea|ei|eu|ey|e|iou|ie|i|oa|oe|oi|ou|oy|o|ue|u|y|dn't|sn't"
VOWEL_GROUPS = VOWEL_EXP.split('|')
VOWEL_STR = ' '.join(VOWEL_GROUPS)

RE_VOWEL_GROUPS = re.compile("(?i)%s" % VOWEL_EXP)
# print('VOWEL_GROUPS: (', VOWEL_STR, ')\n')

def count_vowel_groups(word):
    '''crude dipthong & vowel count standing in for syllables'''
    vgm = RE_VOWEL_GROUPS.findall(word)
    # print("count_vowel_gp:", vgm)
    return len(vgm)

def count_vowels_first_last(word):
    '''naive rules to count syllables'''
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    oldc = word[0]
    if oldc in vowels:
        count += 1
    for nxtc in word[1:]:
        if nxtc in vowels and oldc not in vowels:
            count += 1
        oldc = nxtc
    if word.endswith('le'):
        count += 1
    elif word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    return count


def syllable_count(cmu_prons, word):
    '''
    syllable count: from the first CMU pronunciation, if found,
    or a calculated one.  The word should already be lowercased.
    '''
    try:
        return syl_count_cmu_first(cmu_prons, word)
    except KeyError:
        return count_vowel_groups(word)

def syl_count_sum(cmu_prons, words):
    '''sum of syllable counts for a sequence of lowercased words or tokens'''
    return sum(syllable_count(cmu_prons, word) for word in words)


def syl_count_sentence(cmu_prons, sentence):
    '''sum of syllable counts for all tokens found in a sentence'''
    return syl_count_sum(cmu_prons, word_tokens(sentence))

TOMATO = [['T', 'AH0', 'M', 'EY1', 'T', 'OW2'], ['T', 'AH0', 'M', 'AA1', 'T', 'OW2']]

# NamedTuple to hold basic info on the phonetic sequencing of some text, such as a word.
PhoneTuple = namedtuple('PhoneTuple', 'length phonetics count syllables')

def phone_seq_1(pron, verbose=0):
    '''
    Extracts a syllable-count, phonetic string representation,
    and a phonetic syllable list from a CMU-style pronunciation sequence.
    ALGORITHM:
        Add any phoneme to pending syllable S up to an including the vowel sound,
            marked with a number (usually 0, 1, 2, where 1 means stressed).
            Set oldaccent.
        After oldaccent, get the next phoneme P, and:
            If P is NIL (because the word ended), save the pending (open) syllable S and break.
            If P is another vowel, save the pending (open) syllable S and start a new one with P.
            If P is a consonant, look ahead to the phoneme Q.
                If Q is NIL (because the word ended), save S+P as the final (closed) syllable and break.
                If Q is a consonant, save S+P as a (closed) syllable
                    and continue (or start a new S with Q and skip ahead).
                If Q is a stressed vowel, save (open) syllable S and start a new S with P (or P+Q and skip ahead).
                If Q is an unstressed vowel (marked by 0 or 2):
                    If S's vowell was stressed (marked 1), then save S+P as a (closed) syllable
                    and continue (or start a new S with Q and skip ahead).
                    Else (neither S nor Q has a stressed vowel):
                        For now, save current S as an (open) syllable and start new syllable with P+Q.

        EXAMPLE: 'potato' => ['P', 'AH0', 'T', 'EY1', 'T', 'OW2']
        EXAMPLE: 'potable' =>['P', 'OW1', 'T', 'AH0', 'B', 'AH0', 'L']
        Examples: arthroscopy ar·thros·co·py (är-thrŏs'kə-pē);  anthropology  [an-thruh-pol-uh-jee];
            asexual [ey-sek-shoo-uh l]; lobotomy [luh-bot-uh-mee, loh-]; unconscious /ʌnˈkɒnʃəs/
        Counters: laparectomy [lap-uh-rek-tuh-mee]; unconscious [uhn-kon-shuh s]
        Example/Counter:    la·pel vs lap·i·da·ry and lap·a·ro·to·my
        Example/Counter:    sop·o·rif·ic vs so·pran·o
        Thus:  O·bam·a vs. Ob·am·a vs. O·ba·ma?  No, it's only O·bam·a.
        @Deprecated because dumb about dividing multiple consonants, e.g. "lengthwise"
        Also wrong about "aardvark"
    '''
    if verbose > 1:
        print("- - - - - - - - - - phone_seq_1 - - - - - - - - - - - -")
    syl_count = 0
    phon_list = []
    syllables = []
    sylstring = ''
    oldaccent = None
    prev_cons = False
    idx, end = 0, len(pron)
    while idx < end:
        phon = pron[idx]
        last = phon[-1]
        if verbose > 1:
            print("=============================== phon: %s \t last: %s" % (phon, last))
        if '0' <= last and last <= '9':
            # This phon is a vowel string; strip off the digit and increment the syllable  count.
            vowels = phon[0:-1]
            phon_list.append(vowels)
            syl_count += 1
            if oldaccent:
                # End of an open syllable.  Save it and start new syllable.
                if verbose > 0:
                    print("syllables{} appending OPEN {}".format(syllables, sylstring))
                syllables.append(sylstring)
                sylstring = vowels
                oldaccent = last
            else:
                oldaccent = last
                sylstring += vowels
            prev_cons = False
        else:
            # This phon P is a consonant string.
            phon_list.append(phon)
            if sylstring:
                nxti = idx + 1
                if oldaccent:
                    if prev_cons:
                        # Already got a consonant following a vowel, so this is the
                        # end of a closed syllable.  Save it and start a new one.
                        if verbose > 0:
                            print("syllables{} appending CLOSED {}".format(syllables, sylstring))
                        syllables.append(sylstring)
                        sylstring = phon
                        oldaccent = None
                        prev_cons = True
                    else:
                        # The previous phoneme was the vowel string.  Must decide:
                        # append this consonant to current syllable or start a new one?
                        if nxti < end:
                            # Look ahead:
                            nxtp = pron[nxti]
                            nxtf = nxtp[-1]
                            if verbose > 1:
                                print("+++++++++++++++++++++++++++++++++++++ nxtp: %s \t nxtf: %s" % (nxtp, nxtf))
                            if '0' <= nxtf and nxtf <= '9':
                                if verbose > 3:
                                    print("# Next phon is vowels")
                                syl_count += 1
                                vowels = nxtp[0:-1]
                                phon_list.append(vowels)
                                if nxtf == '1' or oldaccent != '1':
                                    if verbose > 1:
                                        print("# Next phoneme Q = %s is a stressed vowel (%s) or prev was unstressed (%s)" % (
                                            vowels, nxtf, oldaccent), end='')
                                        print("; new syllable takes current consonant P.")
                                        print("syllables{} appending OPEN {}".format(syllables, sylstring))

                                    syllables.append(sylstring)
                                    sylstring = phon + vowels
                                else:
                                    if verbose > 1:
                                        print("# Next phoneme Q is an unstressed vowel;", end='')
                                        print(" current syllable appends current P.")
                                    syllables.append(sylstring + phon)
                                    sylstring = vowels
                                oldaccent = nxtf
                                prev_cons = False
                            else:
                                phon_list.append(nxtp)
                                if verbose > 2:
                                    print("# Next phon is a consonant")
                                    print("syllables{} appending CLOSED {}".format(syllables, sylstring + phon))
                                syllables.append(sylstring + phon)
                                sylstring = nxtp
                                oldaccent = None
                                prev_cons = True
                            idx = nxti
                        else:
                            if verbose > 3:
                                print(">>>>>>>> TRIED TO LOOK AHEAD AND SAW THE END with phon = %s" % phon)
                            sylstring += phon

                else:
                    # So sylstring is not empty, but does not yet have a vowel.  Just append current consonant P.
                    sylstring += phon
                    prev_cons = True
            else:
                # The syllable string is empty, so start a new one with this consonant.
                sylstring = phon
                assert oldaccent is None
                prev_cons = True
        idx = idx + 1

    if oldaccent:
        if verbose > 0:
            print("WORD syllables{} appending {}\n".format(syllables, sylstring))
        syllables.append(sylstring)
    else:
        if verbose > 0:
            print("WORD syllables{} appending {} to last syllable\n".format(syllables, sylstring))
        syllables[-1] += sylstring
    if verbose > 2:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> phon_list:", phon_list)
    phonetics = ''.join(phon_list)
    len_syllables = len(syllables)
    if syl_count != len_syllables:
        print("syl_count != len(syllables): %d v. %d" % (syl_count, len_syllables))

    return PhoneTuple(len(phonetics), phonetics, syl_count, syllables)

TRANS_PCONS = str.maketrans({'k': 'c'})
TRANS_PARTS = str.maketrans({'c': 'k'})

def phone_seq_2(pron, hyphenator, verbose=0):
    '''Extract PhoneTuple from a CMU-style pronunciation sequence, no look ahead.'''
    if verbose > 1:
        print("= = = = = = = = = = phone_seq_2 = = = = = = = = = = = =")
    phons = []
    pcons = []
    syllables = []
    sylstring = ''
    oldac = None
    prev_cons = False

    for phon in pron:
        last = phon[-1]
        if verbose > 1:
            print("=============================== phon: %s \t last: %s" % (phon, last))
        if '0' <= last and last <= '9':
            # This phon is a vowel string; strip off the digit and increment the syllable  count.
            vowel = phon[0:-1]
            newac = last
            phons.append(vowel)
            if sylstring:
                if oldac:
                    ncons = len(pcons)
                    if ncons > 1:
                        # split consonants between current and new syllable
                        scons = ''.join(pcons).lower().translate(TRANS_PCONS)
                        parts = hyphenator.word_syllables(scons)
                        if verbose > 0:
                            print("PCONS:", pcons, "   sylstring:", sylstring,  "  SCONS: ", scons, "  PARTS: ", parts)
                        if len(parts) > 1:
                            syllable = sylstring + parts[0].upper()
                            sylstring = parts[1].translate(TRANS_PARTS).upper() + vowel
                        else:
                            syllable = sylstring + ''.join(pcons[0:-1])
                            sylstring = ''.join(pcons[-1]) + vowel
                        if verbose > 0:
                            print("syllables{} appending CLOSED {}".format(syllables, syllable))
                        syllables.append(syllable)
                        pcons = []
                    elif ncons == 1:
                        # Affix the consonant to the syllable with the stroger vowel
                        if newac == '1' or oldac != '1':
                            if verbose > 1:
                                print("# Next phoneme Q = %s is a stressed vowel (%s) or prev was unstressed (%s)" % (
                                    vowel, newac, oldac), end='')
                                print("; new vowel takes last consonant P = %s." % pcons[0])
                            if verbose > 0:
                                print("PCONS:", pcons, "   sylstring:", sylstring)
                                print("syllables{} appending OPEN {}".format(syllables, sylstring))
                            syllables.append(sylstring)
                            sylstring = pcons[0] + vowel
                        else:
                            if verbose > 1:
                                print("# Next phoneme Q is unstressed vowel (%s)" % vowel, end='')
                                print("; current syllable appends current consonant P = %s." % pcons[0])
                            syllables.append(sylstring + pcons[0])
                            sylstring = vowel
                        pcons = []
                    else:
                        # this vowel immediately follows previous vowel
                        if verbose > 0:
                            print("syllables{} appending OPEN {}".format(syllables, sylstring))
                        syllables.append(sylstring)
                        sylstring = vowel
                else:   # current syllable had not gotten a vowel; now it has
                    sylstring = ''.join(pcons, vowel)
                    pcons = []
            else:
                sylstring = ''.join(pcons) + vowel
                pcons = []
            oldac = last
        else:
            phons.append(phon)
            pcons.append(phon)

    if sylstring:
        syllable = sylstring + ''.join(pcons)
        if verbose > 0:
            print("WORD syllables{} appending {}\n".format(syllables, syllable))
        syllables.append(syllable)
    phonetics = ''.join(phons)
    return PhoneTuple(len(phonetics), phonetics, len(syllables), syllables)


def test_phone_seqs(cmu_prons, hyphenator, verbose):
    words = ['obama', 'fledgling', 'cooperate', 'inadvertant', 'fortify',
    'aggressive', 'ornery', 'potato', 'potable', 'preternatural', 'chivalry',
    'egg', 'banana', 'hopelessness', 'aphrodisiac', 'lightproof', 'matchstick',
    'nightclub', 'corkscrew',
    'lengthwise', 'aardvark']
    if verbose > 5:
        words = ['aardvark']
    for word in words:
        prons = cmu_prons.get(word)
        if prons:
            print("Testing phonetic sequencing on WORD %s" % word)
            for pron in prons:
                seq2 = phone_seq_2(pron, hyphenator, verbose)
                seq1 = phone_seq_1(pron, verbose)
                # print("syllable counts: %d v. %d" % (seq1.count, seq2.count))
                print("SEQ1:", seq1)
                print("SEQ2:", seq2)
                if seq1 != seq2:
                    print("^^^^ WRONG! ^^^^")
                print()
        else:
            print("WORD %s has no CMU prons" % word)

TRANS_NO_DIGITS = str.maketrans('', '', string.digits)

def phon_from_pron(pron):
    '''Returns string representing the phonetic spelling
    from a single CMU pronunciation list of phonemes.'''
    joined = ''.join(pron)
    return joined.translate(TRANS_NO_DIGITS)

def cmu_phon(cmu_prons, word, verbose=False):
    '''Returns a comparable sequence of phonemes from the first CMU pronunciation,
    if present, else an empty string.'''
    try:
        return phon_from_pron(cmu_prons[word][0])
    except KeyError:
        if verbose:
            print("cmu_phonetics NonKEY: ", word)
    return ''

def cmu_phonetics(cmu_prons, word, verbose=False):
    '''Creates a comparable sequence of phonemes for each CMU pronunciation and
    returns the (possibly empty) list.'''
    phons = []
    try:
        for pron in cmu_prons[word]:
            phons.append(phon_from_pron(pron))
    except KeyError:
        if verbose:
            print("cmu_phonetics NonKEY: ", word)
    return phons

class PhoneticWord:
    '''Class holding phonetic representations of a single word.'''
    def __init__(self, cmu_prons_dict, word, verbose=0):
        # print("PhoneSeq.__init__(cmu_prons{}, {})".format(type(cmu_prons), word))
        self.word = word
        self.lwrd = word.lower()
        self.cmu_prons = cmu_prons_dict.get(self.lwrd, [])
        self.phone_sex = [phone_seq_1(pron, verbose) for pron in self.cmu_prons]
        if verbose:
            print("PhoneticWord.__init__: ", end='')
            if self.cmu_prons:
                for idx, seq in enumerate(self.phone_sex):
                    print(idx, self.word, seq.syllables)
            else:
                print(self.word, ": No CMU pronunciations")

    def prons(self):
        '''Returns a list of CMU pronunciations of word; it may be empty.'''
        return self.cmu_prons

    def phons(self):
        '''Returns a list of phonetic representations of word; it may be empty.'''
        return self.phone_sex

CMU_PRON_DICT = None

def cmu_pd():
    '''Returns CMU Pronouncing Dictionary as a global.'''
    global CMU_PRON_DICT
    if CMU_PRON_DICT is None:
        CMU_PRON_DICT = cmudict.dict()
    return CMU_PRON_DICT

def get_prons(word):
    '''Returns CMU Pronouncing Dictionary entry for word, or None.'''
    try:
        return CMU_PRON_DICT.get(word)
    except:
        return cmu_pd().get(word)

def get_pron(word):
    '''Returns first pron in CMU Pronouncing Dictionary entry for word, or None.'''
    try:
        return cmu_pd()[word][0]
    except KeyError:
        return None

def get_phons(word, verbose=False):
    '''Returns phonetic spellings for word based on CMU Pronouncing Dictionary.'''
    return cmu_phonetics(cmu_pd(), word, verbose)


def main():
    '''extract vowels, syllables, pronunciations, etc. from text'''
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="test English chunking")
    parser.add_argument('input_file', type=str, nargs='?', default='train_1000.label',
                        help='file containing text to filter')
    parser.add_argument('-dir', dest='text_dir', type=str, default='/Users/sprax/text',
                        help='directory to search for input_file')
    parser.add_argument('-charset', dest='charset', type=str, default='iso-8859-1',
                        help='charset encoding of input text')
    parser.add_argument('-output_file', type=str, nargs='?', default='lab.txt',
                        help='output path for filtered text (default: - <stdout>)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    cmu_prons = cmu_pd() # get the CMU Pronouncing Dict
    hyphenator = hyphenate.get_default_hyphenator()

    if args.verbose:
        print(parser.prog, ":", main.__doc__, "\n")
    for sentence, counts in EXAMPLES.items():
        print("MANUAL", counts[0], sentence)
        tokens = word_tokens(sentence)
        print("TOKENS", len(tokens), tokens)
        swords = words_split_out(sentence)
        print("SPLITS", len(swords), swords)
        scount = syl_count_sum(cmu_prons, tokens)
        vcount = count_vowel_groups(sentence)
        fcount = count_vowels_first_last(sentence)
        print("SYLLABLES:  manual(%d)  cmupro(%d)  vowel_groups(%d)  nrules(%d)" % (
            counts[1], scount, vcount, fcount))
        print()

        test_phone_seqs(cmu_prons, hyphenator, args.verbose)

if __name__ == '__main__':
    main()
