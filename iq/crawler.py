#!/usr/bin/env python3
'''
crawl links, printing each URL once
'''
import argparse
# import pdb
# from pdb import set_trace
from pprint import pprint
import re


TEST_PAIRS = [
    ('http://web.mit.edu/', ['http:', 'web.mit.edu']),
    ('http://whereis.mit.edu/', ['http:', 'whereis.mit.edu']),
    ('http://mitstory.mit.edu/', ['http:', 'mitstory.mit.edu']),
    ('https://www.csail.mit.edu/', ['https:', 'www.csail.mit.edu']),
    ('https://www.csail.mit.edu/people?person%5B0%5D=role%3A299', ['https:', 'www.csail.mit.edu', 'people']),
    ('https://www.csail.mit.edu/person/russ-tedrake', ['https:', 'www.csail.mit.edu', 'person', 'russ-tedrake']),
    ('http://drake.mit.edu/index.html',  ['http:', 'drake.mit.edu', 'index.html']),
    ('http://drake.mit.edu/from_source.html',  ['http:', 'drake.mit.edu', 'from_source.html']),
    ('http://drake.mit.edu/bazel.html', ['http:', 'drake.mit.edu', 'bazel.html']),
    ('http://drake.mit.edu/mac.html', ['http:', 'drake.mit.edu', 'mac.html']),
]

TEST_URLS = [x[0] for x in TEST_PAIRS]

TEST_WEB = {
    TEST_URLS[0] : [TEST_URLS[1], TEST_URLS[2]],
    TEST_URLS[2] : [TEST_URLS[0], TEST_URLS[1], TEST_URLS[3]],
    TEST_URLS[3] : [TEST_URLS[0], TEST_URLS[2], TEST_URLS[4]],
    TEST_URLS[4] : [TEST_URLS[0], TEST_URLS[3], TEST_URLS[5]],
    TEST_URLS[5] : [TEST_URLS[6]],
    TEST_URLS[6] : [TEST_URLS[6], TEST_URLS[7]],
    TEST_URLS[7] : [TEST_URLS[0], TEST_URLS[8], TEST_URLS[8], TEST_URLS[9]],
}


def links_from_url(url):
    '''mock-up of scraping links from url'''
    return TEST_WEB.get(url, [])


# TODO: split on '.' as well?   [www, mit, edu] is OK, but [index] vs. [index, htm] vs. [index, html] ??
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


# space-hog version
def print_links_once(url):
    print_links_once_rec(url, set())

def print_links_once_rec(url, visited):
    if url in visited:
        return
    visited.add(url)
    print(url)
    links = links_from_url(url)
    for link in links:
        print_links_once_rec(link, visited)


class UrlCrawler:
    '''toy web crawler'''

    def __init__(self):
        '''save tree root'''
        self.root = dict()          # tree of dicts
        self.size = 0               # number of unique URLs added/printed

    def _add_url(self, url):
        '''returs True IFF url was added (not already in self.root); False otherwise'''
        parts = url_parts(url)
        tree = self.root
        # Traverse non-leaf nodes, adding branches as needed
        for part in parts[0:-1]:
            if not part in tree:
                tree[part] = dict()
            tree = tree[part]
        # Check the leaf node: return True IFF added
        last = parts[-1]
        if last in tree:
            tree[last][last] += 1           # increment found count
            return False
        tree[last] = { last : 1 }           # add leaf with found count = 1
        self.size += 1
        return True

    def print_links_once_rec(self, url):
        '''traverses tree depth-first, printing each URL/link once'''
        if self._add_url(url):
            print(url)
            links = links_from_url(url)
            for link in links:
                self.print_links_once_rec(link)

################################################################################

def print_links_once_crawler(url, verbose=1):
    '''creates a UrlCrawler and used it to print the tree of links from URL'''
    crawler = UrlCrawler()
    print("____ Unique URLs ____:")
    crawler.print_links_once_rec(url)
    if verbose > 1:
        print("\n____ Web as Tree of Links, with Leaf-Node Mapped to Counts ____:")
        pprint(crawler.root)
    return crawler.size


def unit_test(verbose):
    '''test examples'''
    num_wrong = 0
    for pair in TEST_PAIRS:
        num_wrong += test_url_parts(pair[0], pair[1])
    size = print_links_once_crawler(TEST_URLS[0], verbose)
    num_wrong += size != len(TEST_URLS)
    print("unit_test for str_part_sum: num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")

def main():
    '''Extract questions from text?'''
    const_url = TEST_PAIRS[-1][0]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-url', type=str, nargs='?', const=const_url,
                        help="URL to use in testing (const: %s)" % const_url)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()
    verbose = args.verbose

    unit_test(verbose)

if __name__ == '__main__':
    main()
