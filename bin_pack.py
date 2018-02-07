#!/usr/bin/env python3
'''
Can the space requirements specified by bits be packed into the specified bins?
'''

import sys
from pdb import set_trace

class BinPack:
    '''
    Implementation: Naive exhaustive recursion with supplementary array.
    Complexity: Time O(N!), additional space O(1).
    '''
    pass


def canPackRecursive(bins, num_usable, items, num_unpacked, usableSpace, neededSpace):
    '''
    * Sorted recursion.  Early return if largest item cannot fit in largest remaining bin.
    * @param bins
    * @param num_usable
    * @param items
    * @param num_unpacked
    * @return
    '''
    if num_unpacked < 1:
        return True
    if num_usable < 1:
        return False

    j = num_unpacked - 1
    k = num_usable - 1

    # return False if the largest remaining bin cannot fit the largest num_unpacked item.
    if bins[k] < items[j]:
        return False

    # Use reverse order, assuming the inputs were sorted in ascending order.
    for k in reversed(range(num_usable)):
        diff_k_j = bins[k] - items[j]
        if diff_k_j >= 0:                         # expected to be True at beginning of loop
            swapping = False
            if diff_k_j < items[0]:               # If the space left in this bin would be less than the
                usableSpace -= diff_k_j            # smallest item, then this bin would become unusable.
                if usableSpace < neededSpace:     # If the remaining usable space would not suffice,
                    return False                   # return False immediately, without decrementing, etc.
                swapping = True                    # Need to swap the diminished bins[k] off the active list.

            usableSpace -= items[j]
            neededSpace -= items[j]
            bins[k] = diff_k_j

            if swapping:
                num_usable -= 1
                bins[k] = bins[num_usable]
                bins[num_usable] = diff_k_j
            else:
                # Otherwise, sort the list by re-inserting diminished bin[k] value where it now belongs.
                for q in reversed(range(k)):
                    if diff_k_j < bins[q]:
                        bins[q + 1] = bins[q]
                    else:
                        break
                bins[q + 1] = diff_k_j

            # Exhaustive recursion: check all remaining solutions that start with item[j] packed in bin[q]
            if canPackRecursive(bins, num_usable, items, j, usableSpace, neededSpace):
                return True

            # failed, so swap back and increment.
            if swapping:
                bins[num_usable] = bins[k]
                bins[k] = diff_k_j
                usableSpace += diff_k_j
                num_usable += 1

            usableSpace += items[j]
            neededSpace += items[j]
            bins[k] += items[j]
    return False


def excess(bins, bits):
    return sum(bins) - sum(bits)


def canPackTrack(bins, bits):
    '''returns True IFF bits can be packed into bins'''
    usableSpace = sum(bins)
    neededSpace = sum(bits)
    excess = usableSpace - neededSpace
    if excess < 0:
        return False        # return early: insufficient total space

    sbins = sorted(bins)    # make a sorted copy
    sbits = sorted(bits)

    if sbins[-1] < sbits[-1]:
        return False        # return early: max bin < max bit

    if canPackRecursive(sbins, len(sbins), sbits, len(sbits), usableSpace, neededSpace):
        # Change the original array.  (Pass by value means bins = sbins would not.)
        for  idx, sbin in enumerate(sbins):
            bins[idx] = sbin
        return True

    print("sbins after failure:", sbins)
    return False


def canPack(bins, bits):
    return canPackTrack(bins, bits)


def main():
    bins = [1, 1, 4]
    bits = [2, 3]
    print("canPack({}, {}) ? {}".format(bins, bits, canPack(bins, bits)))


if __name__ == '__main__':
    main()
