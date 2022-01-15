#!/usr/bin/env python3
# @file: facade.py
# @auth: sprax
# @date: 2021-10-16 22:31:42 Sat 16 Oct

# Sprax Lines       2016.07.12      Written with Python 3.5

'''
Facade v.  Proxy v.  Adaptor v. (In)formal Interface
'''


class Interface():
    ''' base class '''

    # def __init__(self, name):
    #     self.name = name

    def hi(self):
        pass


class ImplOne(Interface):
    ''' derived class '''

    def __init__(self, name1):
        # super().__init__(name1)
        self.name = name1

    def hi(self):
        print("Howdy, I'm %s!" % self.name)


class ImplTwo(Interface):
    ''' derived class '''

    def __init__(self, name1, name2):
        # super().__init__(name1)
        self.name = name1 + " " + name2

    def hi(self):
        print("Hi hi, I'm %s!" % self.name)


class PrefixMixin(object):
    ''' prefix mixin class '''
    pass


def main():
    imp1 = ImplOne("joe")
    imp1.hi()
    imp2 = ImplTwo("jerry", "hall")
    imp2.hi()


if __name__ == '__main__':
    main()
