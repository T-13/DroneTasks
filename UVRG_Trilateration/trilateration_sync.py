#!/usr/bin/env python3

import sys
import argparse
import random
import math
import numpy as np


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Trilateration requiring time synchronization only between base stations.")

    for i in range(1, 11):
        parser.add_argument(
            "-p{}".format(i), type=float, nargs=3, metavar=("x", "y", "z"),
            help="{}. base station position".format(i), required=i < 4)
        parser.add_argument(
            "-t{}".format(i), type=float, metavar=("t"),
            help="time of received signal form {}. base station".format(i), required=i < 4)

    parser.add_argument(
        "-s", type=float, default=343.0, metavar=("sos"), help="speed of sound (default: 343.0)", required=False)
    args = parser.parse_args()

    # Positions
    p = [np.array(args.p1), np.array(args.p2), np.array(args.p3), np.array(args.p4), np.array(args.p5),
         np.array(args.p6), np.array(args.p7), np.array(args.p8), np.array(args.p9), np.array(args.p10)]

    # Times
    t = [args.t1, args.t2, args.t3, args.t4, args.t5, args.t6, args.t7, args.t8, args.t9, args.t10]

    # Remove all unset args
    p = [x for x in p if x.any()]
    t = [x for x in t if x is not None]

    # At least 5 reference positions are required
    if len(p) < 5:
        print("Error! Less than 5 stations given!")
    elif len(p) == 5:
        # Calculate distances from main station to other stations given times and speed of sound
        r = [args.s * (t[i] - t[0]) for i in range(1, len(p))]

        res = trilaterate_sync(p, r)
        print([round(i, 2) for i in res])
    else:
        # Pick random unique combinations of stations
        rand_p = []
        rand_r = []
        shuffled_p = p.copy()  # Copy for shuffling

        while len(rand_p) < len(p):
            # Randomize and pick first 5
            random.shuffle(shuffled_p)

            # Calculate distances from main station to other stations given times and speed of sound
            shuffled_r = [args.s * (t[i] - t[0]) for i in range(1, len(shuffled_p))]

            # Always pick different set of stations
            if not already_used_stations(shuffled_p[0:5], rand_p):
                rand_p.append(shuffled_p[0:5])
                rand_r.append(shuffled_r[0:5])

        P = np.array([0.0, 0.0, 0.0])  # End result
        positions = []

        # Calculate all positions
        for pos, r_pos in zip(rand_p, rand_r):
            # Calculate for current 5 stations
            res = trilaterate_sync(pos, r_pos)
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


def already_used_stations(current, previous):
    # Check if current 5 stations had already been used
    for p in previous:
        match = 0
        for point in p:
            all_0 = (point == current[0]).all()
            all_1 = (point == current[1]).all()
            all_2 = (point == current[2]).all()
            all_3 = (point == current[3]).all()
            all_4 = (point == current[4]).all()
            if all_0 or all_1 or all_2 or all_3 or all_4:
                match += 1
        if match == 5:
            return True

    return False


def trilaterate_sync(p, r):
    p1, r1 = p[0], r[0]

    # Calculate positional differences
    dp = []
    for pos in p[1:]:
        dp.append(np.array([pos[0] - p1[0], pos[1] - p1[1], pos[2] - p1[2]]))

    h = len(dp)

    # Create linear system
    a = [[0 for x in range(h - 1)] for y in range(h - 1)]
    b = [[0 for x in range(1)] for y in range(h - 1)]

    for i in range(1, len(dp)):
        a[i - 1][0] = ((2 * dp[i][0]) / r[i]) - ((2 * dp[0][0]) / r1)
        a[i - 1][1] = ((2 * dp[i][1]) / r[i]) - ((2 * dp[0][1]) / r1)
        a[i - 1][2] = ((2 * dp[i][2]) / r[i]) - ((2 * dp[0][2]) / r1)

        bi = dp[i][0] ** 2 + dp[i][1] ** 2 + dp[i][2] ** 2
        b0 = dp[0][0] ** 2 + dp[0][1] ** 2 + dp[0][2] ** 2
        b[i - 1][0] = r[i] - r[0] - bi / r[i] + b0 / r[0]

    # Perform Gaussian elimination
    gauss = np.linalg.lstsq(a, b, rcond=None)[0].flatten()

    # Base result off of original position
    return p[0] - gauss


if __name__ == "__main__":
    sys.exit(main())
