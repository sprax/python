#!/usr/bin/env python3
'''
Can the space requirements specified by bits be packed into the specified bins?
'''
from itertools import islice
# import pdb
# from pdb import set_trace
from datetime import datetime

from num import fibonaccis
from num import prime_gen

class BinPack:
    '''
    Implementation: Naive exhaustive recursion with supplementary array.
    Complexity: Time O(N!), additional space O(1).
    '''
    pass


def can_packRecursive(bins, num_usable, bits, num_unpacked, usableSpace, neededSpace):
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
            if can_packRecursive(bins, num_usable, bits, j, usableSpace, neededSpace):
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


def can_packTrack(bins, bits):
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

    if can_packRecursive(sbins, len(sbins), sbits, len(sbits), usableSpace, neededSpace):
        # Change the original array.  (Pass by value means bins = sbins would not.)
        for  idx, sbin in enumerate(sbins):
            bins[idx] = sbin
        return True

    print("sbins after failure:", sbins)
    return False


def can_pack(bins, bits):
    return can_packTrack(bins, bits)


def can_packNaive(bins, bits):
    packed = [False] * len(bits)
    return can_packNaiveRec(bins, bits, packed)


def can_packNaiveRec(bins, bits, packed):
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
                    if can_packNaiveRec(bins, bits, packed):
                        return True                # success: return
                    bins[j] += bits[i]   # failure: restore item amount to bin
            packed[i] = False
    return False


class BinPackTest:
    pass


def show_wrong(result, expected):
    if result == expected:
        return 0
    print("Wrong result:  %s, expected:  %s\n" % (result, expected))
    return 1


def test_can_pack(can_pack, bins, bits, verbose, name, number, expected):
    result = False
    excess = excessSpace(bins, bits)
    if verbose > 0:
        print("              Test can_pack:  %s: %d" % (name, number))
        print("bins to fill:", bins)
        print("bits to pack:", bits)
        sumBins = sum(bins)
        sumBits = sum(bits)
        diff = sumBins - sumBits
        assert diff == excess
        print("bin space - bits space: %d - %d = %d" % (sumBins, sumBits, diff))

    if excess < 0:
        print("Insufficient total bin space.")
    else:
        # Test the interface function:
        begTime = datetime.now()
        result = can_pack(bins, bits)
        runTime = datetime.now() - begTime
        if verbose > 0:
            print("Pack bits in bins?", result)
            print("Bin space after:", bins)
        print("Run time millis: %7.2f" % (runTime.total_seconds() * 1000))
        if result:
            assert sum(bins) == excess
    return show_wrong(result, expected)


def passFail(num_wrong):
    return "PASS" if num_wrong == 0 else "FAIL"

def test_packer(packer, packer_name, level):
    testName = type(BinPack).__name__ + ".test_packer(" + packer_name + ")"
    num_wrong = 0
    test_num = 0

    if level < 1:

        test_num += 1
        bins = [1, 1, 4]
        bits = [2, 3]
        num_wrong += test_can_pack(packer, seas, holes, 1, testName, test_num, False)

        test_num += 1
        seas = [2, 2, 37]
        holes = [4, 37]
        num_wrong += test_can_pack(packer, seas, holes, 1, testName, test_num, False)

        test_num += 1
        servers = [8, 16, 8, 32]
        tasks = [18, 4, 8, 4, 6, 6, 8, 8]
        num_wrong += test_can_pack(packer, servers, tasks, 1, testName, test_num, True)

        test_num += 1
        limits = [1, 3]
        needs = [4]
        num_wrong += test_can_pack(packer, limits, needs, 1, testName, test_num, False)

        test_num += 1
        duffels = [2, 5, 2, 2, 6]
        bags = [3, 3, 5]
        num_wrong += test_can_pack(packer, duffels, bags, 1, testName, test_num, True)

        test_num += 1
        sashes = [1, 2, 3, 4, 5, 6, 8, 9]
        badges = [1, 4, 6, 6, 8, 8]
        num_wrong += test_can_pack(packer, sashes, badges, 1, testName, test_num, False)

    if level > 0:

        test_num += 1
        crates = list(fibonaccis.fib_generate(11, 1))
        boxes = list(islice(prime_gen.sieve(), 12))
        boxes.append(27)
        num_wrong += test_can_pack(packer, crates, boxes, 1, testName, test_num, False)

        if level > 1:    # A naive algorithm may take a very long time...
            test_num += 1
            fibs = list(fibonaccis.fib_generate(12, 1))
            mems = list(islice(prime_gen.sieve(), 47))
            print("%s:\t%d\n" % (testName, test_num))
            num_wrong += test_can_pack(packer, fibs, mems, 1, testName, test_num, True)

            test_num += 1
            frames = list(fibonaccis.fib_generate(13, 1))
            photos = list(islice(prime_gen.sieve(), 70))
            num_wrong += test_can_pack(packer, frames, photos, 1, testName, test_num, False)

            test_num += 1
            blocks = list(fibonaccis.fib_generate(14, 1))
            allocs = list(islice(prime_gen.sieve(), 2, 90))
            num_wrong += test_can_pack(packer, blocks, allocs, 1, testName, test_num, False)

            test_num += 1
            frames = list(fibonaccis.fib_generate(15, 1))
            photos = list(islice(prime_gen.sieve(), 24))
            num_wrong += test_can_pack(packer, frames, photos, 1, testName, test_num, False)

            test_num += 1
            frames = list(fibonaccis.fib_generate(15, 1))
            photos[0] = 4
            num_wrong += test_can_pack(packer, frames, photos, 1, testName, test_num, False)

            test_num += 1
            frames = list(fibonaccis.fib_generate(36, 1))
            photos = list(islice(prime_gen.sieve(), 27650))
            for j in range(min(1500, len(photos))):
                photos[j] += 1
            num_wrong += test_can_pack(packer, frames, photos, 1, testName, test_num, False)

    print("END   %s,  wrong %d,  %s\n" % (testName, num_wrong, passFail(num_wrong)))
    return num_wrong


def unit_test(level):
    testName = "BinPack.unit_test"
    print("BEGIN:", testName)
    num_wrong = 0

    num_wrong += test_packer(can_packTrack, "can_packTrack", level)
    num_wrong += test_packer(can_packNaive, "can_packNaive", level)

    print("END: ", testName, num_wrong)
    return num_wrong


def main():
    unit_test(1)

if __name__ == '__main__':
    main()
