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


def num_from_fdl(fdl):
    ''' convert a linked list of digits in forward order, that is,
        an fdl = forward digit list (most significant digit first),
        to a number.
    '''
    num = 0
    if isinstance(fdl, ListNode):
        while fdl:
            num = num * 10 + fdl.val
            fdl = fdl.next
            if not fdl:
                break
    return num



def num_from_rdl(rdl):
    ''' convert a linked list of digits in reverse order, that is,
        an rdo = reversed digit list (least significant digit first),
        to a number.
    '''
    num = 0
    if isinstance(rdl, ListNode):
        pot = 1
        while rdl:
            num += rdl.val * pot
            rdl = rdl.next
            if not rdl:
                return num
            pot *= 10
    return num


def add_two_fwd_dig_lls(l1, l2):
    """
    :type l1: ListNode
    :type l2: ListNode
    :rtype: ListNode
    """
    return num_from_fdl(l1) + num_from_fdl(l2)



def add_two_rev_dig_lls(l1, l2):
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
    num = add_two_fwd_dig_lls(l1, l2)
    print("add_two_fwd_dig_lls =>", num)
    num = add_two_rev_dig_lls(l1, l2)
    print("add_two_rev_dig_lls =>", num)


if __name__ == '__main__':
    main()
