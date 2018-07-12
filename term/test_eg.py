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
        self.assertEqual( 1.0, 1.0 )
        self.assertNotEqual( 1.0, 0.999999999 )
        self.assertEqual(True, True)




if __name__ == "__main__":
    unittest.main()
