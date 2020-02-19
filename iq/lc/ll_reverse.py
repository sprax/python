#!/usr/bin/env python3
''' add two numbers represented as linked lists
'''
import pdb
from pdb import set_trace


class ListNode(object):
    ''' Definition for singly-linked list. '''

    def __init__(self, val):
        self.val = val
        self.next = None


# Utility function to print the linked LinkedList
def printList(node, label=''):
    print("%s[" % label, end='')
    temp = node
    while (temp):
        print(" %d" % temp.val, end='')
        temp = temp.next
    print(']')


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        tail = None
        while (head):
            next = head.next
            head.next = tail
            tail = head
            head = next
        return tail


def main():
    ''' test driver '''
    sol = Solution()

    l2 = ListNode(1)
    l2.next = ListNode(2)
    nx = l2.next
    nx.next = ListNode(3)
    nx = nx.next
    nx.next = ListNode(4)
    nx = nx.next
    nx.next = ListNode(5)
    nx = nx.next
    nx.next = ListNode(6)
    nx = nx.next
    nx.next = ListNode(7)
    nx = nx.next
    nx.next = ListNode(8)
    nx = nx.next
    nx.next = ListNode(9)
    printList(l2, "before: ")
    lr = sol.reverseList(l2)
    printList(lr, " after: ")


if __name__ == '__main__':
    main()
