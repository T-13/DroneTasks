#!/usr/bin/env python3

import sys
import argparse
import random
import math
import numpy as np


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Trilateration")
    for i in range(1, 11):
        parser.add_argument(
            "-p{}".format(i), type=float, nargs=3, metavar=("x", "y", "z"),
            help="{}. base station position".format(i), required=i < 4)
        parser.add_argument(
            "-r{}".format(i), type=float, metavar=("r"),
            help="distance to {}. base station".format(i), required=i < 4)
    args = parser.parse_args()

    # Positions
    p = [np.array(args.p1), np.array(args.p2), np.array(args.p3), np.array(args.p4), np.array(args.p5),
         np.array(args.p6), np.array(args.p7), np.array(args.p8), np.array(args.p9), np.array(args.p10)]

    # Distances
    r = [args.r1, args.r2, args.r3, args.r4, args.r5, args.r6, args.r7, args.r8, args.r9, args.r10]

    # Remove all unset args
    p = [x for x in p if x.any()]
    r = [x for x in r if x is not None]

    if len(p) == 3:
        k1, k2 = three_point_trilateration(p, r)

        print([round(i, 2) for i in k1])
        print([round(i, 2) for i in k2])
    elif len(p) == 4:
        k1 = four_point_trilateration(p, r)

        print([round(i, 2) for i in k1])
    else:
        # Pick random unique combinations of stations
        rand_stations = []
        stations = p.copy()  # Copy for shuffling

        while len(rand_stations) < len(p):
            # Randomize and pick first 4
            random.shuffle(stations)
            four_stations = stations[0:4]

            # Always pick different set of stations
            if not already_used_stations(four_stations, rand_stations):
                rand_stations.append(four_stations)

        P = np.array([0.0, 0.0, 0.0])  # End result
        positions = []

        # Calculate all positions
        for stations in rand_stations:
            # Get distances for current stations
            r_of_stations = []
            for s in stations:
                r_of_stations.append(r[get_index(p, s)])

            # Calculate for current 4 stations
            res = four_point_trilateration(stations, r_of_stations)
            positions.append(res)
            P += res

        # Average
        P /= len(p)

        # Calculate error
        err = 0
        for j in positions:
            err += np.linalg.norm(j - P)**2

        err /= len(p)
        err = math.sqrt(err)

        print([round(i, 2) for i in P])
        print("RMSE: {}".format(round(err, 2)))


def get_index(points, point):
    for i, p in enumerate(points):
        if np.array_equal(p, point):
            return i


def already_used_stations(current, previous):
    # Check if current 4 stations had already been used
    for p in previous:
        match = 0
        for point in p:
            all_0 = (point == current[0]).all()
            all_1 = (point == current[1]).all()
            all_2 = (point == current[2]).all()
            all_3 = (point == current[3]).all()
            if all_0 or all_1 or all_2 or all_3:
                match += 1
        if match == 4:
            return True

    return False


def three_point_trilateration(p, r):
    p1, p2, p3 = p[0], p[1], p[2]
    r1, r2, r3 = r[0], r[1], r[2]

    # Convert to planar coordinate system (all points on z = 0)
    v1 = p2 - p1  # Vector from p1 to p2 (p2 is shifted to our coordinate system)
    v2 = p3 - p1  # Vector from p1 to p3 (p3 is shifted to our coordinate system)
    # p1 is center of our coordinate system (0, 0, 0)

    # Create orthogonal axes of our coordinate system (simplified Gram-Schmidt process)
    v1xv2 = np.cross(v1, v2)
    xn = v1 / np.linalg.norm(v1)
    zn = v1xv2 / np.linalg.norm(v1xv2)
    yn = np.cross(xn, zn)

    d = np.dot(xn, v1)  # p1 = [0, 0, 0]
    i = np.dot(xn, v2)  # p2 = [d, 0, 0]
    j = np.dot(yn, v2)  # p3 = [i, j, 0]

    # Calculate target's position
    x = (r1**2 - r2**2 + d**2) / (2 * d)
    y = (r1**2 - r3**2 + i**2 + j**2) / (2 * j) - (i / j) * x
    z = math.sqrt(abs(r1**2 - x**2 - y**2)) * zn

    # Convert back to original coordinate system
    k = p1 + x * xn + y * yn
    k1 = k + z
    k2 = k - z

    return k1, k2


def four_point_trilateration(p, r):
    p1, p2, p3, p4 = p[0], p[1], p[2], p[3]
    r1, r2, r3, r4 = r[0], r[1], r[2], r[3]

    # Convert to planar coordinate system (all points on z = 0)
    v1 = p2 - p1  # Vector from p1 to p2 (p2 is shifted to our coordinate system)
    v2 = p3 - p1  # Vector from p1 to p3 (p3 is shifted to our coordinate system)
    # p1 is center of our coordinate system (0, 0, 0)

    # Create orthogonal axes of our coordinate system (simplified Gram-Schmidt process)
    v1xv2 = np.cross(v1, v2)
    xn = v1 / np.linalg.norm(v1)

    # Exit of vectors are collinear
    if np.linalg.norm(v1xv2) == 0:
        print("V1 and V2 are collinear")
        sys.exit(1)

    zn = v1xv2 / np.linalg.norm(v1xv2)
    yn = np.cross(xn, zn)

    d = np.dot(xn, v1)  # p1 = [0, 0, 0]
    i = np.dot(xn, v2)  # p2 = [d, 0, 0]
    j = np.dot(yn, v2)  # p3 = [i, j, 0]

    # p4 = [a, b, c]
    a = np.dot((p4 - p1), xn)
    b = np.dot((p4 - p1), yn)
    c = np.dot((p4 - p1), zn)

    # Calculate target's position
    x = (r1**2 - r2**2 + d**2) / (2 * d)
    y = (r1**2 - r3**2 + i**2 + j**2) / (2 * j) - (i / j) * x

    if almost_equal(c, 0):
        z = np.zeros(3)
    else:
        z = (r1**2 - r4**2 + a**2 + b**2 + c**2) / (2 * c) - (a / c) * x - (b / c) * y

    # Convert back to original coordinate system
    k = p1 + x * xn + y * yn + z * zn

    return k


# Compares 2 numbers if equal, designed for floats to overcome precision errors
def almost_equal(a, b):
    return np.abs(a - b) < 0.000001


if __name__ == "__main__":
    sys.exit(main())
