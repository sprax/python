'''
gen_prime_pal.py
wrapper by sprax 2018.09, based on:
    Sieve of Eratosthenes
    Code by David Eppstein, UC Irvine, 28 Feb 2002
    http://code.activestate.com/recipes/117119/
'''
import itertools

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1

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
