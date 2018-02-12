#!/usr/bin/env python3
''' Polar cooridinate formalae '''

import argparse
import math


class Polar:
    '''2D point in polar coords'''

    def __init__(self, rho, phi):
        ''' initialize radial and angular coordinates '''
        self.rho = rho
        self.phi = phi
        self.xcc = None     # X cartesian coordinate
        self.ycc = None     # Y cartesian coordinate

    def __str__(self):
        return "(%.4f %.4f)" % (self.rho, self.phi)

    def xcoord(self):
        ''' returns memoized X cartesian coordinate '''
        if self.xcc is None:
            self.xcc = self.rho * math.cos(self.phi)
        return self.xcc

    def ycoord(self):
        ''' returns memoized Y cartesian coordinate '''
        if self.xcc is None:
            self.xcc = self.rho * math.sin(self.phi)
        return self.xcc


def distance_cart(pol_a, pol_b):
    '''
    returns the Euclidean distance between two points represented by
    polar coordinates, computed after converting them to a difference
    vector in cartesian coordinates.
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
    parser = argparse.ArgumentParser(description="functions for 2D points as polar coordinates")
    parser.add_argument('-islice', action='store_true',
                        help='use itertools.islice instead of list comprehension')
    parser.add_argument('-seed', type=int, nargs='?', const=1, default=12345,
                        help='seed for random (const: 1,  default: 12345)')
    parser.add_argument('-verbose', type=int, nargs='?', const=1, default=1,
                        help='verbosity of output (default: 1)')
    args = parser.parse_args()

    polar_a = Polar(1, 1*math.pi/6)
    polar_b = Polar(1, 2*math.pi/6)
    print("Cartesian vec distance({}, {}): {}".format(polar_a, polar_b, distance_cart(polar_a, polar_b)))
    print("Trigonometric distance({}, {}): {}".format(polar_a, polar_b, distance_trig(polar_a, polar_b)))


if __name__ == '__main__':
    main()
