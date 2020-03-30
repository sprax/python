#!/usr/bin/env python3
# Sprax Lines       2016.09.26      Written for Python 3.5
'''Output some dates.'''

import argparse
import datetime
import re
import time

import text_ops
from utf_print import utf_print

# DAY_CODES = ['Mnd', 'Tsd', 'Wnd', 'Thd', 'Frd', 'Std', 'Snd']

def print_dates(out_format, start_date, offset_days, num_days, per_day, verbose):
    '''Output num_days consecutive formatted dates from start_date'''
    date = start_date
    date += datetime.timedelta(days=offset_days)
    # for _ in itertools.repeat(None, num_days):
    for day_num in range(num_days):
        tstm = date.timetuple()
        if verbose > 2:
            print(tstm)
        dstr = time.strftime(out_format, tstm)
        locs = day_locs(tstm.tm_wday, day_num)
        # code = DAY_CODES[tstm.tm_wday]
        # print(tstm)
        # print("%s ==> %s %s\t%s" % (date, dstr, code, locs))
        if per_day > 1:
            print("%s AM \t%s" % (dstr, locs))
            print("%s PM \t%s" % (dstr, 'Home'))
        else:
            print("%s\t%s" % (dstr, locs))
        date += datetime.timedelta(days=1)

def day_locs(wday, count=0):
    '''usual locations'''
    ans = 'Home\tCOVID-19 shutdown, day %d' % count
    # if wday < 5:
    #     ans += 'MIT'
    # if wday in [1, 4]:  # Tuesday or Friday
    #     ans += '/CFC'
    # elif wday in [3, 6]:  # Thursday or Sunday
    #     ans += '/MRC'
    return ans

def try_parse_date(text, in_formats):
    '''Try to extract a date by matching the input date formats.'''
    date = None
    for date_format in in_formats:
        try:
            print("\t\t try_parse(text, date_format) : ({}, {})".format(text, date_format))
            date = datetime.datetime.strptime(text, date_format)
            return date
        except ValueError:
            pass
    return None

def reformat_date(text, in_formats, out_format, verbose):
    '''If text parses as a date of one of the specified formats, return that date.
    Otherwise, return text as-is.'''
    date = try_parse_date(text, in_formats)
    if date:
        tstm = date.timetuple()
        dstr = time.strftime(out_format, tstm)
        if verbose > 0:
            print(date, '=>', dstr)
            if verbose > 5:
                print('=>', tstm)
        return time.strftime(out_format, tstm)
    else:
        return text

def replace_first_date(text, in_formats, out_format, verbose):
    '''Replace any recognized date at the start of text with one of the specified format.'''
    date_first_pat = r"^\s*(\d\d\d\d\.\d\d\.\d\d)'(.*?)[,.!?]'(\s*|$)"
    rgx_date = re.compile(date_first_pat)
    matched = re.match(rgx_date, text)
    if matched:
        raw_date, body = matched.groups()
        ref_date = reformat_date(raw_date, in_formats, out_format, verbose)
        if verbose > 3:
            print(ref_date)
        return "\t".join(ref_date, body)
    return text

def replace_dates(texts, in_formats, out_format, verbose):
    '''Replace any recognized date at the start of text with one of the specified format.'''
    texts_out = []
    for text in texts:
        text_out = replace_first_date(text, in_formats, out_format, verbose)
        if verbose > 3:
            print(text_out)
        texts_out.append(text_out)
    return texts_out


def reformat_journal(jrnl_file, in_formats, out_format, verbose):
    '''rewrite journal file in canonical format'''
    print("convert diary to jrnl format: out_format:", out_format)
    for ref in reformat_all_paragraphs(jrnl_file, in_formats, out_format, verbose):
        if verbose > 0:
            for part in ref:
                utf_print(part)
            print()
        # utf_print('ref: ', ref[0] if len(ref) > 0 else ref)

def reformat_all_paragraphs(path, in_formats, out_format, verbose, charset='utf8'):
    '''Parses paragraphs into leading date, first sentence, and body.
    Reformats the date, if present.'''
    with open(path, 'r', encoding=charset) as text:
        for idx, para in enumerate(text_ops.paragraph_iter(text)):
            if verbose > 3:
                print("    Paragraph {}:".format(idx))
                utf_print(para)
            yield reformat_paragraph(para, in_formats, out_format, verbose)

def reformat_paragraph(paragraph, in_formats, out_format, verbose):
    '''return date string, head, and body from paragraph'''
    if not paragraph:
        print("WARNING: paragraph is empty!")
        return ()
    (date, wday, locs, head, body) = extract_date_head_body(paragraph, verbose)
    if date:
        refd = reformat_date(date, in_formats, out_format, verbose)
        print("\t reformatted date:\t", refd)
    if head:
        head = head.replace('’', "'")
    if body:
        body = body.replace('’', "'")
    return (date, wday, locs, head, body)

def extract_date_head_body(paragraph, verbose):
    '''extract (date, head, body) from paragraph, where date and body may be None'''
    if verbose > 5:
        utf_print("edhb: ", paragraph)
    rem = re.match(dated_entry_regex(), paragraph)
    if rem:
        if verbose > 2:
            for part in rem.groups():
                utf_print("\t", part)
            print()
        return rem.groups()
    else:
        return (None, None, None, None, paragraph)

# rgx_qt = re.compile(r"(?:^\s*|said\s+|says\s+|\t\s*|[,:-]\s+)['\"](.*?)([,.!?])['\"](?:\s+|$)")
# @staticmethod
# def tag_regex(tagsymbols):
    # pattern = r'(?u)\s([{tags}][-+*#&/\w]+)'.format(tags=tagsymbols)
    # return re.compile( pattern, re.UNICODE )

def dated_entry_regex():
    '''return compiled regex pattern'''
    date_grp = r'(?:\s*(\d\d\d\d.\d\d.\d\d|\d\d.\d\d.\d\d)[-\s])?'
    wday_grp = r'(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun|\
                  Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+)?'
    locs_grp = r'(?:\s*([^.?!]+)(?:\t|\s\s+))?'
    head_grp = r'(?:\s*)?([^.?!]+(?:[.?!][\'"]?|$))'
    body_grp = r'(?:\s*)?(\w.*)?'
    pattern = r"{}{}{}{}{}".format(date_grp, wday_grp, locs_grp, head_grp, body_grp)
    return re.compile(pattern, re.UNICODE)

def main():
    '''get args and call print_dates'''
    default_format_out = '%Y.%m.%d %a'
    default_num_days = 7
    default_jrnl_input = "djs.txt"
    start_date = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        # usage='%(prog)s [options]',
        description="Read/write journal-entry style dates"
        )
    parser.add_argument('offset_days', type=int, nargs='?', default=0,
                        help='offset from start date (default: today) to first output date')
    parser.add_argument('num_days', type=int, nargs='?', default=default_num_days,
                        help="number of days' dates to output (default: {})"
                        .format(default_num_days))
    parser.add_argument('per_day', type=int, nargs='?', default=1,
                        help='number of entries per day (default: 1)')
    parser.add_argument('-jrnl_input', metavar='FILE', type=str,
                        help='convert dated-entry text file to jrnl format (default: {})'
                        .format(default_jrnl_input))
    parser.add_argument('-out_format', metavar='FORMAT', type=str, default=default_format_out,
                        help='output date format (default: {})'
                        .format(default_format_out.replace('%', '%%')))
    parser.add_argument('-start_date', metavar='DATE', type=str,
                        help='start date (default: today)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    in_formats = ['%Y.%m.%d']
    out_format = args.out_format if args.out_format else default_format_out

    if args.start_date:
        try:
            start_date = datetime.datetime.strptime(args.start_date, out_format)
        except ValueError:
            print("WARNING: Failed to parse start date: {}; using default: {}"
                  .format(args.start_date, start_date))

    if args.jrnl_input:
        reformat_journal(args.jrnl_input, in_formats, out_format, args.verbose)
    else:
        print_dates(out_format, start_date, args.offset_days, args.num_days
                    , args.per_day, args.verbose)

if __name__ == '__main__':
    main()
