'''
gen_prime_pal.py
wrapper by sprax 2018.09, based on:
    Sieve of Eratosthenes
    Code by David Eppstein, UC Irvine, 28 Feb 2002
    http://code.activestate.com/recipes/117119/
'''
import itertools
import sys

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    prime_divs = {}


    cand = 2    # The loop var to increment and check for primeness
    while True:
        if cand not in prime_divs:
            # cand is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            yield cand
            prime_divs[cand * cand] = [cand]
        else:
            # cand is composite. prime_divs[cand] is the list of primes that
            # divide it. Since we've reached cand, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            for prim in prime_divs[cand]:
                prime_divs.setdefault(prim + cand, []).append(prim)
            del prime_divs[cand]
        cand += 1


def gen_prime_pal():
    """ Generate an infinite sequence of palindromic prime numbers,
        a.k.a prime palindromes.
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in
            gen_primes())) if s[:n//2] == s[-1:h:-1])


def gen_prime_pal_idx_range(beg_idx=0, end_idx=1000):
    """ Generate sequence of prime palindromes from beg_idx to end_idx,
        that is, return a generator that, from the infinite sequence of
        palindromic prime numbers, yields only those that would have
        indices in the range [beg_idx, end_idx].
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in itertools.islice(
                gen_primes(), beg_idx, end_idx))) if s[:n//2] == s[-1:h:-1])


DEFAULT_BEG = 100
DEFAULT_END = 2000

def main():
    '''Print lists of prime palindromes (default up to X)'''
    argc = len(sys.argv)
    beg_num = int(sys.argv[2]) if argc > 2 else DEFAULT_BEG
    end_num = int(sys.argv[1]) if argc > 1 else DEFAULT_END

    print list(gen_prime_pal_idx_range(beg_num, end_num))

if __name__ == '__main__':
    main()
