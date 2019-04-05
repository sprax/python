#!/usr/bin/env python3
'''
Validate balance and order of parentheses, braces, and brackets (), {}, []"
'''
import argparse

OPENERS_TO_CLOSERS = {
    '(' : ')',
    '{' : '}',
    '[' : ']'
}
OPENERS = frozenset(OPENERS_TO_CLOSERS.keys())
CLOSERS = frozenset(OPENERS_TO_CLOSERS.values())


def calc_str_ez(mes):
    '''
    calculate value of an arithmetic expression in a string,
    no positive or negative signs allowed.
    '''
    if not isinstance(mes, str):
        raise ValueError("not a str")
    stack = []
    num = 0
    in_num = False
    rq_num = True
    for ch in mes:
        if ch.isdigit():
            dig = ord(ch) - ord('0');
            if in_num:
                num = num * 10 + dig
            else:
                num = dig
                in_num = true
        elif ch.isspace():
            if in_num:
                in_num = False
                stack.push(num)


            pass # FIXME start here

def is_valid_parens(code):
    '''
    validates balance and ordering of parentheticals: (), {}, [],
    but not the pairs <>, '', or "".
    '''
    openers_stack = []
    for char in code:
        if char in OPENERS:
            openers_stack.append(OPENERS_TO_CLOSERS[char])
        elif char in CLOSERS:
            if not openers_stack:
                return False            # no opener
            if char != openers_stack.pop():
                return False            # wrong closer
    return not openers_stack




def main():
    '''drives is_valid_parens'''
    parser = argparse.ArgumentParser(description="Validate balance and order of "
                                     "parentheses, braces, and brackets (), {}, []")
    parser.add_argument('text', type=str, nargs='?', default='What set { of bracketed '
                        '[ (multi) (parentheticals) ] } is this ??',
                        help='text to validate')
    args = parser.parse_args()

    valid = is_valid_parens(args.text)
    print('is_valid("%s") = %s' % (args.text, valid))

if __name__ == '__main__':
    main()
