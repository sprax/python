#!/usr/bin/env python3
import argparse
import random
SAMPLE_COUNT = 10
DEFAULT_SEED = 12345

def sample_wiki_titles(text_file, count=SAMPLE_COUNT, seed=DEFAULT_SEED, verbose=1):
    ''' Force the value of the seed so the results are repeatable '''
    random.seed(seed)
    print("samples, count=", count)
    sample_titles = []
    for index, line in enumerate(open("../words.txt")):
            # Generate the reservoir
            if index < count:
                    sample_titles.append(line)
            else:
                    # Randomly replace elements in the reservoir
                    # with a decreasing probability.
                    # Choose an integer between 0 and index (inclusive)
                    r = random.randint(0, index)
                    if r < count:
                            sample_titles[r] = line.rstrip()
    print(sample_titles)

def main():
    '''Extract questions from text?'''
    default_file = '../words.txt'
    parser = argparse.ArgumentParser(description="Validate balance and order of "
                                     "parentheses, braces, and brackets (), {}, []")
    parser.add_argument('count', type=int, nargs='?', const=16, default=10,
                        help='Count of randomly sampled titles (const: 16, default: 10)')
    parser.add_argument('file', type=str, nargs='?', default=default_file,
                        help="Text file, one item per line (default: %s)" % default_file)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    print("args.count:", args.count)

    sample_wiki_titles(args.file, args.count)


if __name__ == '__main__':
    main()
