'''
ggg.py
'''
from __future__ import print_function
import itertools
import sys

def gggg():
    """ GGGG """
    some_divs = {}
    cnd_val = 2
    while True:
        if cnd_val not in some_divs:
            yield cnd_val
            some_divs[cnd_val * cnd_val] = [cnd_val]
        else:
            for ggg_val in some_divs[cnd_val]:
                some_divs.setdefault(ggg_val + cnd_val, []).append(ggg_val)
            del some_divs[cnd_val]
        cnd_val += 1

def gggg_op():
    """ GGGG, optimized"""
    some_divs = {}
    yield 2
    cnd_val = 3
    while True:
        if cnd_val not in some_divs:
            yield cnd_val
            some_divs[cnd_val * cnd_val] = [cnd_val]
        else:
            for ggg_val in some_divs[cnd_val]:
                some_divs.setdefault(ggg_val*2 + cnd_val, []).append(ggg_val)
            del some_divs[cnd_val]
        cnd_val += 2

def gggg_bounded(beg_val=2, end_val=1000):
    """ more """
    some_divs = {}
    cnd_val = 2
    while cnd_val <= end_val:
        if cnd_val not in some_divs:
            if beg_val <= cnd_val:
                yield cnd_val
            some_divs[cnd_val * cnd_val] = [cnd_val]
        else:
            for ggg_val in some_divs[cnd_val]:
                some_divs.setdefault(ggg_val + cnd_val, []).append(ggg_val)
            del some_divs[cnd_val]
        cnd_val += 1

def gggg_slc():
    """ only some """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in
            gggg())) if s[:n//2] == s[-1:h:-1])


def gggg_slc_idx_range(beg_idx=0, end_idx=100):
    return itertools.islice((x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in gggg()))
                             if s[:n//2] == s[-1:h:-1]), beg_idx, end_idx)


def gggg_slc_sub_range(beg_idx=0, end_idx=1000):
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in itertools.islice(
                gggg(), beg_idx, end_idx))) if s[:n//2] == s[-1:h:-1])


def gggg_slc_val_range(beg_val=0, end_val=1000):
    """
    Generate sequence of some palindromes between beg_val and end_val.
    That is, return a generator that, from the finite range of integers
    between beg_val and end_val, yields only those that are palindromic
    somes.
    """
    return (x for x, s, n, h in (
        (x, s, n, n//2 if n%2 else (n-1)//2) for x, s, n in (
            (x, str(x), len(str(x))) for x in gggg_bounded(beg_val, end_val)))
            if s[:n//2] == s[-1:h:-1])


DEFAULT_BEG_NUM = 0
DEFAULT_END_NUM = 32

def main():
    argc = len(sys.argv)
    if argc < 2:
        beg_num = DEFAULT_BEG_NUM
        end_num = DEFAULT_END_NUM
    elif argc < 3:
        beg_num = DEFAULT_BEG_NUM
        end_num = int(sys.argv[1])
    elif argc < 4:
        beg_num = int(sys.argv[1])
        end_num = int(sys.argv[2])
    else:
        print("Usage: %s [[beg] end] # defaults: beg=%d, end=%d"
              % (sys.argv[0], DEFAULT_BEG_NUM, DEFAULT_END_NUM))
        exit(1)

    print("gggg_slc [%s]  beg = %d  end = %d ::::::::::::::::"
          % (sys.argv[0], beg_num, end_num))
    print("ggggo num value range:", *list(itertools.islice((p for p in gggg_op()),
                                          beg_num, end_num)))
    print("ggggo num value range:", *list(itertools.islice((p for p in gggg()),
                                          beg_num, end_num)))
    print("some num value range:", *list(gggg_bounded(beg_num, end_num)))
    print("some pal value range:", *list(gggg_slc_val_range(beg_num, end_num)))
    print("some pal subix range:", *list(gggg_slc_sub_range(beg_num, end_num)))
    print("some pal index range:", *list(gggg_slc_idx_range(beg_num, end_num)))

if __name__ == '__main__':
    main()
