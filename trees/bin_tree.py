#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
# import pdb
# from pdb import set_trace

class BinTreeNode:
    ''' binary tree node with parent, left, right,
    key (for placement) and value (for payload)'''

    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

    def has_left(self):
        '''unnecessary convenience method'''
        return self.left

    def has_right(self):
        '''unnecessary convenience method'''
        return self.right

    def is_left(self):
        '''True IFF this is the left child of its parent'''
        return self.parent and self.parent.left == self

    def is_right(self):
        '''True IFF this is the right child of its parent'''
        return self.parent and self.parent.right == self

    def is_root(self):
        '''True IFF this node has no parent'''
        return not self.parent

    def is_leaf(self):
        '''True IFF this node has no child'''
        return not (self.right or self.left)

    def is_parent(self):
        '''True IFF this node is a parent, that is, has a child'''
        return self.left or self.right

    def is_full(self):
        '''True IFF this node is a double parent, that is, has both a left and a right child'''
        return self.left and self.right

    def set_node_data(self, key, val, left, right):
        ''' (re)sets all node data and re-parents child nodes '''
        self.key = key
        self.val = val
        self.left = left
        self.right = right
        if left:
            left.parent = self
        if right:
            right.parent = self


class BinSearchTree:
    ''' basic binary search tree '''

    def __init__(self):
        ''' null root; if present, root counts in size '''
        self.root = None
        self.size = 0

    def length(self):
        '''returns the number of nodes in the tree'''
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.root.__iter__()

    def put(self, key, val):
        '''replace tree's val for key, if present, or add new key-val node if not.'''
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = BinTreeNode(key, val)
        self.size += 1

    def _put(self, key, val, node):
        '''recursive implemnetation for put'''
        if key < node.key:
            if node.has_left():
                self._put(key, val, node.left)
            else:
                node.left = BinTreeNode(key, val, parent=node)
        elif key > node.key:
            if node.has_right():
                self._put(key, val, node.right)
            else:
                node.right = BinTreeNode(key, val, parent=node)
        else:   # if key == node.key, replace the value (no duplicate keys)
            node.val = val

    def get(self, key, default=None):
        '''returns val for found key, else default'''
        if self.root:
            node = self._get(key, self.root)
            return node.val if node else default
        return default

    def _get(self, key, node):
        '''recursive implemnetation for get'''
        if not node:
            return None
        if key < node.key:
            return self._get(key, node.left)
        if key > node.key:
            return self._get(key, node.right)
        assert node.key == key
        return node


    def __getitem__(self, key):
        '''
        overloads the [] operator for retrieval, using the get method,
        to mimic dict subscripting
        '''
        return self.get(key)


    def __setitem__(self, key, val):
        '''
        overloads the [] operator for assignment, using the put method,
        to mimic dict assignment
        '''
        self.put(key, val)


    def __contains__(self, key):
        '''implements the "in" operator'''
        if self._get(key, self.root):
            return True
        return False


def mirror_trees(t1, t2):
    '''True IFF binary trees t1 and t2 morror each other'''
    if not t1 and not t2:
        return True
    if t1 or t2:
        return False
    return mirror_trees(t1.left, t2.right) and mirror_trees(t1.right, t2.left)


def test_func_2(func_2, pair, expect, verbose):
    '''
    tests the result of func_2 applied to the pair of arguments against expect.
    Returns the number of wrong answers, that is,
    0 if result == expect,
    1 if not.
    '''
    result = func_2(*pair)
    passed = result == expect
    if verbose > passed:
        print("%s(%s, %d)  %s: expect: %s, result: %s"
              % (func_2.__name__, pair[0], pair[1], "PASS" if passed else "FAIL",
                 expect, result))
    return not passed


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    samples = [
        [["abcd", 4], 0],
        [["abab", 2], 0],
        [["abac", 3], 1],
        [["abacadede", 3], 4],
    ]
    num_wrong = 0
    # for sample in samples:
    #     num_wrong += test_func_2(num_repeat_1_subs_slow, *sample, verbose)
    #
    print("unit_test for has_one_repeated:  num_tests:", len(samples),
          " num_wrong:", num_wrong, " -- ", "FAIL" if num_wrong else "PASS")


def main():
    '''driver for unit_test'''
    const_a = "abcdefgh"
    const_b = "abc_efgh"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', type=str, nargs='?', const=const_a,
                        help="str_a to test against str_b (const: %s)" % const_a)
    parser.add_argument('-b', type=str, nargs='?', const=const_b,
                        help="str_b to test against str_a (const: %s)" % const_b)
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()


    unit_test(args)


if __name__ == '__main__':
    main()
