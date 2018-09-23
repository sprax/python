'''
gen_prime_pal.py
wrapper by sprax 2018.09, based on:
    Sieve of Eratosthenes
    Code by David Eppstein, UC Irvine, 28 Feb 2002
    http://code.activestate.com/recipes/117119/
'''
from __future__ import print_function
import itertools
import sys

def gen_primes():
    """ Generate an unbounded (infinite) sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    prime_divs = {}
    cnd_val = 2        # The loop var to increment and check for primeness
    while True:
        if cnd_val not in prime_divs:
            # cnd_val is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            yield cnd_val
            prime_divs[cnd_val * cnd_val] = [cnd_val]
        else:
            # cnd_val is composite. prime_divs[cnd_val] is the list
            # of primes that divide it.  Since we've reached cnd_val,
            # we no longer need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger numbers.
            for prm_val in prime_divs[cnd_val]:
                prime_divs.setdefault(prm_val + cnd_val, []).append(prm_val)
            del prime_divs[cnd_val]
        cnd_val += 1

def gen_primes_bounded(beg_val=2, end_val=1000):
    """ Generate a bounded sequence of prime numbers.
    """
    prime_divs = {}
    cnd_val = 2
    while True:
        if end_val < cnd_val:
            break
        if cnd_val not in prime_divs:
            if beg_val <= cnd_val:
                yield cnd_val
            prime_divs[cnd_val * cnd_val] = [cnd_val]
        else:
            for prm_val in prime_divs[cnd_val]:
                prime_divs.setdefault(prm_val + cnd_val, []).append(prm_val)
            del prime_divs[cnd_val]
        cnd_val += 1

def gen_prime_pal():
    """ Generate an infinite sequence of palindromic prime numbers,
        a.k.a prime palindromes.
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in
            gen_primes())) if s[:n//2] == s[-1:h:-1])


def gen_prime_pal_idx_range(beg_idx=0, end_idx=100):
    """
    Generate the subsequence of prime palindromes wih indices
    between beg_idx and end_idx.  That is, return a generator
    that, from the infinite sequence of palindromic prime numbers,
    yields only those that would have indices in the range
    [beg_idx, end_idx].  The returned generator will thus
    yield end_idx - beg_idx prime palindromes before it is exhausted.
    """
    return itertools.islice((x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in gen_primes()))
                             if s[:n//2] == s[-1:h:-1]), beg_idx, end_idx)


def gen_prime_pal_sub_range(beg_idx=0, end_idx=1000):
    """
    Generate the subsequence of palindromic primes from the sequence
    of all primes as indexed from beg_idx to end_idx.
    That is, return a generator that, from the infinite sequence of
    prime numbers, yields only those that are palindromic and would
    have indices in the range [beg_idx, end_idx].  The returned
    generator's length will thus be however many of those N indexed
    primes are palindromic, where N = end_idx - beg_idx.
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in itertools.islice(
                gen_primes(), beg_idx, end_idx))) if s[:n//2] == s[-1:h:-1])


def gen_prime_pal_val_range(beg_val=0, end_val=1000):
    """
    Generate sequence of prime palindromes between beg_val and end_val.
    That is, return a generator that, from the finite range of integers
    between beg_val and end_val, yields only those that are palindromic
    primes.
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in gen_primes_bounded(beg_val, end_val)))
            if s[:n//2] == s[-1:h:-1])


DEFAULT_BEG = 100
DEFAULT_END = 2000

def main():
    '''Print lists of prime palindromes (default up to X)'''
    argc = len(sys.argv)
    beg_num = int(sys.argv[1]) if argc > 1 else DEFAULT_BEG
    end_num = int(sys.argv[2]) if argc > 2 else DEFAULT_END
    print("prime num value range:", *list(gen_primes_bounded(beg_num, end_num)))
    print("prime pal value range:", *list(gen_prime_pal_val_range(beg_num, end_num)))
    print("prime pal subix range:", *list(gen_prime_pal_sub_range(beg_num, end_num)))
    print("prime pal index range:", *list(gen_prime_pal_idx_range(beg_num, end_num)))

if __name__ == '__main__':
    main()
