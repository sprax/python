#!/usr/bin/env python3
''' add two numbers represented as linked lists
'''
import pdb
from pdb import set_trace

class ListNode(object):
    ''' Definition for singly-linked list. '''
    def __init__(self, x):
        self.val = x
        self.next = None


def num_from_rdl(rdl):
    ''' convert a linked list of digits in reverse order, that is,
        an rdo = reversed digit list,
        to a number.
    '''
    sum = 0
    if isinstance(rdl, ListNode):
        pot = 1
        while rdl:
            sum += rdl.val * pot
            rdl = rdl.next
            if not rdl:
                return sum
            pot *= 10
    return sum


def add_two_numbers(l1, l2):
    """
    :type l1: ListNode
    :type l2: ListNode
    :rtype: ListNode
    """
    return num_from_rdl(l1) + num_from_rdl(l2)


def main():
    ''' test driver '''
    l1 = ListNode(1)
    l1.next = ListNode(2)
    l1.next.next = ListNode(3)
    l1.next.next.next = ListNode(4)
    l2 = ListNode(5)
    l2.next = ListNode(6)
    nx = l2.next
    nx.next = ListNode(7)
    nx = nx.next
    nx.next = ListNode(8)
    nx = nx.next
    nx.next = ListNode(9)
    # set_trace()
    num = add_two_numbers(l1, l2)
    print("num =", num)


if __name__ == '__main__':
    main()
