#!/usr/bin/env python3
'''Python 3.3+ counter closure'''

def init_counter(count=0):
    '''(re)set counter that increments whenever called (closure)'''
    _count = count      # the enclosed value
    def _increment_counter():
        '''inner incrementer function'''
        nonlocal _count
        _count += 1
        return _count
    return _increment_counter

def main():
    '''test driver for init_counter'''
    counter = init_counter(6)
    print("counter() =>", counter())
    print("counter() => %d" % counter())
    print("Re-initializing counter...")
    counter = init_counter(0)
    print("counter() =>",     counter())
    print("counter() => %d" % counter())


if __name__ == '__main__':
    main()
