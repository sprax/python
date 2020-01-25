#!/usr/bin/env python3
''' add two numbers represented as linked lists
'''
import pdb
from pdb import set_trace

class ListNode(object):
    ''' Definition for singly-linked list. '''
    def __init__(self, data):
        self.data = data
        self.next = None

# Utility function to print the linked LinkedList
def printList(node, label=''):
    print("%s[" % label, end='')
    temp = node
    while (temp):
        print(" %d" % temp.data, end='')
        temp = temp.next
    print(']')

class Solution(object):
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        # # with temp, faster than 24.3%
        # nxt = node.next
        # node.data = nxt.data
        # node.next = nxt.next
        # direct, faster than 83.3%
        try:
            node.data = node.next.data
            node.next = node.next.next
        except AttributeError:
            pass

def main():
    ''' test driver '''
    sol = Solution()
    l1 = ListNode(4)
    ld = ListNode(5)
    l1.next = ld
    l1.next.next = ListNode(1)
    le = ListNode(9)
    l1.next.next.next = le

    printList(l1, "BEG entire list: ")
    sol.deleteNode(ld)
    printList(l1, "DEL node link 1: ")
    sol.deleteNode(le)
    printList(l1, "DEL saved end N: ")


    #
    # l2 = ListNode(5)
    # l2.next = ListNode(6)
    # nx = l2.next
    # nx.next = ListNode(7)
    # nx = nx.next
    # nx.next = ListNode(8)
    # nx = nx.next
    # nx.next = ListNode(9)
    # # set_trace()
    # l3 = (l1, l2)


if __name__ == '__main__':
    main()
