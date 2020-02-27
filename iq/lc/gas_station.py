"""
There are N fuel stations along a circular route, where the amount of fuel at station i is fuel[i].

You have a car with an unlimited fuel tank and it costs cost[i] of fuel to travel from station i to its next station (i+1). You begin the journey with an empty tank at one of the fuel stations.

Return the starting fuel station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1.

Note:

If there exists a solution, it is guaranteed to be unique.
Both input arrays are non-empty and have the same length.
Each element in the input arrays is a non-negative integer.
Example 1:

Input:
fuel = [1,2,3,4,5]
cost = [3,4,5,1,2]

Output: 3

Explanation:
Start at station 3 (index 3) and fill up with 4 unit of fuel. Your tank = 0 + 4 = 4
Travel to station 4. Your tank = 4 - 1 + 5 = 8
Travel to station 0. Your tank = 8 - 2 + 1 = 7
Travel to station 1. Your tank = 7 - 3 + 2 = 6
Travel to station 2. Your tank = 6 - 4 + 3 = 5
Travel to station 3. The cost is 5. Your fuel is just enough to travel back to station 3.
Therefore, return 3 as the starting index.
Example 2:

Input:
fuel = [2,3,4]
cost = [3,4,3]

Output: -1

Explanation:
You can't start at station 0 or 1, as there is not enough fuel to travel to the next station.
Let's start at station 2 and fill up with 4 unit of fuel. Your tank = 0 + 4 = 4
Travel to station 0. Your tank = 4 - 3 + 2 = 3
Travel to station 1. Your tank = 3 - 3 + 3 = 3
You cannot travel back to station 2, as it requires 4 unit of fuel but you only have 3.
Therefore, you can't travel around the circuit once no matter where you start
"""
class Solution(object):
    def can_complete_circuit(self, fuel, cost):
        """
        brute force
        :type fuel: List[int]
        :type cost: List[int]
        :rtype: int
        """
        size = len(fuel)
        for beg in range(size):
            tot = 0
            for nxt in range(size):
                idx = (beg + nxt) % size
                tot = tot + fuel[idx] - cost[idx]
                if tot < 0:
                    break
            else:
                return beg
        return -1


    def first_feasible_station(self, fuel, cost):
        """
        Reasoning: Total excess = sum of fuel - cost at each station.
                   If the total < 0, there is no solution; otherwise,
                   there must be at least one solution, by the pigeon hole principle.
        The answer will be the first index after the last indebted one, if it exists.
        :type fuel: List[int]
        :type cost: List[int]
        :rtype: int
        """
        size = len(fuel) # "guaranteed to be > 0"
        if size < 1 or size != len(cost):
            raise ValueError("bad size: fuel({}) cost({})".format(size, len(cost)))
        excess_tot = 0
        excess_run = 0
        result_idx = 0  # assume first index works until proven otherwise
        for idx in range(size):
            excess_now = fuel[idx] - cost[idx]
            excess_tot += excess_now
            excess_run += excess_now
            if (excess_run < 0):
                excess_run = 0
                result_idx = idx + 1    # try the next one
        if excess_tot < 0:
            return -1
        return result_idx


    def canCompleteCircuit(self, fuel, cost):
        """ True IFF first feasible starting station is found (i.e. is not -1) """
        return self.first_feasible_station(fuel, cost)


def test_one(func, fuel, cost, expect):
    actual = func(fuel, cost)
    print("{}({}, {}) => {} =?= {}"
        .format(func.__name__, fuel, cost, actual, expect))
    return actual != expect


def main():
    ''' test Solution '''
    sol = Solution()
    num_wrong = 0

    # Input A:
    fuel = [2,3,4]
    cost = [3,4,3]
    expect = -1
    num_wrong += test_one(sol.canCompleteCircuit, fuel, cost, expect)
    num_wrong += test_one(sol.can_complete_circuit, fuel, cost, expect)

    # Input B:
    fuel = [1,2,3,4,5]
    cost = [3,4,5,1,2]
    expect = 3
    num_wrong += test_one(sol.canCompleteCircuit, fuel, cost, expect)
    num_wrong += test_one(sol.can_complete_circuit, fuel, cost, expect)

    # Input C:
    fuel = [1, 2, 3, 4, 5, 1, 9, 4]
    cost = [3, 4, 5, 1, 9, 1, 2, 4]
    expect = 5
    num_wrong += test_one(sol.canCompleteCircuit, fuel, cost, expect)
    # num_wrong += test_one(sol.can_complete_circuit, fuel, cost, expect)

    # Input D:
    fuel = [5,1,2,3,4]
    cost = [4,4,1,5,1]
    expect = 4
    num_wrong += test_one(sol.canCompleteCircuit, fuel, cost, expect)
    # num_wrong += test_one(sol.can_complete_circuit, fuel, cost, expect)




    print("num_wrong: %d" % num_wrong)

if __name__ == '__main__':
    main()
