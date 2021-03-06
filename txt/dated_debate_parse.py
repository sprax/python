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
import time

import text_ops
from utf_print import utf_print

def main():
    '''get args and call ...'''
    default_format_out = '%Y.%m.%d %a'
    default_debate_text = "djs.txt"
    # default_start_date = start_date = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Read/write journal-entry style dates"
        )
    parser.add_argument('debate_text', metavar='TRANSCRIPT', type=str,
                        help='convert speaker-labeled text file to paragraphs (default: {})'
                        .format(default_debate_text))
    parser.add_argument('-out_format', metavar='FORMAT', type=str, default=default_format_out,
                        help='output date format (default: {})'
                        .format(default_format_out.replace('%', '%%')))
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    in_formats = ['%Y.%m.%d']
    out_format = args.out_format if args.out_format else default_format_out

    debate = Debate(args.debate_text, in_formats, out_format, args.verbose)
    # now summarize it...

class DebateTurn:
    def __init__(self, speaker, date, text):
        self.speaker = speaker
        self.date = date
        self.text = text
        
class Debate:
    '''Initialize debate as a sequence of turns by moderators and contestants.'''
    def __init__(self, transcript, date_formats_in, date_format_out, moderators=[], debaters=[]):
        self.moderators = moderators
        self.debaters = debaters
        self.turn_count = 0
        self.all_turns = []
        self.speaker_turns = {} 
        self.parse_transcript(transcript, date_formats_in, date_format_out)

    def parse_transcript(self, transcript_file, date_formats_in, date_format_out):
        '''Populates Debate data: array of all speaker turns as one sequence,
        and dictionary mapping each speaker to an array of turn indices.'''
        verbose = 1
        for para in reformat_paragraphs(transcript_file, verbose):
            if is_comment(para):
                continue
            (speaker, date, body) = extract_speaker_date_body(para, verbose)
            if speaker:
                print("<====", speaker, '====>')
            if date:
                refd = reformat_date(date, in_formats, out_format, verbose)
                # print("\t reformatted date:\t", refd)
            if body:
                body = body.replace('’', "'")

def reformat_paragraphs(path, verbose, charset='utf8'):
    '''Just get the paragraphs.'''
    with open(path, 'r', encoding=charset) as text:
        for para in paragraphs.paragraph_iter(text):
            yield para

def is_comment(string):
    return string[0] == '#'


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
    body_grp = r'(?:\s*)?(\w.*)?'
    pattern = r"{}{}{}".format(spkr_grp, date_grp, body_grp)
    return re.compile(pattern, re.UNICODE)


if __name__ == '__main__':
    main()

