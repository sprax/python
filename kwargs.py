

#!/usr/bin/env python3
#
# # -*- coding: utf-8 -*-
'''Example classes with args and kwargs in __init__'''

import sys

class CopyCtor:
    '''init can be used as a simple copy-constructor.'''
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], type(self)) and not kwargs:
            # Copy Constructor
            other = args[0]
            # copy all the other's attributes:
            self.__dict__ = dict(other.__dict__)
        else:
            if args:
                # import pdb; pdb.set_trace()
                # print("WARNING: %s.%s:  ignoring args: " % (type(self).__name__, sys._getframe().f_code.co_name), *args)
                print("WARNING: %s.%s:  ignoring args: " % (type(self).__name__, self.__init__.__name__), *args)
            self.__dict__ = kwargs


class BothCopyCtor():
    '''init can be used as a simple copy-constructor.'''
    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], type(self)):
            # Copy Constructor
            other = args[0]
            # copy all the other's attributes:
            self.__dict__ = dict(other.__dict__)
            if kwargs:
                self.__dict__.update(kwargs)
        else:
            if args:
                # import pdb; pdb.set_trace()
                # print("WARNING: %s.%s:  ignoring args: " % (type(self).__name__, sys._getframe().f_code.co_name), *args)
                print("WARNING: %s.%s:  ignoring args: " % (type(self).__name__, self.__init__.__name__), *args)
            self.__dict__ = kwargs

def test_kwargs(*args):
    orig = CopyCtor(*args, foo="FOO", bar="BAR")
    print("orig:", orig.__dict__)
    copy = CopyCtor(orig)
    print("copy:", copy.__dict__)
    print()

    both = BothCopyCtor(*args, foo="Foosball", bar="Barbell")
    print("both:", both.__dict__)
    diff = BothCopyCtor(both, bar="Beer", baz="Bazaar")
    print("diff:", diff.__dict__)



if __name__ == '__main__':
    test_kwargs(sys.argv)
