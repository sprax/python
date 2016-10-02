#!/usr/bin/env python3
# Sprax Lines       2016.09.26      Written for Python 3.5
'''Output some dates.'''

import argparse
import sys
import time
import datetime

# DAY_CODES = ['Mnd', 'Tsd', 'Wnd', 'Thd', 'Frd', 'Std', 'Snd']

def print_dates(start_date, offset_days, num_days, per_day):
    '''Output num_days consecutive formatted dates from start_date'''
    date = start_date
    date += datetime.timedelta(days=offset_days)
    tstm = date.timetuple()
    print(tstm)
    # for _ in itertools.repeat(None, num_days):
    for _ in range(num_days):
        # print("day: ", day)
        dstr = time.strftime("%Y.%m.%d %a", tstm)
        if tstm.tm_wday < 5:
            locs = 'Home/CIC'
        elif tstm.tm_wday == 5:
            locs = 'Home/NH'
        else:
            locs = 'Home/MIT'
        # code = DAY_CODES[tstm.tm_wday]
        # print(tstm)
        # print("%s ==> %s %s\t%s" % (date, dstr, code, locs))
        if per_day > 1:
            print("%s AM \t%s" % (dstr, locs))
            print("%s PM \t%s" % (dstr, 'Home'))
        else:
            print("%s\t%s" % (dstr, locs))
        date += datetime.timedelta(days=1)
        tstm = date.timetuple()


def main():
    '''get args and call print_dates'''

    default_num_days = 7
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
    parser.add_argument('-start_date', metavar='DATE', type=str,
                        help='start date (default: today)')
    parser.add_argument('-verbose', type=int, nargs=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    # Expected start_date format: "2013-09-28 20:30:55.78200"
    # default_start_date = datetime.datetime.now()
    start_date = default_start_date = datetime.datetime.now()
    if args.start_date:
        try:
            start_date = datetime.datetime.strptime(args.start_date, "%Y.%m.%d")
        except ValueError:
            print("Failed to parse date: {}; using today!".format(args.start_date))
            start_date = default_start_date
    print_dates(start_date, args.offset_days, args.num_days, args.per_day)

if __name__ == '__main__':
    main()
