#!/usr/bin/env python3
# Sprax Lines       2016.09.26      Written for Python 3.5
'''Output some dates.'''

import sys
import time
import datetime

DAY_CODES = ['Mnd', 'Tsd', 'Wnd', 'Thd', 'Frd', 'Std', 'Snd']

def print_dates(beg_day, num_day):
    '''Output dates'''
    date = datetime.datetime.now()
    date += datetime.timedelta(days=beg_day)
    tstm = date.timetuple()
    print(tstm)
    # for _ in itertools.repeat(None, num_day):
    for _ in range(num_day):
        # print("day: ", day)
        date += datetime.timedelta(days=1)
        tstm = date.timetuple()
        dstr = time.strftime("%Y.%m.%d", tstm)
        if tstm.tm_wday < 5:
            locs = 'CIC'
        elif tstm.tm_wday < 6:
            locs = 'Home/NH'
        else:
            locs = 'Home/MIT'
        code = DAY_CODES[tstm.tm_wday]
        # print(tstm)
        # print("%s ==> %s %s\t%s" % (date, dstr, code, locs))
        print("%s %s AM \t%s" % (dstr, code, locs))
        print("%s %s PM \t%s" % (dstr, code, 'Home'))


def main():
    '''get args and call print_dates'''
    argc = len(sys.argv)
    if argc > 3:
        print(sys.argv[0])
        print(__doc__)

    # Get the paths to the files (relative or absolute)
    num_day = int(sys.argv[1]) if argc > 1 else 7
    beg_day = int(sys.argv[2]) if argc > 2 else 0
    print_dates(beg_day, num_day)

if __name__ == '__main__':
    main()
