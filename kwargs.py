

#!/usr/bin/env python3
#
# # -*- coding: utf-8 -*-
'''Example classes with args and kwargs in __init__'''

import sys
from pdb import set_trace

class CopyCtor:
    ''' init can be used as a simple copy-constructor.
        When args[0] is an instance, it is copied and kwargs are ignored.
        Otherwise, the kwargs are used and args is ignored.
    '''

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], type(self)) and not kwargs:
            # Copy Constructor
            other = args[0]
            # copy all the other's attributes:
            self.__dict__ = dict(other.__dict__)
            if kwargs:
                print("WARNING: %s.%s:  ignoring kwargs: "
                      % (type(self).__name__, self.__init__.__name__), **kwargs)
        else:
            if args:
                # import pdb; pdb.set_trace()
                # print("WARNING: %s.%s:  ignoring args: "
                #     % (type(self).__name__, sys._getframe().f_code.co_name), *args)
                print("WARNING: %s.%s:  ignoring args: "
                      % (type(self).__name__, self.__init__.__name__), *args)
            self.__dict__ = kwargs


class BothCopyCtor:
    ''' init can be used as a copy-constructor with updates (differences from original).
        If args[0] is an instance, it is copied and the kwargs are used to update the new object.
        Otherwise, the kwargs are used and args is ignored.
    '''

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
                # print("WARNING: %s.%s:  ignoring args: "
                #       % (type(self).__name__, sys._getframe().f_code.co_name), *args)
                print("WARNING: %s.%s:  ignoring args: "
                      % (type(self).__name__, self.__init__.__name__), *args)
            self.__dict__ = kwargs


class KwargsOnly:
    '''init takes kwargs only, and uses only the kwargs that are listed as valid.'''

    def __init__(self, **kwargs):
        valid_kwargs = ['name', 'kind', 'text']
        for key, val in kwargs.items():
            if key not in valid_kwargs:
                raise TypeError("Invalid keyword argument %s" % key)
            setattr(self, key, val)


def test_kwargs(*args):
    '''Test the class constructors'''
    orig = CopyCtor(*args, foo="FOO", bar="BAR")
    print("orig:", orig.__dict__)
    copy = CopyCtor(orig)
    print("copy:", copy.__dict__)
    print()

    both = BothCopyCtor(*args, foo="Foosball", bar="Barbell")
    print("both:", both.__dict__)
    diff = BothCopyCtor(both, bar="Beer", baz="Bazaar")
    print("diff:", diff.__dict__)
    print()

    try:
        bust = KwargsOnly(name='myKwargsOnly', kind='checked', test='Four square')
        print("bust:", bust.__dict__)
    except TypeError as ex:
        print("Caught expected TypeError from KwargsOnly(...test=...):", ex)

    only = KwargsOnly(name='myKwargsOnly', kind='checked', text='Four score')
    print("only:", only.__dict__)

if __name__ == '__main__':
    test_kwargs(sys.argv)
