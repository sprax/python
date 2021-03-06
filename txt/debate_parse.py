#!/usr/bin/env python3
# Sprax Lines       2016.09.26      Written for Python 3.5
'''Parse a debate transcript into speaker turns:
N > 1 contestants each have approximately the same number T of turns,
M >= 0 moderators collectively have somewhere between T and N*T turns,
and each turn is an array of one or more paragraphs, each of which
divides into one or more sentences.
'''

import argparse
import datetime
import re

import text_ops
import sums_word_freq
from utf_print import utf_print

def main():
    '''get args and call ...'''
    default_debate_text = "djs.txt"
    default_verbose = 1
    default_debug = 1
    # default_start_date = start_date = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Parse and/or summarize a debate transcript."
        )
    parser.add_argument('-all_as_one', action='store_true',
            help='summarize debate as one block of text (no speaker turns)')
    parser.add_argument('debate_text', metavar='TRANSCRIPT', type=str,
            help='convert speaker-labeled text file to paragraphs (default: {})'
            .format(default_debate_text))
    parser.add_argument('-fM', '-freq_max', dest='max_freq', type=float, nargs='?',
           const=1, default=0.9, help='maximum frequency cut-off (default: 0.9)')
    parser.add_argument('-fm', '-freq_min', dest='min_freq', type=float, nargs='?',
           const=1, default=0.1, help='minimum frequency cut-off (default: 0.1)')
    parser.add_argument('-index_only', action='store_true',
            help='output only the indices of extracted sentences')
    parser.add_argument('-lp', '--list_paragraphs', action='store_true',
            help='list paragraph numbers')
    parser.add_argument('-ls', '--list_sentences', action='store_true',
            help='list sentence numbers')
    parser.add_argument('-ns', '-num_sentences', metavar='SENTENCES',
            dest='max_sentences', type=int, nargs='?', const=1, default=1,
            help='max number of sentences per summarized turn')
    parser.add_argument('-nt', '-num_turns', dest='max_turns', metavar='TURNS',
            type=int, nargs='?', const=1, default=0,
            help='max number of turns to show, or 0 for all (default)')
    parser.add_argument('-nw', '-max_words', dest='max_words', metavar='WORDS',
            type=int, nargs='?', const=12, default=0,
            help='maximum words per paragraph: print only the first M words,\
            or all if M < 1 (default: 0)')
    parser.add_argument('-percent', metavar='PERCENT', dest='sum_percent',
            type=int, nargs='?', const=1, default=0,
            help='summarize to PERCENT percent of original number of sentences')
    parser.add_argument('-debug', type=int, nargs='?', const=1, default=default_debug,
            help="debug level (default: {})".format(default_debug))
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=default_verbose,
            help="verbosity of output (default: {})".format(default_verbose))
    args = parser.parse_args()
    verbose = args.verbose
    if args.debug > 3:
        print("args:", args)
        exit(0)

    debate = Debate(args.debate_text, args.max_turns, verbose)

    if args.sum_percent > 0:
        summarize_debate(debate, args, verbose)
    else:
        print_debate(debate, args.max_turns, args.max_words)


def summarize_debate(debate, args, verbose):
    '''Summarize a debate all at once or turn by turn.'''
    sentence_count = 0
    freqsum = sums_word_freq.FrequencySummarizer(args.min_freq, args.max_freq, verbose)
    for turn in debate.all_turns:
        for para in turn.text:
            sentence_count += freqsum.add_text(para)
    print('---------------------------------------------------------------------------')
    if args.all_as_one:
        sum_count, _ = text_ops.resolve_count(0, args.sum_percent, sentence_count)
        if verbose > 0:
            print("Keeping {} of {} sentences.".format(sum_count, sentence_count))
        if args.index_only:
            summary_indices = freqsum.summarize_all_idx(sum_count)
            print(summary_indices)
        else:
            summary_sentences = freqsum.summarize_all_snt(sum_count)
            for sum_sentence in summary_sentences:
                utf_print(sum_sentence)
                print()
    else:
        if verbose > 0:
            print("Keeping {} sentence(s) for each of {} turns."
                    .format(args.max_sentences, debate.turn_count()))
        for turn_id in range(debate.turn_count()):
            summarize_turn(debate, freqsum, turn_id, args)
    print('---------------------------------------------------------------------------')

def summarize_turn(debate, freqsum, turn_id, opt):
    '''Summarize one DebateTurn'''
    old_size = freqsum.sentence_count()
    turn = debate.all_turns[turn_id]
    sents_idx = freqsum.summarize_next_idx(turn.get_text(),
            opt.max_sentences, opt.sum_percent)

    new_size = freqsum.sentence_count()
    print("Turn {}, {}:".format(turn_id, turn.speaker))
    if opt.index_only:
        print(sents_idx)
        return
    sents_idx.sort()
    for j in sents_idx:
        sentence = freqsum.text_sentences[j]
        if opt.list_sentences:
            print("{} in [{}, {}]: ".format(sents_idx, old_size, new_size), end='')
        if opt.max_words:
            text_ops.print_paragraph_regex_count(sentence, opt.max_words)
        else:
            utf_print(sentence)

def print_debate(debate, max_turns, max_words):
    '''Print up to max_turns turns from debate, stopping after max_words per sentence.'''
    para_count = 1
    num_turns = max_turns if max_turns else len(debate.all_turns)
    for idx, turn in enumerate(debate.all_turns[:num_turns]):
        turn.print_turn(idx, para_count, max_words)

class DebateTurn:
    '''one speaker turn in a debate'''
    def __init__(self, speaker, date, text):
        self.speaker = speaker
        self.date = date
        self.text = [text]

    def get_text(self):
        '''Returns all the text in a turn.'''
        return ' '.join(self.text)

    def print_turn(self, turn_index, para_count=0, max_words=0):
        '''print the text of one speaker's turn'''
        print("{} ({})".format(self.speaker, turn_index))
        for para in self.text:
            if para_count:
                print("{}:  ".format(para_count), end='')
                para_count += 1
            if max_words:
                text_ops.print_paragraph_regex_count(para, max_words)
            else:
                utf_print(para)
        print()

class Debate:
    '''Initialize debate as a sequence of turns by moderators and contestants.'''
    def __init__(self, transcript, max_turns, verbose):
        self.speakers = set()
        self.moderators = set()
        self.debaters = set()
        self.all_turns = []
        self.speaker_turns = {}
        self.verbose = verbose
        self.parse_transcript(transcript, max_turns)

    def turn_count(self):
        '''returns the total number of turns'''
        return len(self.all_turns)

    def parse_transcript(self, transcript_file, max_turns):
        '''Populates Debate data: array of all speaker turns as one sequence,
        and dictionary mapping each speaker to an array of turn indices.'''
        verbose = 1
        turn = DebateTurn('[debate start]', datetime.datetime.now(), '')
        prev_speaker = ''
        self.all_turns.append(turn)
        num_turns = 0
        for para in parse_paragraphs(transcript_file):
            if is_comment(para):
                continue

            refd = None
            (speaker, date, body) = extract_speaker_date_body(para, verbose)
            if date:
                refd = date
                print("\t  date:\t", refd)
            if speaker and speaker != prev_speaker:
                num_turns += 1
                if max_turns and num_turns > max_turns:
                    break
                prev_speaker = speaker
                self.add_speaker(speaker)
                turn = DebateTurn(speaker, refd, body)
                self.all_turns.append(turn)
                self.speaker_turns[speaker].append(turn)
            elif body:
                body = body.replace('’', "'")
                turn.text.append(body)
            elif self.verbose > 2:
                print("______parse_paragraph: discarding:\n", para)

    def add_speaker(self, name):
        '''add a name to the set of speakers'''
        if name not in self.speakers:
            self.speakers.add(name)
            self.speaker_turns[name] = []
            if self.verbose > 3:
                print("<==== new speaker: ", name, '====>')

    def add_moderator(self, name):
        '''add a name to the set of moderators'''
        if name in self.debaters:
            raise ValueError('moderator error: ' + name + ' already in debators')
        self.moderators.add(name)
        self.add_speaker(name)

    def add_debater(self, name):
        '''add a name to the set of debators'''
        if name in self.moderators:
            raise ValueError('debater error: ' + name + ' already in moderators')
        self.debaters.add(name)
        self.add_speaker(name)

    def get_turns(self, speaker_name):
        '''get the turns for one speaker'''
        return self.speaker_turns[speaker_name]

    def print_first_per_turn(self, max_words):
        '''Print beginning of turns, up to max words.'''
        for turn in self.all_turns:
            print(turn.speaker)
            for para in turn.text:
                text_ops.print_paragraph_regex_count(para, max_words)
            print()

def parse_paragraphs(path, charset='utf8'):
    '''Just get the paragraphs.'''
    with open(path, 'r', encoding=charset) as text:
        for para in text_ops.paragraph_iter(text):
            yield para

RGX_COMMENT = re.compile('([#(/[.%-])')

def is_comment(string):
    '''comments start with # or // or /* or . or % or - or ... ?'''
    return RGX_COMMENT.match(string) is not None

def extract_speaker_date_body(paragraph, verbose):
    '''extract (date, head, body) from paragraph, where date and body may be None'''
    rem = re.match(speaker_dated_entry_regex(), paragraph)
    if rem:
        if verbose > 2:
            for part in rem.groups():
                utf_print("\t", part)
            print()
        return rem.groups()
    else:
        return (None, None, paragraph)

# rgx_qt = re.compile(r"(?:^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](?:\s+|$)")
# @staticmethod
# def tag_regex(tagsymbols):
    # pattern = r'(?u)\s([{tags}][-+*#&/\w]+)'.format(tags=tagsymbols)
    # return re.compile( pattern, re.UNICODE )

# @staticmethod
def speaker_dated_entry_regex():
    '''return compiled regex pattern'''
    spkr_grp = r'(?:\s*([A-Z]+):(?:\s*))?'
    date_grp = r'(?:\s*(\d\d\d\d.\d\d.\d\d|\d\d.\d\d.\d\d)[-\s])?'
    body_grp = r'(?:\s*)?(\S.*)?'
    pattern = r"{}{}{}".format(spkr_grp, date_grp, body_grp)
    return re.compile(pattern, re.UNICODE)


if __name__ == '__main__':
    main()
