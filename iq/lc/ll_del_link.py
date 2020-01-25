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

    def next_not_value(self, node, value):
        """
        :type node: ListNode
        :type data: int
        :rtype: ListNode
        """
        # set_trace()
        while (node and node.data == value):
            node = node.next
        return node


    def remove_by_value(self, node, value):
        """
        :type node: ListNode
        :type data: int
        :rtype: ListNode
        """
        # set_trace()
        head = self.next_not_value(node, value)
        node = head
        while (node):
            # print(" %d" % node.data, end='')
            node.next = self.next_not_value(node.next, value)
            node = node.next
        return head

    def removeElements(self, head, data):
        """
        LeetCode signature
        :type head: ListNode
        :type data: int
        :rtype: ListNode
        """
        while (head and head.data == data):
            head = head.next

        node = head
        while (node):
            print(" %d" % node.data, end='')
            next = node.next
            while (next and next.data == data):
                next = next.next
            node.next = next
            node = node.next
        return head



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

    l2 = ListNode(6)
    l2.next = ListNode(6)
    nx = l2.next
    nx.next = ListNode(7)
    nx = nx.next
    nx.next = ListNode(6)
    nx = nx.next
    nx.next = ListNode(8)
    nx = nx.next
    nx.next = ListNode(6)
    nx = nx.next
    nx.next = ListNode(6)
    nx = nx.next
    nx.next = ListNode(9)
    nx = nx.next
    nx.next = ListNode(6)
    # set_trace()
    l3 = (l1, l2)
    printList(l2, "before: ")
    # l2 = sol.remove_by_value(l2, 6)
    l2 = sol.removeElements(l2, 6)
    printList(l2, " after: ")



if __name__ == '__main__':
    main()
