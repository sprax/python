#!/usr/bin/env python3
import argparse
import random
SAMPLE_COUNT = 10
DEFAULT_SEED = 12345

def sample_line_items(text_file, count=SAMPLE_COUNT, seed=DEFAULT_SEED, verbose=1):
    ''' extracts uniformly random sample of count lines from the text file '''
    reservoir = []
    with open(text_file) as text:
        reservoir = reservoir_sample(text, count, seed, verbose)
        if verbose:
            print(reservoir)
    return reservoir


def reservoir_sample(iterable, count=SAMPLE_COUNT, seed=DEFAULT_SEED, verbose=1):
    ''' extracts uniformly random sample from the iterable '''
    random.seed(seed)                   # repeatability
    reservoir = []
    for index, line in enumerate(iterable):
        # Generate the reservoir
        if index < count:
            reservoir.append(line.rstrip())
        else:
            # Randomly replace elements in the reservoir
            # with a decreasing probability.
            # Choose an integer between 0 and index (inclusive)
            rdx = random.randint(0, index)
            if rdx < count:
                reservoir[rdx] = line.rstrip()
    return reservoir


def main():
    ''' driver for sample_line_items'''
    default_file = '../words.txt'
    parser = argparse.ArgumentParser(description=sample_line_items.__doc__)
    parser.add_argument('count', type=int, nargs='?', const=16, default=10,
                        help='Count of randomly sampled lines (const: 16, default: 10)')
    parser.add_argument('file', type=str, nargs='?', default=default_file,
                        help="Text file, one item per line (default: %s)" % default_file)
    parser.add_argument('-seed', type=int, nargs='?', const=1, default=12345,
                        help='seed for random (const: 1,  default: 12345)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    print("args.count:", args.count)

    sample_line_items(args.file, args.count, args.seed, args.verbose)


if __name__ == '__main__':
    main()
