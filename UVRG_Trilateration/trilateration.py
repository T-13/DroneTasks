#!/usr/bin/env python3

import sys
import argparse
import math
import numpy as np


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Trilateration")
    parser.add_argument(
        "-p1", type=float, nargs=3, metavar=("x", "y", "z"), help="first base station position", required=True)
    parser.add_argument(
        "-p2", type=float, nargs=3, metavar=("x", "y", "z"), help="second base station position", required=True)
    parser.add_argument(
        "-p3", type=float, nargs=3, metavar=("x", "y", "z"), help="third base station position", required=True)
    parser.add_argument("-r1", type=float, metavar=("r"), help="distance to first base station", required=True)
    parser.add_argument("-r2", type=float, metavar=("r"), help="distance to second base station", required=True)
    parser.add_argument("-r3", type=float, metavar=("r"), help="distance to third base station", required=True)
    args = parser.parse_args()

    p1, p2, p3 = np.array(args.p1), np.array(args.p2), np.array(args.p3)
    r1, r2, r3 = args.r1, args.r2, args.r3

    # Validate input
    if r1 < 0 or r2 < 0 or r3 < 0:
        print("Invalid input! Distance may not be negative!")
        return 1

    # Convert to planar coordinate system (all points on z = 0)
    p2n = p2 - p1
    p3n = p3 - p1
    p1n = np.zeros(3)

    v1 = p2n
    v2 = p3n
    v1xv2 = np.cross(v1, v2)

    xn = v1 / np.linalg.norm(v1)
    zn = v1xv2 / np.linalg.norm(v1xv2)
    yn = np.cross(xn, zn)

    d = np.dot(xn, v1)
    i = np.dot(xn, v2)
    j = np.dot(yn, v2)
    p2n = np.array([d, 0, 0])
    p3n = np.array([i, j, 0])

    # Calculate target's position
    x = (r1**2 - r2**2 + d**2) / 2 * d
    y = (r1**2 - r3**2 + i**2 + j**2) / 2 * j - (i / j) * x

    z1 = math.sqrt(r1**2 - x**2 - y**2)
    z2 = -z1

    print(z1)
    print(z2)

    # TODO Convert back to original coordinate system


if __name__ == "__main__":
    sys.exit(main())
