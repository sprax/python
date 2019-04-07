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


REQ_NUM, MID_NUM, NEED_OP = 1, 2, 3

def calc_str_ez(mes):
    '''
    calculate value of an arithmetic expression in a string,
    no positive or negative signs allowed.
    '''
    if not isinstance(mes, str):
        raise ValueError("not a str")
    op_chars = ['+', '-', '*', '/']
    num_stack = []
    ops_stack = []
    num = 0
    estate = REQ_NUM
    for ch in mes + ' ':
        print("ch: %s; estate is: %s" % (ch, str(estate)))
        if ch.isdigit():
            dig = ord(ch) - ord('0');
            if estate is MID_NUM:
                num = num * 10 + dig
            else:
                num = dig
                estate = MID_NUM
        elif ch.isspace():
            if estate is MID_NUM:
                print "GOT NUM: (%s)" % num
                num_stack.append(num)
                estate = NEED_OP
        elif ch in op_chars:
            if estate is NEED_OP:
                estate = REQ_NUM
            else:
                raise ValueError("op not expected: (" + ch + "); estate is: " + str(estate))
        else:
            raise ValueError("char not expected: " + ch)
            pass # FIXME start here
    return 99




def main():
    '''drives calc_str_ez, etc.'''
    parser = argparse.ArgumentParser(description="parse and compute arithmetic value of string")
    parser.add_argument('text', type=str, nargs='?', default='7 + 12',
                        help='text to validate')
    args = parser.parse_args()

    print('calc_str_ez("%s") . . .' % (args.text))

    value = calc_str_ez(args.text)
    print('calc_str_ez("%s") = %s' % (args.text, value))

if __name__ == '__main__':
    main()
