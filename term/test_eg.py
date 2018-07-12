import unittest
from flask import Flask, render_template, request
# import flaskapi
import requests
import json
import sys

class TestExamples(unittest.TestCase):
    ''' example tests '''

    def test_asserts(self):
        ''' test TestCase's assert* functions '''
        self.assertAlmostEqual(10.0, 9.99999999)
        self.assertAlmostEqual( 1.0, 0.99999999)
        self.assertNotAlmostEqual( 1.0, 0.9999999)
        self.assertNotEqual( 1.0, 0.999999999 )
        self.assertEqual( 1.0, 1.0 )
        self.assertEqual(True, True)
        lst = ['A', 1, 'bb', 'aa']
        dct = { k : n for n, k in enumerate(lst) }
        evn = { k : n for n, k in enumerate(lst) if n % 2 == 0 }
        odd = { k : n for n, k in enumerate(lst) if n % 2 }
        print("lst:", lst)
        print("dct:", dct)
        print("evn:", evn)
        print("odd:", odd)
        self.assertDictContainsSubset( evn, dct )
        self.assertDictContainsSubset( odd, dct )




if __name__ == "__main__":
    unittest.main()
