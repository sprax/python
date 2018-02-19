#!/usr/bin/env python3
'''
crawl links, printing each URL once
'''
import argparse
# import pdb
# from pdb import set_trace
import re


TEST_PAIRS = [
    ('http://web.mit.edu/',  ['http:', 'web.mit.edu']),
    ('http://whereis.mit.edu/', ['http:', 'whereis.mit.edu']),
    # ('http://mitstory.mit.edu/',
    # ('http://drake.mit.edu/from_source.html',
    # ('http://drake.mit.edu/bazel.html',
    # ('http://drake.mit.edu/mac.html',
    # ('https://www.csail.mit.edu/',
    ('https://www.csail.mit.edu/person/berthold-horn', ['https:', 'www.csail.mit.edu', 'person', 'berthold-horn']),
    ('https://www.csail.mit.edu/people?person%5B0%5D=role%3A299', ['https:', 'www.csail.mit.edu', 'people'])
]

# TODO: splint on '.' as well?   [www, mit, edu] is OK, but [index] vs. [index, htm] vs. [index, html] ??
REC_URL_SPLITTER = re.compile(r'[/]+')

def url_parts(url):
    '''
    returns list of non-empty strings, namely,
    the parts of url as split on "/" and excluding any query string.
    '''
    query_idx = url.find('?')
    if query_idx > 0:
        url = url[0:query_idx]
    return [x for x in REC_URL_SPLITTER.split(url) if x]


def test_url_parts(url, expect, verbose=1):
    '''test url_parts(url)'''
    print("_______ url_parts(%s) ?? Expect: %s" % (url, expect))
    result = url_parts(url)
    failed = result != expect
    print("_______ url_parts(%s) -> Result: %s  --  %s\n" % (url, result, "FAIL" if failed else "PASS"))
    return failed



def print_links_once(url):
    print_links_once_rec(url, set())

def print_links_once_rec(url, visited):
    if url in visited:
        return
    visited.add(url)
    print(url)
    links = getLinksFromPage(url)
    for link in links:
        print_links_once_rec(link, visited)


class UrlCrawler:

    def __init__():
        self.tree = dict()           # tree as dict of dicts (last one can be of leaves)

    def add_url(url):
        '''returs True IFF url was added (not already in self.tree); False otherwise'''
        parts = url_slitter(url)
        tree = self.tree
        for part in parts[0:-1]:
            if part in tree:
                tree = tree[part]
            else:
                tree[part] = dict()

        last = parts[-1]
        if last in tree:
            return False
        else:
            tree[last] = { last : 1 }         # add leaf
            return True


    def print_links_once_rec(self, url):
        if self.add_url(url):
            print(url)
            links = getLinksFromPage(url)
            for link in links:
                self.print_links_once_rec(link)






def unit_test(verbose):
    '''test examples'''
    num_wrong = 0
    for pair in TEST_PAIRS:
        num_wrong += test_url_parts(pair[0], pair[1])
    print("unit_test for str_part_sum: num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")

def main():
    '''Extract questions from text?'''
    const_sod = "01123581321345589144233377610987"
    parser = argparse.ArgumentParser(description=url_parts.__doc__)
    parser.add_argument('-digits', type=str, nargs='?', const=const_sod,
                        help="string of digits to test, instead of running unit_test "
                        "(const: %s)" % const_sod)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    verbose = args.verbose

    if args.digits:
        nums = str_part_sum(args.digits, verbose)
        print("{} -> {}".format(args.digits, nums))
    else:
        unit_test(verbose)

if __name__ == '__main__':
    main()
