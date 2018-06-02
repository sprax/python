#!/usr/bin/python
'''
Functions and tests for flattening nested lists/tuples into a generator.

Interview Questions:
1.  How can you define a function that sums any list (or tuple) of numbers?
2.  How can you define a function that gives an alternating sum of elements in a list or tuple?
    (Add first element, subtract the next, then alternate -- so + evens and - minus odds == sum(evens) - sum(odds))
3.  What will you do if the elements of the list (or tuple) can be other lists or tuples?
4.  What do you generally call a data structure that may contain elements of the same general data structure?
5.  What kinds of algorithms can you apply to a recursive data structure?
6.  How can you traverse a recursive data structure (visit every node or element) without using recursion?
7.  When you make an iterative function that traverses a recursive data structure, such as a list of lists,
    do you need any additional data structures?
8.  If you use a recursive function, what might happen to the stack?
9.  What is tail-recursion?
10.  What is a generator function?   (In mathematics, physics, computer science, programming)
10a.     What is a generator in Python?  In other languages?
10b.     What is the point of generators in general?
11. What are EAFP and LBYL?
11a.     In what contexts might it be better to ask for forgiveness than for permission?
11b.     In what contexts might it be better to ask for forgiveness than for permission?
12.  How can you define a function that transforms any list whose elements may be scalars, lists, or tuples into a simple list of scalars?
12a.     What are the inputs and the output of such a "flatten" function?
12b.     What choices do you make for the algorithm, with what consequences?
12c.     What about the order of the output list?  Do all choices in 9b give the same outcome?
12d.     Can you name the possible output orders?  (breadth-first?  depth-first?  level-order?  pre-order?  in-order?)

13. How can you define a function that, given an iterable recursive data structure in which the leaf nodes are numbers,
    outputs the alternating sum of all its elements?
13a.    What do you need to know to make your function compute the right answer?
13b.    What do you need to know to make your function compute that answer efficiently?
13c.    If the requirment is to traverse a large list breadth-first (level-order),
        what additional data structure would you use to make the algorithm efficient?   [queue]
13d.    If the requirment is to traverse a large list depth-first (pre-order),
        what additional data structure would you use to make the algorithm efficient?   [stack]

Error Handling:
14. What if the argument passed to this last function is one number, not a list or other iterable?
14a.    What extra step could handle that case?
15. How to handle an argument list of lists that contains non-numerical leaf nodes?
15a.    Pre-filter, ignore non-numbers in-place, or throw?

Testing Questions:
16. How would you test that the your function's implementation is correct?
16a.    Is it enough to get the right answer on a few test examples?  Why or why not?
16b.    How could you divide up your testing to be more sure it gives you what you want?

Bonus Questions:
17. Does the simple flatten_df_rec give pre-order, in-order, post-order, or what?
18. Can any N-ary tree be mapped uniquely (and thus reversibly) to a list of leaves and recursive lists?
18a.    How?    [Hint: Where do you put the tree's root node?]
18b.    A trie is a kind of tree, right?  How can you map a prefix-tree of all English words to a recursive list?
        [Hint: What is the root node of such a trie or prefix-tree?]
19. Can any list of lists be mapped uniquely (and thus reversibly) to an N-ary tree?
18a.    Can you map each list value to exactly one tree node?
18b.    Will each tree-node point to exactly one value in the original list?  Must it?
18c.    Hint: How to you map an empty list to a tree?  How about [1, 2, 3]?  And [[[1], 2], 3]?
'''
from __future__ import print_function
from collections import deque

POS_SUM = sum

EASIER_LIST = [0, 1, [3, 4], 2, [5, [7, 8], 6, [9]]]
'''           [ ]
            /  |  \
           0   1   2
             / |   | \
            3  4   5  6
                  / \  \
                 7   8  9
 pre-order (root, children left to right): 0 1 3 4 2 5 7 8 6 9
post-order (children left to right, root): 0 3 4 1 7 8 5 9 6 2
  in-order (left, root, right) is not well-defined for non-binary trees
'''

HARDER_LIST = [[2], 0, [3, [6, [[10, [12, [14, 15], 13], 11]]], [7, 8, 9]], 1, [4, 5]]
'''
              [ ]
            /  |   \
          [ ]  0    1
          /    |   / \
         2     3  4   5
              / \
             6  [ ]
            /  / | \
          [ ] 7  8  9
          / \
         10  11
        / \
      12   13
     /  \
    14  15
'''

def flatten_df_rec(lst):
    '''Flattens nested lists or tuples in-order
    (but fails on strings)'''
    for item in lst:
        try:
            for i in flatten_df_rec(item):
                yield i
        except TypeError:
            yield item


def flatten_bf_itr(lst, trace=False):
    '''
    Flattens nested lists or tuples in "breadth-first" or "level-order"
    '''
    queue = deque([lst])
    while queue:
        lst = queue.popleft()
        try:
            for elt in lst:
                try:
                    first = elt[0]
                    queue.append(elt)
                    if trace:
                        print("elt[0]={}\tQ<{}>)".format(first, queue))
                except (IndexError, TypeError):
                    if trace:
                        print("E={}\tq<{}>)".format(elt, queue))
                    yield elt
        except (IndexError, TypeError):
            if trace:
                print("X({})\tq<{}>)".format(lst, queue))
            yield lst


def alt_sum(flat_iter):
    '''
    alternately adds and subtracts elements in an iterable (as in a simple list
    or tuple), with verbosity.  Adds first element, subtracts second, and so on.
    '''
    asum, sign = 0, 1
    for elem in flat_iter:
        asum += sign * elem
        sign = -sign
    return asum


def test_flatten(flatten_func, nested_list, verbose):
    '''applies a function to flatten a possibly nested list, with verbosity'''
    result = flatten_func(nested_list)
    if verbose:
        listed = list(result)
        print("test_flatten({}, {}) => {}".format(flatten_func.__name__,
                                                  nested_list, listed))
        return listed
    return result


def test_pos_sum(pos_sum_func, flat_iter, verbose):
    ''' applies a function to sum a simple iterable (as in a list or tuple),
        with verbosity '''
    result = pos_sum_func(list(flat_iter))
    if verbose:
        print("test_pos_sum({}, {}) => {}".format(pos_sum_func.__name__,
                                                  flat_iter, result))
    return result


def test_alt_sum(alt_sum_func, flat_iter, verbose):
    ''' applies a function to alternately add and subtract elements in an iterable
    (as in a simple list or tuple), with verbosity '''
    result = alt_sum_func(list(flat_iter))
    if verbose:
        print("test_alt_sum({}, {}) => {}".format(test_alt_sum.__name__,
                                                  flat_iter, result))
    return result


def test_flatten_pos_alt_sums(flatten_func, nested_list, verbose):
    ''' Tests flattening and summing functions '''
    flat_iter = test_flatten(flatten_func, nested_list, verbose)
    pos_value = test_pos_sum(POS_SUM, flat_iter, verbose)
    alt_value = test_alt_sum(alt_sum, flat_iter, verbose)
    if verbose:
        print("pos sum: %d,  alt sum: %d\n" % (pos_value, alt_value))
    return flat_iter, pos_value, alt_value


def test_flattens_and_sums(nested_list, verbose):
    ''' Tests flattening and summing functions '''
    df_flat, df_pos, df_alt = test_flatten_pos_alt_sums(flatten_df_rec, nested_list, verbose)
    bf_flat, bf_pos, bf_alt = test_flatten_pos_alt_sums(flatten_bf_itr, nested_list, verbose)
    intersection = [pair[0] for pair in zip(bf_flat, df_flat) if pair[0] == pair[1]]
    if verbose:
        print("intersection of depth-first and breadth-first flattened lists:", intersection)
        print("diff pos sum of depth-first and breadth-first flattened lists:", df_pos - bf_pos)
        print("diff alt sum of depth-first and breadth-first flattened lists:", df_alt - bf_alt)
    return intersection

def main():
    '''tests flatten and sum functions as applied to lists'''
    verbose, overlap = True, []
    overlap += test_flattens_and_sums(EASIER_LIST, verbose)
    overlap += test_flattens_and_sums(HARDER_LIST, verbose)
    print("cumulative overlap:", overlap)

if __name__ == '__main__':
    main()
