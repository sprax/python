#!/usr/bin/env python3
'''Polar cooridinate formalae & functions for 2D points as polar coordinates'''

import argparse
import math
import random
# from pdb import set_trace

class Polar:
    '''2D point in polar coords'''

    def __init__(self, rho, phi):
        ''' initialize radial and angular coordinates '''
        self.rho = rho
        self.phi = phi
        self.xcc = None     # X Cartesian coordinate
        self.ycc = None     # Y Cartesian coordinate

    def __str__(self):
        return "(%.4f %.4f)" % (self.rho, self.phi)


    def xcoord(self):
        ''' returns memoized X Cartesian coordinate '''
        if self.xcc is None:
            self.xcc = self.rho * math.cos(self.phi)
        return self.xcc

    def ycoord(self):
        ''' returns memoized Y Cartesian coordinate '''
        if self.ycc is None:
            self.ycc = self.rho * math.sin(self.phi)
        return self.ycc


def from_xy(xcc, ycc):
    '''returns a Polar instance initialized from Cartesian coords'''
    rho = math.sqrt(xcc * xcc + ycc * ycc)
    phi = math.atan2(ycc, xcc)
    pol = Polar(rho, phi)
    pol.xcc = xcc
    pol.ycc = ycc
    return pol


def distance_cart(pol_a, pol_b):
    '''
    returns the Euclidean distance between two points represented by
    polar coordinates, computed after converting them to a difference
    vector in Cartesian coordinates.
    '''
    x_diff = pol_a.xcoord() - pol_b.xcoord()
    y_diff = pol_a.ycoord() - pol_b.ycoord()
    return math.sqrt(x_diff*x_diff + y_diff*y_diff)


def distance_trig(pol_a, pol_b):
    '''
    returns the Euclidean distance between two points represented by
    polar coordinates, computed using trigonometric formulae.
    '''
    rho_a = pol_a.rho
    rho_b = pol_b.rho
    return math.sqrt(rho_a * rho_a + rho_b * rho_b - 2 * rho_a * rho_b * math.cos(pol_a.phi - pol_b.phi))


def main():
    ''' driver for dice_pair_sum_gen'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-islice', action='store_true',
                        help='use itertools.islice instead of list comprehension')
    parser.add_argument('-seed', type=int, nargs='?', const=1, default=12345,
                        help='seed for random (const: 1,  default: 12345)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    pol_a = Polar(1, 1*math.pi/6)
    pol_b = Polar(1, 2*math.pi/6)
    print("Cartesian vec distance AB({}, {}): {}".format(pol_a, pol_b, distance_cart(pol_a, pol_b)))
    print("Trigonometric distance AB({}, {}): {}".format(pol_a, pol_b, distance_trig(pol_a, pol_b)))

    pol_c = from_xy(pol_a.xcoord(), pol_a.ycoord())
    print("Cartesian vec distance AC({}, {}): {}".format(pol_a, pol_c, distance_cart(pol_a, pol_c)))
    print("Trigonometric distance AC({}, {}): {}".format(pol_a, pol_c, distance_trig(pol_a, pol_c)))

    if args.seed:
        random.seed(args.seed)

    pol_d = Polar(1.0 + random.random(), random.random() * math.pi)
    print("Cartesian vec distance AD({}, {}): {}".format(pol_a, pol_d, distance_cart(pol_a, pol_d)))
    print("Trigonometric distance CD({}, {}): {}".format(pol_c, pol_d, distance_trig(pol_c, pol_d)))

if __name__ == '__main__':
    main()
