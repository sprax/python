#!/usr/bin/env python3
'''
template for simple code testing
'''

import argparse
# import pdb
# from pdb import set_trace

def is_bst(tree):
    '''True IFF binary tree is in a valid BST order (left.val <= parent.val <= right.val)'''
    if tree is None:
        return True
    is_bst_left = is_bst_right = True
    if tree.left:
        if tree.left.key >= tree.key:
            return False
        is_bst_left = is_bst(tree.left)
    if tree.right:
        if tree.right.key <= tree.key:
            return False
        is_bst_right = is_bst(tree.right)
    return is_bst_left and is_bst_right


class BinTreeNode(object):
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

    def is_bst(self):
        '''True IFF binary tree is in a valid BST order (left.val <= parent.val <= right.val)'''
        return is_bst(self)


class BinSearchTree(object):
    ''' basic binary search tree '''

    def __init__(self, root=None):
        ''' null root; if present, root counts in size '''
        self.root = root
        self.size = 1 if root else 0

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


    def is_bst(self):
        '''True IFF binary tree is in a valid BST order (left.val <= parent.val <= right.val)'''
        return is_bst(self.root)


def mirror_shaped_trees(ltree, rtree):
    '''True IFF binary trees ltree and rtree morror each other in shape'''
    if not ltree and not rtree:
        return True
    if not ltree or not rtree:
        return False
    return mirror_shaped_trees(ltree.left, rtree.right) and mirror_shaped_trees(ltree.right, rtree.left)

def is_shape_symmetric(node):
    '''True IFF binary tree is symmetric in shape (presence/absence of nodes)'''
    return True if not node else mirror_shaped_trees(node.left, node.right)

def mirror_valued_trees(ltree, rtree):
    '''True IFF binary trees ltree and rtree morror each other in shape and values'''
    if not ltree and not rtree:
        return True
    if not ltree or not rtree:
        return False
    return (ltree.val == rtree.val and
            mirror_valued_trees(ltree.left, rtree.right) and
            mirror_valued_trees(ltree.right, rtree.left))

def is_value_symmetric(tree):
    '''True IFF binary tree is symmetric in shape and value (present and values of nodes)'''
    return True if not tree else mirror_valued_trees(tree.left, tree.right)



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


def test_predicate(verbose, predicate, subject, expect):
    '''
    tests if the predicate function, applied to subject, gives the expected answer.
    Returns the number of wrong answers, that is,
    0 if predicate(subject) == expect,
    1 otherwise.
    '''
    result = predicate(subject)
    passed = result == expect
    if verbose > passed:
        print("%s %s: expected %s for %s"
              % (predicate.__name__, "PASS" if passed else "FAIL", expect, subject))
    return not passed


def unit_test(args):
    ''' test different (kinds of) predicate detectors '''
    root = BinTreeNode(8, "eight")
    left = BinTreeNode(5, "seven", parent=root)
    right = BinTreeNode(11, "seven", parent=root)
    root.left = left
    root.right = right
    tree = BinSearchTree(root)
    pairs = [
        [tree.root, True],
    ]
    num_wrong = 0
    for pair in pairs:
        num_wrong += test_predicate(args.verbose, is_shape_symmetric, *pair)
        num_wrong += test_predicate(args.verbose, is_value_symmetric, *pair)
        num_wrong += test_predicate(args.verbose, BinTreeNode.is_bst, *pair)
    print("unit_test:  num_tests:", len(pairs),
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
