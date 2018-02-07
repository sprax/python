#!/usr/bin/env python3
'''
Can the space requirements specified by bits be packed into the specified bins?
'''
from pdb import set_trace
import sys
from time import time

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
                        break
                bins[q + 1] = diff_k_j

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


def main():
    bins = [1, 1, 4]
    bits = [2, 3]
    print("canPack(:, :) ? :".format(bins, bits, canPack(bins, bits)))

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
    def test_canPack(packer, bins, bits, verbose, name, number, expected):
        result = False
        excess = excessSpace(bins, bits)
        if verbose > 0:
            print("\n\t  Test canPack:  %s: %d\n" % (name, number))
            printArray("bin space before: ", bins)
            print("bits to pack:    ")
            Sx.printArrayFolded(bits, 24)
            binTot = IntStream.of(bins).sum()
            itemTot = IntStream.of(bits).sum()
            diff = binTot - itemTot
            assert(diff == excess)
            print("Total bin space - bits space: %d - %d = %d\n" % (binTot, itemTot, diff))

        if excess < 0:
            print("Insufficient total bin space.")
        else:
            # Test the interface function:
            begTime = time()
            result = packer.canPack(bins, bits)
            runTime = time() - begTime
            if verbose > 0:
                print("Pack bits in bins? %s\n", result)
                printArray("Bin space after:  ", bins)

            print("Run time millis:    %d\n", runTime)
            if result:
                assert Arrays.stream(bins).sum() == excess


        return Sz.showWrong(result, expected)


    def test_packer(packer, packer_name, level):
        testName = type(BinPack).__name__ + ".test_packer(" + packer_name + ")"
        Sz.begin(testName)
        numWrong = 0, testNum = 0
        #IBinPack binPacker = new BinPackRec()


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

            fibs = FibonacciInt32.fib32Range(0, 12)
            mems = Primes.primesInRangeIntArray(2, 47)
            numWrong += test_canPack(packer, fibs, mems, 1, testName, ++testNum, True)

            crates = FibonacciInt32.fib32Range(0, 9)
            boxes = Primes.primesInRangeIntArray(2, 25)
            numWrong += test_canPack(packer, crates, boxes, 1, testName, ++testNum, False)

            if level > 2:    # A naive algorithm may take a very long time...
                frames = FibonacciInt32.fib32Range(0, 13)
                photos = Primes.primesInRangeIntArray(2, 70)
                numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)
                            blocks = FibonacciInt32.fib32Range(0, 14)
                allocs = Primes.primesInRangeIntArray(2, 90)
                numWrong += test_canPack(packer, blocks, allocs, 1, testName, ++testNum, False)

                frames = FibonacciInt32.fib32Range(0, 15)
                photos = Primes.primesInRangeIntArray(2, 125)
                numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)

                frames = FibonacciInt32.fib32Range(0, 15)
                photos[0] = 4
                numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)

                frames = FibonacciInt32.fib32Range(0, 36)
                photos = Primes.primesInRangeIntArray(2, 27650)
                for (j = 1 j < 1500 && j < photos.length j++:
                    photos[j] += 1

                numWrong += test_canPack(packer, frames, photos, 1, testName, ++testNum, False)
        Sz.end(testName, numWrong)
        return numWrong


    def unit_test(level):
        testName = BinPack.class.getName() + ".unit_test"
        Sz.begin(testName)
        numWrong = 0

        numWrong += test_packer(BinPack::canPackTrack, "canPackTrack", level + 2)
        numWrong += test_packer(BinPack::canPackNaive, "canPackNaive", level)

        Sz.end(testName, numWrong)
        return numWrong


    def main():
        unit_test(2)

if __name__ == '__main__':
    main()
