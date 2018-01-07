#!/usr/bin/env python3
# Sprax Lines       2016.07.12      Written with Python 3.5
'''
inheritance and MRO
'''


class Base(object):
    def __init__(self, name):
        self.name = name

    def hi(self):
        print("Hi, I'm %s!" % self.name)

class Derived(Base):
    def __init__(self, name, epi):
        super().__init__(name)
        self.name += " " + epi

    def hi(self):
        print("Hello, I'm %s!" % self.name)

class PrefixMixin(object):
    pass




def main():
    base = Base("joe")
    base.hi()
    derv = Derived("jerry", "hall")
    derv.hi()

if __name__ == '__main__':
    main()
