#!/usr/bin/env python3

import sys
import argparse


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Trilateration")
    parser.add_argument("-p1", nargs=3, metavar=("x", "y", "z"), help="first base station position", required=True)
    parser.add_argument("-p2", nargs=3, metavar=("x", "y", "z"), help="second base station position", required=True)
    parser.add_argument("-p3", nargs=3, metavar=("x", "y", "z"), help="third base station position", required=True)
    parser.add_argument("-r1", type=float, metavar=("r"), help="distance to first base station", required=True)
    parser.add_argument("-r2", type=float, metavar=("r"), help="distance to second base station", required=True)
    parser.add_argument("-r3", type=float, metavar=("r"), help="distance to third base station", required=True)
    args = parser.parse_args()

    p1, p2, p3 = args.p1, args.p2, args.p3
    r1, r2, r3 = args.r1, args.r2, args.r3

    # Validate input
    if r1 < 0 or r2 < 0 or r3 < 0:
        print("Invalid input! Distance may not be negative!")
        return 1

    # TODO Convert to planar coordinate system (all points on z = 0)

    # TODO Calculate target's position

    # TODO Convert back to original coordinate system


if __name__ == "__main__":
    sys.exit(main())
