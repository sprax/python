#!/usr/bin/env python
'''Functions for catching and handling KeyboardInterrupts.'''

import time

def handle_kbint(start_time, prev_kbint_time, message, location=None, inspect=True):
    '''
    Handle KeyboardInterrupt with just a method, not a class.
    Usage (as inside a long-running loop):
        start_time = prev_kbint = time.time()
        try:
            # do things
        except KeyboardInterrupt:
            seconds_since_kbint = handle_KeyboardInterrupt(start_time, prev_kbint_time, location, message)
            break if seconds_since_kbint < 2 else prev_kbint_time += seconds_since_kbint
    '''
    kbint_time = time.time()
    sec_since_start = kbint_time - start_time
    sec_since_kbint = kbint_time - prev_kbint_time
    if location is None:
        if inspect:
            import inspect
            location = inspect.stack()[1][3]
        else:
            location = ''
    print("\nKeyboardInterrupt at %d seconds, %d since prior: %s: %s" % (
        sec_since_start, sec_since_kbint, location, message))
    return sec_since_kbint


def test_handle_kbint():
    '''test_handle_kbint: Since the KeyboardInterrupt will be caught during
    the sleep(1), the printed odd count will lag 1 behind the even count.'''
    count = even = odd = 0
    start_time = prev_kbint = time.time()
    print("kbint BEG", count)
    while True:
        try:
            count += 1
            even = count * 2
            time.sleep(1)
            odd = even + 1
        except KeyboardInterrupt:
            sec_since_kbint = handle_kbint(start_time, prev_kbint, "Count %d,  Even %d,  Odd %d." % (
                count, even, odd))
            if sec_since_kbint < 1:
                print("Caught 2 interrupts in less than a second -- breaking out of loop in test_handle_kbint!")
                break
            prev_kbint += sec_since_kbint
    print("kbint END", count)

###############################################################################
if __name__ == '__main__':
    test_handle_kbint()
