#!/usr/bin/env python3
'''
Can the space requirements specified by bits be packed into the specified bins?
'''
from itertools import islice
import pdb
from pdb import set_trace
import sys
from time import time

from num import fibonaccis
from num import prime_gen as pg

class BinPack:
    '''
    Implementation: Naive exhaustive recursion with supplementary array.
    Complexity: Time O(N!), additional space O(1).
    '''
    pass


def canPackRecursive(bins, num_usable, bits, num_unpacked, usableSpace, neededSpace):
    '''
    * Sorted recursion.  Early return if largest item cannot fit in largest remaining bin.
    * @param bins
    * @param num_usable
    * @param bits
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
    if bins[k] < bits[j]:
        return False

    # Use reverse order, assuming the inputs were sorted in ascending order.
    for k in reversed(range(num_usable)):
        diff_k_j = bins[k] - bits[j]
        if diff_k_j >= 0:                         # expected to be True at beginning of loop
            swapping = False
            if diff_k_j < bits[0]:               # If the space left in this bin would be less than the
                usableSpace -= diff_k_j            # smallest item, then this bin would become unusable.
                if usableSpace < neededSpace:     # If the remaining usable space would not suffice,
                    return False                   # return False immediately, without decrementing, etc.
                swapping = True                    # Need to swap the diminished bins[k] off the active list.

            usableSpace -= bits[j]
            neededSpace -= bits[j]
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
                        bins[q + 1] = diff_k_j
                        break
                else:
                    # set_trace()
                    bins[0] = diff_k_j

            # Exhaustive recursion: check all remaining solutions that start with item[j] packed in bin[q]
            if canPackRecursive(bins, num_usable, bits, j, usableSpace, neededSpace):
                return True

            # failed, so swap back and increment.
            if swapping:
                bins[num_usable] = bins[k]
                bins[k] = diff_k_j
                usableSpace += diff_k_j
                num_usable += 1

            usableSpace += bits[j]
            neededSpace += bits[j]
            bins[k] += bits[j]
    return False


def excessSpace(bins, bits):
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


def canPackNaive(bins, bits):
    packed = [False] * len(bits)
    return canPackNaiveRec(bins, bits, packed)


def canPackNaiveRec(bins, bits, packed):
    '''
    * Naive exhaustive recursion, no early failure (as when sum(bins) < sum(bits)), no sorting.
    * Tries to fit bits into bins in the original order given.
    * @param bins
    * @param bits
    * @param packed
    * @return
    '''
    if all(packed):
        return True

    for i in range(len(bits)):
        if not packed[i]:
            # Exhaustive: check all remaining solutions that start with item[i] packed in some bin[j]
            packed[i] = True
            for j in range(len(bins)):
                if (bins[j] >= bits[i]):
                    bins[j] -= bits[i]            # deduct item amount from bin and try to pack the rest
                    if canPackNaiveRec(bins, bits, packed):
                        return True                # success: return
                    bins[j] += bits[i]   # failure: restore item amount to bin
            packed[i] = False
    return False


class BinPackTest:
    pass


def show_wrong(result, expected):
    if result == expected:
        return 0
    print("Wrong result %s, expected %s\n" % (result, expected))
    return 1


def test_canPack(can_pack, bins, bits, verbose, name, number, expected):
    result = False
    excess = excessSpace(bins, bits)
    if verbose > 0:
        print("\n\t  Test canPack:  %s: %d\n" % (name, number))
        print("bin space before: ", bins)
        print("bits to pack:    ")
        # # TODO Sx.printFolded(bits, 24)
        binTot = sum(bins)
        itemTot = sum(bits)
        diff = binTot - itemTot
        assert(diff == excess)
        print("Total bin space - bits space: %d - %d = %d\n" % (binTot, itemTot, diff))

    if excess < 0:
        print("Insufficient total bin space.")
    else:
        # Test the interface function:
        begTime = time()
        result = can_pack(bins, bits)
        runTime = time() - begTime
        if verbose > 0:
            print("Pack bits in bins? %s\n", result)
            print("Bin space after:  ", bins)

        print("Run time millis:    %d\n", runTime)
        if result:
            assert sum(bins) == excess

    return show_wrong(result, expected)


def passFail(numWrong):
        return "PASS" if numWrong == 0 else "FAIL"

def test_packer(packer, packer_name, level):
    testName = type(BinPack).__name__ + ".test_packer(" + packer_name + ")"
    numWrong = 0
    testNum = 0

    seas = [2, 2, 37]
    holes = [4, 37]
    numWrong += test_canPack(packer, seas, holes, 1, testName, ++testNum, False)

    servers = [8, 16, 8, 32]
    tasks = [18, 4, 8, 4, 6, 6, 8, 8]
    print("%s:\t%d\n", testName, ++testNum)
    numWrong += test_canPack(packer, servers, tasks, 1, testName, ++testNum, True)

    limits = [1, 3]
    needs = [4]
    print("%s:\t%d\n", testName, ++testNum)
    numWrong += test_canPack(packer, limits, needs, 1, testName, ++testNum, False)

    duffels = [2, 5, 2, 2, 6]
    bags = [3, 3, 5]
    print("%s:\t%d\n", testName, ++testNum)
    numWrong += test_canPack(packer, duffels, bags, 1, testName, ++testNum, True)

    sashes = [1, 2, 3, 4, 5, 6, 8, 9]
    badges = [1, 4, 6, 6, 8, 8]
    print("%s:\t%d\n", testName, ++testNum)
    numWrong += test_canPack(packer, sashes, badges, 1, testName, ++testNum, False)

    if level > 1:
        print("%s:\t%d\n", testName, ++testNum)

        fibs = fibonaccis.fib_generate(12)
        mems = list(islice(pg.sieve(), 47))
        # mems = Primes.primesInRangeIntArray(2, 47)
        numWrong += test_canPack(packer, fibs, mems, 1, testName, ++testNum, True)

        crates = fibonaccis.fib_generate(9)
        boxes = Primes.primesInRangeIntArray(2, 25)
        numWrong += test_canPack(packer, crates, boxes, 1, testName, ++testNum, False)

        if level > 2:    # A naive algorithm may take a very long time...
            frames = fibonaccis.fib_generate(13)
            photos = Primes.primesInRangeIntArray(2, 70)
            numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)
            blocks = fibonaccis.fib_generate(14)
            allocs = Primes.primesInRangeIntArray(2, 90)
            numWrong += test_canPack(packer, blocks, allocs, 1, testName, ++testNum, False)

            frames = fibonaccis.fib_generate(15)
            photos = Primes.primesInRangeIntArray(2, 125)
            numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)

            frames = fibonaccis.fib_generate(15)
            photos[0] = 4
            numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)

            frames = fibonaccis.fib_generate(36)
            photos = Primes.primesInRangeIntArray(2, 27650)
            for j in range(min(1500, len(photos))):
                photos[j] += 1

            numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)

    print("\nEND   %s,  wrong %d,  %s\n\n", testName, numWrong, passFail(numWrong));
    return numWrong


def unit_test(level):
    testName = "BinPack.unit_test"
    print("BEGIN:", testName)
    numWrong = 0

    bins = [1, 1, 4]
    bits = [2, 3]
    print("canPack(:, :) ? :".format(bins, bits, canPack(bins, bits)))

    numWrong += test_packer(canPackTrack, "canPackTrack", level + 2)
    numWrong += test_packer(canPackNaive, "canPackNaive", level)

    print("END: ", testName, numWrong)
    return numWrong


def main():
    unit_test(2)

if __name__ == '__main__':
    main()
